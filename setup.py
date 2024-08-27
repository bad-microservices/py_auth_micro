from setuptools import setup

with open("py_auth_micro/_version.py") as infile:
    version_line = infile.read()

version_line = (
    version_line.replace("__version__", "")
    .replace("\n", "")
    .replace("=", "")
    .replace(" ", "")
    .replace(" ", "")
)
version = version_line.replace('"', "")
setup(version=version)
