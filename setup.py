"""Setup conf for tanuki app."""
from setuptools import setup, find_packages

setup(
    name="tanuki",
    version="0.1.6",
    author="Fabien Schwob",
    author_email="github@x-phuture.com",
    license="AGPL",
    url="https://github.com/jibaku/tanuki/",
    description="""Create dynamic forms in Django""".strip(),
    packages=find_packages(exclude=[]),
    include_package_data=True,
    install_requires=[
        'Django>=1.4',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
