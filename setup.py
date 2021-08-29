from setuptools import setup

setup(
    name="bridgebeams",
    version="0.1.0",
    description="Provides Australian bridge beams for use with the sectionproperties package",
    py_modules=["bridgebeams"],
    author="Colin Caprani",
    url="https://github.com/ccaprani/bridgebeams",
    author_email="colin.caprani@monash.edu",
    install_requires=["sectionproperties"],
)
