#
## (Re)builds Python metafile (__init__.py) and documentation
#
# 
# Meta
DESTDIR="/"
init := geni/__init__.py geni/util/__init__.py geni/methods/__init__.py 

subdirs := keyconvert #pyOpenSSL-0.9

all: $(init) $(subdirs)

install: all
	python setup.py install --root=$(DESTDIR) --record=GENI_INSTALLED_FILES

$(subdirs): $(init)

$(subdirs): %:
	$(MAKE) -C $@

clean:
	python setup.py clean
	cd keyconvert && make clean

index: $(init)

index-clean:
	rm $(init)

.phony: all install force clean index $(subdirs)

geni/__init__.py:
	(echo '## Please use make index to update this file' ; echo 'all = """' ; cd geni; ls -1 *.py | grep -v __init__ | sed -e 's,.py$$,,' ; echo '""".split()') > $@

geni/methods/__init__.py:
	(echo '## Please use make index to update this file' ; echo 'all = """' ; cd geni/methods; ls -1 *.py | grep -v __init__ | sed -e 's,.py$$,,' ; echo '""".split()') > $@

geni/util/__init__.py:
	(echo '## Please use make index to update this file' ; echo 'all = """' ; cd geni/util; ls -1 *.py | grep -v __init__ | sed -e 's,.py$$,,' ; echo '""".split()') > $@

geni_now := $(sort $(shell fgrep -v '"' geni/__init__.py 2>/dev/null))
# what should be declared
geni_paths := $(filter-out %/__init__.py, $(wildcard geni/*.py))
geni_files := $(sort $(notdir $(geni_paths:.py=)))
ifneq ($(geni_now), $(geni_files))
geni/__init__.py: force
endif

methods_now := $(sort $(shell fgrep -v '"' geni/methods/__init__.py 2>/dev/null))
# what should be declared
method_paths := $(filter-out %/__init__.py, $(wildcard geni/methods/*.py))
method_files := $(sort $(notdir $(method_paths:.py=)))
ifneq ($(methods_now), $(methods_files))
geni/methods/__init__.py: force
endif

util_now := $(sort $(shell fgrep -v '"' geni/util/__init__.py 2>/dev/null))
# what should be declared
util_paths := $(filter-out %/__init__.py, $(wildcard geni/util/*.py))
util_files := $(sort $(notdir $(util_paths:.py=)))
ifneq ($(util_now), $(util_files))
geni/util/__init__.py: force
endif

force:

.PHONY: all install force clean index tags $(subdirs)
