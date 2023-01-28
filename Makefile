# Makefile front-end for rust dev works.
VERSION		= 1.0
RELEASE		= 2
DATE		= $(shell date)
NEWRELEASE	= $(shell echo $$(($(RELEASE) + 1)))
PROJECT_NAME    = rexpect-examples
TOPDIR = $(shell pwd)
MANPAGES = 
A2PS2S1C  = /bin/a2ps --sides=2 --medium=Letter --columns=1 --portrait --line-numbers=1 --font-size=8
A2PSTMP   = ./tmp
DOCS      = ./docs

SHELL := /bin/bash

.PHONY: all sqlite rpm

all: help
#https://stackoverflow.com/questions/6273608/how-to-pass-argument-to-makefile-from-command-line
args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`
%:
	@:

versionfile:
	echo "version:" $(VERSION) > etc/version
	echo "release:" $(RELEASE) >> etc/version
	echo "source build date:" $(DATE) >> etc/version

manpage:
	for manpage in $(MANPAGES); do (pod2man --center=$$manpage --release="" ./docs/$$manpage.pod > ./docs/$$manpage.1); done

clean: cleantmp
	-rm -rf *~ *.lock
	-rm -rf docs/*.1
	-find . -type f -name *~  -exec rm -f {} \;
	-find . -type d -name target -exec rm -rf {} \;

clean_hard:
	-rm -rf $(shell $(PYTHON) -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")/adagios 


clean_hardest: clean_rpms


#Ref: https://stackoverflow.com/questions/1490949/how-to-write-loop-in-a-makefile
# MANIFEST  
SRC1= Makefile 
SRC2= 
#SRC2= manage.py profiles_projects-dir-layout.txt

cleantmp:
	rm -f ${A2PSTMP}/*.ps ${A2PSTMP}/*.pdf	
.ps: cleantmp
	$(foreach var, $(SRC1), ${A2PS2S1C} $(var) --output=${A2PSTMP}/$(var).ps ;)
	$(foreach var, $(SRC2), ${A2PS2S1C} $(var) --output=${A2PSTMP}/$(var).ps ;)
	touch .ps

allpdf: .pdf
	make -C profiles_api pdf
	make -C profiles_project pdf
	touch .pdf

.pdf: .ps
	$(foreach var, $(SRC1), (cd ${A2PSTMP};ps2pdf $(var).ps $(var).pdf);)
	$(foreach var, $(SRC2), (cd ${A2PSTMP};ps2pdf $(var).ps $(var).pdf);)
	rm -f ${A2PSTMP}/*.ps
	cp ${A2PSTMP}/*.pdf  ${DOCS}/
	touch .pdf
tree: clean
	tree -L 4 > ${PROJECT_NAME}-dir-layout.txt

test:
	(cargo test)

# enable makefile to accept argument after command
#https://stackoverflow.com/questions/6273608/how-to-pass-argument-to-makefile-from-command-line

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`
%:
	@:

status:
	git status
commit:
	git commit -am "$(call args, Automated commit message without details, Please read the git diff)"  && git push
pull:
	git pull
help:
	@echo "Usage: make <target> <argument>"
	@echo
	@echo "Available targets are:"
	@echo "  sqlite                 bind to sqlite DB"
	@echo "  build                  call up cargo build"
	@echo "  help                   Showing this help "
	@echo "  clean                  clean all artifact files"
	@echo "  commit {"my message"}  ie, git commit, without or with real commit message"
	@echo "  status                 ie, git status"
	@echo "  pull                   ie, git pull"
	@echo ""

check:
	rpm -q liboping-devel

.PHONY: examples build check

build:
	(cargo build)

_FEATURES4 = 
_DEBUG4 = target/debug/examples

cargo-example:
	cargo build ${_FEATURES4} --example cargo-example && ${_DEBUG4}/cargo-example --help
examples: cargo-example
	cargo build ${_FEATURES4} --example cargo-example-derive && ${_DEBUG4}/cargo-example-derive --help
	cargo build ${_FEATURES4} --example demo && ${_DEBUG4}/demo --help
	cargo build ${_FEATURES4} --example find && ${_DEBUG4}/find --help
	cargo build ${_FEATURES4} --example pacman && ${_DEBUG4}/pacman --help
	cargo build ${_FEATURES4} --example git && ${_DEBUG4}/git --help
	cargo build ${_FEATURES4} --example repl && ls -l ${_DEBUG4}/repl
	cargo build ${_FEATURES4} --example typed-derive && ${_DEBUG4}/typed-derive --help
	cargo build ${_FEATURES4} --example escaped-positional-derive && ${_DEBUG4}/escaped-positional-derive  --help
	cargo build ${_FEATURES4} --example escaped-positional && ${_DEBUG4}/escaped-positional --help
	cargo build ${_FEATURES4} --example multicall-hostname && ${_DEBUG4}/multicall-hostname --help
	cargo build ${_FEATURES4} --example multicall-busybox && ${_DEBUG4}/multicall-busybox  --help

sqlite:
	time cargo build --release --features sqlite
	strip -s target/release/vaultwarden
rpm:
	time cargo generate-rpm
	ls -l target/generate-rpm/vaultwarden*.rpm
	rpm -qlp target/generate-rpm/vaultwarden*.rpm 
