#!/usr/bin/env python3
"""Build offline country coverage from runtime families and research registries.

Run with the project environment. No network is used. Boundaries are cached
Natural Earth data; see docs/source/_static/coverage/README.md.
"""
from __future__ import annotations
import importlib
import inspect
import json
import sys
from pathlib import Path
from html import escape
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
ASSETS = ROOT / 'docs/source/_static/coverage'
COUNTRIES = {'aus':'AU','be':'BE','ca':'CA','gr':'GR','ie':'IE','india':'IN','jp':'JP','kr':'KR','mx':'MX','no':'NO','nz':'NZ','pl':'PL','qa':'QA','ru':'RU','th':'TH','tr':'TR','tw':'TW','uk':'GB','us':'US','za':'ZA','cn':'CN','es':'ES','hu':'HU','id':'ID','nl':'NL','np':'NP','ro':'RO','sk':'SK','vn':'VN','kh':'KH','my':'MY','pk':'PK','lk':'LK','bd':'BD','ma':'MA','it':'IT','fr':'FR','dk':'DK','ua':'UA','bg':'BG','lt':'LT','hr':'HR','br':'BR','ar':'AR','cr':'CR'}
NAMES = {'AU':'Australia','BE':'Belgium','CA':'Canada','GB':'United Kingdom','GR':'Greece','IE':'Ireland','IN':'India','JP':'Japan','KR':'South Korea','MX':'Mexico','NO':'Norway','NZ':'New Zealand','PL':'Poland','QA':'Qatar','RU':'Russia','TH':'Thailand','TR':'Türkiye','TW':'Taiwan','US':'United States','ZA':'South Africa','CN':'China','ES':'Spain','HU':'Hungary','ID':'Indonesia','NL':'Netherlands','NP':'Nepal','RO':'Romania','SK':'Slovakia','VN':'Vietnam','KH':'Cambodia','MY':'Malaysia','PK':'Pakistan','LK':'Sri Lanka','BD':'Bangladesh','MA':'Morocco','IT':'Italy','FR':'France','DK':'Denmark','UA':'Ukraine','BG':'Bulgaria','LT':'Lithuania','HR':'Croatia','BR':'Brazil','AR':'Argentina','CR':'Costa Rica'}

# Producer's range is offered in both countries, with the same manual/profile
# definitions. Keep an explicit family allowlist so future Ireland-only ranges
# are not silently attributed to the UK. See Banagher's Bridge Beams page.
SHARED_IE_GB_FAMILIES = {
    'IeMBeamSection', 'IeMYBeamSection', 'IeMYEBeamSection',
    'IeSYBeamSection', 'IeSYEBeamSection', 'IeSolidBoxBeamSection',
    'IeTBeamSection', 'IeTYBeamSection', 'IeUBeamSection',
    'IeUMBBeamSection', 'IeWBeamSection', 'IeYBeamSection',
    'IeYEBeamSection',
}


