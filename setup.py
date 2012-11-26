# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# Dynamically calculate the version based on adworks.VERSION.
VERSION = (0, 1, 0, 'final', 0)

def get_version(version=None):
    """Derives a PEP386-compliant version number from VERSION."""
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        # At the toplevel, this would cause an import loop.
        from django.utils.version import get_svn_revision
        svn_revision = get_svn_revision()[4:]
        if svn_revision != 'unknown':
            sub = '.dev%s' % svn_revision

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub

setup(
    name="django-adworks",
    version=get_version(),
    description = "A simple Django application to manage ad banner design and approval processes.",
    long_description=open("README.rst").read(),
    keywords=["django", "ad", "banner", "demo"],
    author = "Ozgur Gunes",
    author_email = "o.gunes@gmail.com",
    url = "http://github.com/ozgurgunes/django-adworks/",
    packages=find_packages(),
    install_requires=[
        'django>=1.4',
        'django-uuidfield>=0.4',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    include_package_data=True,
    zip_safe=False,
)
