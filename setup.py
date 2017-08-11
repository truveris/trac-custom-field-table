import os.path
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.rst")).read()
    CHANGES = open(os.path.join(here, "CHANGES.txt")).read()
except IOError:
    README = CHANGES = ""

setup(
    name="trac-custom-field-table", version="0.0.1",
    description="Provides support for showing a table within a ticket "
                "description, of all tickets with ids listed in a given custom "
                "field",
    long_description=README + "\n\n" + CHANGES,
    author="Truveris Inc.",
    author_email="engineering@truveris.com",
    url="http://github.com/truveris/trac-custom-field-table",
    packages=find_packages(exclude=["*.tests*"]),
    license="ISC License",
    install_requires=[
        "Trac>=1.2",
        "Genshi>=0.5",
    ],
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Framework :: Trac",
        "Topic :: Software Development :: Bug Tracking",
    ],
    entry_points={
        "trac.plugins": [
            "trac_custom_field_table = trac_custom_field_table",
        ],
    },
)
