"""Run many table-driven checks inside one pytest test and report all failures.

The catalogue is data: re-running the same assertions once per size as
separate pytest items only adds noise. ``run_checks`` executes each check
over its cases, collects every failure (labelled ``check[case-id]``, so the
family and size are named) and fails once with the full list.

A check is either a zero-argument callable, or a tuple
``(fn, P(argnames, argvalues, ids=None), ...)``; several ``P`` specs are
combined as a cartesian product, like stacked ``pytest.mark.parametrize``.
"""
from __future__ import annotations

import inspect
import itertools

import pytest
from _pytest.mark.structures import ParameterSet


def P(argnames, argvalues, ids=None, **_ignored):
    """Mirror of ``pytest.mark.parametrize(argnames, argvalues, ids=...)``."""
    if isinstance(argnames, str):
        names = [n.strip() for n in argnames.split(",") if n.strip()]
    else:
        names = list(argnames)
    cases = []
    for index, value in enumerate(argvalues):
        given_id = None
        if isinstance(value, ParameterSet):
            given_id = value.id
            values = tuple(value.values)
        elif len(names) == 1:
            values = (value,)
        else:
            values = tuple(value)
        if ids is not None and given_id is None:
            given_id = ids(value) if callable(ids) else ids[index]
        if given_id is None:
            given_id = "-".join(_auto_id(name, v, index) for name, v in zip(names, values))
        cases.append((str(given_id), dict(zip(names, values))))
    return names, cases


def _auto_id(name, value, index):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return str(value)
    if inspect.isclass(value) or inspect.isfunction(value):
        return value.__name__
    return f"{name}{index}"


def _message(exc):
    text = str(exc).strip() or repr(exc)
    lines = text.splitlines()
    if len(lines) > 6:
        lines = lines[:6] + ["..."]
    return f"{type(exc).__name__}: " + "\n      ".join(lines)


def _label(fn):
    name = fn.__name__
    return name[len("_check_"):] if name.startswith("_check_") else name


def run_checks(*checks):
    failures = []
    ran = 0
    for check in checks:
        if callable(check):
            fn, cases = check, [(None, {})]
        else:
            fn, *specs = check
            cases = []
            for combo in itertools.product(*(spec[1] for spec in specs)):
                ids = [cid for cid, _ in combo]
                kwargs = {}
                for _, kw in combo:
                    kwargs.update(kw)
                cases.append(("-".join(ids), kwargs))
            if not cases:
                failures.append(f"{_label(fn)}: empty case list")
        for case_id, kwargs in cases:
            ran += 1
            label = _label(fn) if case_id is None else f"{_label(fn)}[{case_id}]"
            try:
                fn(**kwargs)
            except (KeyboardInterrupt, SystemExit):
                raise
            except BaseException as exc:  # includes pytest.raises' Failed
                failures.append(f"{label}: {_message(exc)}")
    if failures:
        pytest.fail(f"{len(failures)} of {ran} checks failed:\n  - " + "\n  - ".join(failures),
                    pytrace=False)
    return ran
