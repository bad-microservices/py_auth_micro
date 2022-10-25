from setuptools import setup
with open('py_auth_micro/_version.py') as infile:
    version_line = infile.read()

version_line = version_line.replace("__version__","")
version_line = version_line.replace("=","")
version_line = version_line.replace(" ","")
version_line = version_line.replace(" ","")
version = version_line.replace("\"","")
setup(

    version=version
)
