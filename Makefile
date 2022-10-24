checkfiles = jwt_helper/ doc/

help:
	@echo "jwt_helper Makefile"
	@echo "usage: make <target>"
	@echo "Targets:"
	@echo "    - doc       Build the documentation"
	@echo "    - package   Build jwt_helper as package"

docdeps:
	pipenv install --dev

doc: docdeps
	rm -fR ./_build
	pipenv run sphinx-build -M html doc _build

package:
	pipenv install
	rm -fR dist/
	pipenv run python -m build
