# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build


latexpdf2:
	@$(SPHINXBUILD) -M "latexpdf" "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -t Internal
	python replace.py
	cd _build/latex
	xelatex ds-2022-spring-final
	ren ds-2022-spring-final.pdf ds-2022-spring-final-solutions.pdf
	xcopy ds-2022-spring-final-solutions.pdf ../.. /Y
	cd ../..



# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

solutions:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -t Internal
	python replace.py
	cd _build/latex && pdflatex ds-2022-spring-final
	mv _build/latex/ds-2022-spring-final.pdf ds-2022-spring-final-solutions.pdf

questions:
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd _build/latex && pdflatex ds-2022-spring-final
	mv _build/latex/ds-2022-spring-final.pdf .

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