def implemented():
    result = {}
    for package, code in COUNTRIES.items():
        module = importlib.import_module('bridgebeams.'+package)
        classes = {value for name,value in vars(module).items()
                   if inspect.isclass(value) and name.endswith('Section')
                   and value.__module__.startswith('bridgebeams.'+package+'.')}
        families=[]
        for cls in sorted(classes,key=lambda value:value.__name__):
            name=cls.__name__
            note=''; variants=[]
            if name in ('FebeISection','GrExtendedISection'):
                note='Parametric template: source does not specify all flange thicknesses; zero fixed profiles counted.'
            elif name=='SuperTGirderSection':
                variants=[(f'T{i}, subtype{s}',(i,s),{}) for s in (1,2) for i in range(1,6) if not(i==5 and s==1)]
                note='Nine documented type/subtype combinations; nominal default flange only. Continuous width and web overrides are not additional profiles.'
            elif name=='IGirderSection':
                variants=[(f'T{i}',(i,),{}) for i in range(1,5)]
            elif name=='IeTYBeamSection':
                variants=[(size+' '+variant,(size,),{'variant':variant})
                          for variant in ('bs','ss')
                          for attr in ('SIZES_'+variant.upper(),'SIZES_EDGE_'+variant.upper())
                          for size in getattr(cls,attr)]
            elif name=='NzSuperTSection':
                variants=[('1025 x2490',(1025,),{}),('1225 x2490',(1225,),{}),('1225 x1990',(1225,),{'top_width':1990})]
                note='Three source width/depth arrangements; arbitrary top-width overrides excluded.'
            elif name=='NzHollowCoreSection':
                variants=[(f'{d} {u}',(d,u),{}) for d,u in [(650,'inner'),(900,'inner'),(587,'inner'),(587,'outer')]]
                note='Outer650/900 unresolved; optional drip grooves/local holes excluded. Circular approximation resolution does not add profiles.'
            elif name=='ThDOHIGirderSection':
                variants=[]
                note='Superseded for counting by ThDohIGirderR2Section("IG20"), which resolves the separate web and splay from the 2015 DOH standard; the old plain-web estimate is retained for compatibility.'
            else:
                sizes=getattr(cls,'STANDARD_SIZES',None) or getattr(cls,'SIZES',None) or getattr(cls,'TYPES',None)
                if sizes is None:
                    raise RuntimeError(f'No explicit counting rule for {cls.__module__}.{name}')
                variants=[(str(size),(size,),{}) for size in sizes]
                if name=='KhcISection':note='Three source standard sizes; KHC-20 and KHC-40 extrapolations excluded.'
                if name=='NoNtbKtbSection':note='Includes explicitly recorded user-inferred15 mm bottom chamfers.'
                if name=='QaQBeamSection':note='Documented reconstructed profiles with source-rounding residuals.'
            # Construct each counted choice; namespace aliases are removed above.
            labels=[]; provenance={}
            for label,args,kwargs in variants:
                beam=cls(*args,**kwargs)
                provenance[label]=getattr(beam,'provenance',None) or 'unlabelled'
                poly=getattr(beam,'polygon',None)
                if poly is None:poly=beam.geometry.geom
                if poly.is_empty:raise RuntimeError(f'Empty profile: {name} {label}')
                labels.append(label)
            family_id=f'{cls.__module__}.{name}'
            families.append({'id':family_id,'name':name,'module':cls.__module__,
                             'count':len(labels),'profiles':labels,
                             'profile_ids':[f'{family_id}:{label}' for label in labels],
                             'note':note,'provenance':provenance})
        result[code]=families
    return result


def provenance_counts(unique_families):
    seen={}
    for families in unique_families.values():
        for family in families:
            for label,pid in zip(family['profiles'],family['profile_ids']):
                seen[pid]=family['provenance'][label]
    counts={}
    for value in seen.values():
        counts[value]=counts.get(value,0)+1
    return dict(sorted(counts.items()))


