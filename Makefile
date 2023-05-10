checkfiles = py_auth_micro/ doc/

help:
	@echo "py_auth_micro Makefile"
	@echo "usage: make <target>"
	@echo "Targets:"
	@echo "    - doc       Build the documentation"
	@echo "    - package   Build py_auth_micro as package"
	@echo "    - deps      Installs needed Dependencies"
	@echo "    - devdeps   Installs needed Dependencies for development"

deps:
	pipenv install

devdeps:
	pipenv install --dev

doc: devdeps
	rm -fR ./_build
	pipenv run sphinx-build -M html doc _build

package: devdeps
	rm -fR dist/
	pipenv run python -m build