def build():
    boundaries=json.loads((ASSETS/'boundaries.json').read_text())
    countries={f['code']:{'code':f['code'],'name':f['name'],'sources':[],'families':[]} for f in boundaries['features']}
    seen_sources={}
    def add(code,name,source):
        row=countries.setdefault(code,{'code':code,'name':name,'sources':[],'families':[]})
        key=(code,source['id'])
        if key in seen_sources:
            row['sources'][seen_sources[key]]=source
            return False
        seen_sources[key]=len(row['sources'])
        row['sources'].append(source)
        return True
    records=0
    files=['europe-americas-sources.json','asia-africa-sources.json']
    if (ROOT/'docs/research/data/india-followup.json').exists():
        files.append('india-followup.json')
    for filename in files:
        data=json.loads((ROOT/'docs/research/data'/filename).read_text())
        for s in data['sources']:
            added=add(s['country_code'],s['country'],{'title':s.get('title_en') or s.get('title_original') or s['id'],
                'url':s.get('url',''),'status':s.get('status','recorded'),'registry':filename,'id':s['id'],
                'family_names':s.get('families',[]),'title_original':s.get('title_original','')})
            records+=int(added)
    data=json.loads((ROOT/'docs/research/data/pdf-transcriptions.json').read_text())
    for code,s in data['sources'].items():
        add(code.upper(),NAMES[code.upper()],{'title':s['title'],'url':s['url'],'status':'PDF transcription','registry':'pdf-transcriptions.json','id':code})
        records+=1
    data=json.loads((ROOT/'docs/research/data/banagher-pending-families.json').read_text())
    for s in data['sources']:
        # Producer jurisdiction is Ireland. GB records remain independently
        # sourced in the regional registry, not inferred from distribution.
        add('IE','Ireland',{'title':s.get('title_en',s['id'])+' — '+', '.join(s.get('families',[])),
            'url':s.get('url',''),'status':s.get('status','recorded'),'registry':'banagher-pending-families.json','id':s['id']})
        records+=1
    followup = ROOT/'docs/research/data/canada-followup.json'
    if followup.exists():
        canada=json.loads(followup.read_text())
        for s in canada['sources']:
            records+=int(add('CA','Canada',{'title':f"Ontario MTO {s['drawing']}: {s['title']}",
                'url':canada['official_index_url'],'status':s.get('status','current standard drawing'),
                'registry':'canada-followup.json','id':s['drawing']}))
    us_states=ROOT/'docs/research/data/us-states-followup.json'
    if us_states.exists():
        for s in json.loads(us_states.read_text())['records']:
            records+=int(add('US','United States',{'title':f"{s['state']} · {s['title']}",
                'url':s['url'],'status':s['readiness'],
                'registry':'us-states-followup.json','id':s['id']}))
    washington=ROOT/'docs/research/data/us-washington-followup.json'
    if washington.exists():
        ws=json.loads(washington.read_text())
        for key in ('source_outlines','source_properties'):
            s=ws[key]
            records+=int(add('US','United States',{'title':s['title'],'url':s['url'],
                'status':'official drawing and independent property check',
                'registry':'us-washington-followup.json','id':'wsdot_'+key}))
    for deep_search in sorted((ROOT/'docs/research/data').glob('deep-search-*-2026-09.json')):
        for s in json.loads(deep_search.read_text())['records']:
            records+=int(add(s['country_code'],s['country'],{
                'title':s.get('title_en') or s['title_original'],
                'url':s['url'],'status':s['status'],'registry':deep_search.name,
                'id':s['id'],'language':s['language'],'source_type':s['source_type'],
                'locator':s.get('locator',''),'family_names':s['family_names'],
                'title_original':s['title_original']}))
    producer_url='https://banagherprecast.com/products/bridge-beams/'
    for code in ('IE','GB'):
        records+=int(add(code,NAMES[code],{'title':'Banagher Bridge Beams — shared Ireland/UK product range',
            'url':producer_url,'status':'producer confirms range and UK/Ireland supply',
            'registry':'producer availability','id':'banagher_shared_range'}))
    unique_families = implemented()
    for code,families in unique_families.items():
        for family in families:
            family['jurisdictions'] = [code]
        row=countries.setdefault(code,{'code':code,'name':NAMES[code],'sources':[],'families':[]})
        row['families']=families
    # Country rows express availability. A shared profile belongs to both
    # jurisdictions but contributes only once to the distinct global total.
    irish = {family['name']: family for family in unique_families['IE']}
    missing = SHARED_IE_GB_FAMILIES - irish.keys()
    if missing:
        raise RuntimeError(f'Missing shared Banagher families: {sorted(missing)}')
    for name in sorted(SHARED_IE_GB_FAMILIES):
        irish[name]['jurisdictions'] = ['IE', 'GB']
        shared = deepcopy(irish[name])
        shared['name'] = name.replace('Ie', 'Uk', 1)
        shared['note'] = ('Shared Banagher Ireland/UK producer catalogue; '
                          'UK export aliases the same geometry. ' + shared['note']).strip()
        countries['GB']['families'].append(shared)
    for code,row in countries.items():
        row['name']=NAMES.get(code,row['name'])
        row['count']=sum(f['count'] for f in row['families'])
        row['source_count']=len(row['sources'])
        row['researched']=bool(row['sources'])
    result={'count_basis':'Country counts represent named source-backed discrete geometry choices available in that jurisdiction. Shared producer profiles appear in each applicable country but only once in the unique global total. Includes documented reconstructions; excludes arbitrary continuous inputs, incomplete parametric templates and Korean extrapolations. Count is not a design certification.',
        'source_count_basis':'Research source records, including partial, blocked and rejected leads; duplicate publications can have separate family records. Not implemented sections.',
        'researched_jurisdictions':sum(r['researched'] for r in countries.values()),
        'source_records':records,'implemented_countries':sum(r['count']>0 for r in countries.values()),
        'implemented_profiles':len({profile_id for families in unique_families.values()
                                    for family in families for profile_id in family['profile_ids']}),
        'country_profile_assignments':sum(r['count'] for r in countries.values()),
        'provenance_basis':'Distinct profiles by provenance. unlabelled = families implemented before September 2026, which predate the attribute; see their module documentation.',
        'provenance_counts':provenance_counts(unique_families),
        'countries':sorted(countries.values(),key=lambda r:r['name'])}
    (ASSETS/'coverage-data.json').write_text(json.dumps(result,indent=2)+'\n')
    # Fully rendered HTML has no fetch dependency and works through file:// too.
    template=(ASSETS/'coverage-template.html').read_text()
    svg=['<svg viewBox="0 0 1080 470" role="group" aria-label="World coverage by implemented profile count">']
    for f in boundaries['features']:
        if f['code']=='AQ':continue
        row=countries[f['code']];count=row['count']
        level=('low' if count<=5 else 'mid' if count<=15 else 'high' if count<=40 else 'max') if count else ('zero' if row['researched'] else 'norecord')
        label=f"{row['name']}: {count} profiles; {row['source_count']} research records"
        svg.append(f'<path class="country {level}" data-code="{escape(f["code"])}" tabindex="0" role="button" aria-label="{escape(label)}" d="{f["path"]}"><title>{escape(label)}</title></path>')
    svg.append('</svg>')
    rows=[]
    for r in result['countries']:
        def label(f):
            n=sum(v=='estimate' for v in f.get('provenance',{}).values())
            return f"{f['name']} ({f['count']}{', '+str(n)+' estimate' if n else ''})"
        family=', '.join(label(f) for f in r['families']) or '—'
        rows.append(f'<tr data-code="{escape(r["code"])}"><th scope="row"><button class="country-select" data-code="{escape(r["code"])}">{escape(r["name"])}</button></th><td>{escape(r["code"])}</td><td>{r["count"]}</td><td>{r["source_count"]}</td><td>{escape(family)}</td></tr>')
    payload=json.dumps(result).replace('<','\\u003c')
    output=template.replace('<!-- MAP -->',''.join(svg)).replace('<!-- ROWS -->','\n'.join(rows)).replace('/* DATA */',payload)
    output=output.replace('<!-- SUMMARY -->',f"{result['implemented_profiles']} distinct implemented profiles ({', '.join(f'{v} {k}' for k,v in result['provenance_counts'].items())}) · {result['country_profile_assignments']} country-profile assignments · {result['implemented_countries']} countries with fixed profiles · {result['researched_jurisdictions']} researched jurisdictions · {records} source records")
    (ASSETS/'index.html').write_text(output)
    # GB = shared Banagher aliases plus UK-only producer families (e.g. FP McCann).
    uk_own=[f for f in unique_families['GB'] if f['module'].startswith('bridgebeams.uk.')]
    uk_only=sum(f['count'] for f in uk_own)
    assert countries['GB']['count']==sum(irish[name]['count'] for name in SHARED_IE_GB_FAMILIES)+uk_only>0
    assert {pid for f in countries['GB']['families'] for pid in f['profile_ids']} == {
        pid for name in SHARED_IE_GB_FAMILIES for pid in irish[name]['profile_ids']} | {
        pid for f in uk_own for pid in f['profile_ids']}
    assert countries['IN']['count']==9 and countries['IN']['researched']
    print(json.dumps({k:v for k,v in result.items() if k!='countries'},indent=2))
    print('Nonzero country counts:',{r['code']:r['count'] for r in result['countries'] if r['count']})

if __name__=='__main__':build()
