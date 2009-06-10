#
## (Re)builds Python metafile (__init__.py) and documentation
# 
# overwritten by the specfile
DESTDIR="/"

init := geni/__init__.py geni/util/__init__.py geni/methods/__init__.py 
subdirs := keyconvert #pyOpenSSL-0.9

all: install

install: $(init) $(subdirs) install-python

install-python:
	python setup.py install --root=$(DESTDIR) --record=GENI_INSTALLED_FILES

$(subdirs): $(init)

$(subdirs): %:
	$(MAKE) -C $@

clean:
	python setup.py clean
	for i in $(subdirs); do make -C $$i clean ; done

index: $(init)

index-clean:
	rm $(init)

.phony: all install install-python force clean index $(subdirs)

force:

# are the .java files used ?
tags:	
	find . -name '*.py' -o -name '*.sh' -o -name '*.ecore'  | grep -v '/\.svn/' | xargs etags



########## indexes
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

########## sync
# 2 forms are supported
# (*) if your plc root context has direct ssh access:
# make sync PLC=private.one-lab.org
# (*) otherwise, entering through the root context
# make sync PLCHOST=testbox1.inria.fr GUEST=vplc03.inria.fr

ifdef GUEST
ifdef PLCHOST
SSHURL:=root@$(PLCHOST):/vservers/$(GUEST)
SSHCOMMAND:=ssh root@$(PLCHOST) vserver $(GUEST)
endif
endif
ifdef PLC
SSHURL:=root@$(PLC):/
SSHCOMMAND:=ssh root@$(PLC)
endif

LOCAL_RSYNC_EXCLUDES	:= --exclude '*.pyc' 
RSYNC_EXCLUDES		:= --exclude .svn --exclude CVS --exclude '*~' --exclude TAGS $(LOCAL_RSYNC_EXCLUDES)
RSYNC_COND_DRY_RUN	:= $(if $(findstring n,$(MAKEFLAGS)),--dry-run,)
RSYNC			:= rsync -a -v $(RSYNC_COND_DRY_RUN) $(RSYNC_EXCLUDES)

sync:
ifeq (,$(SSHURL))
	@echo "sync: You must define, either PLC, or PLCHOST & GUEST, on the command line"
	@echo "  e.g. make sync PLC=private.one-lab.org"
	@echo "  or   make sync PLCHOST=testbox1.inria.fr GUEST=vplc03.inria.fr"
	@exit 1
else
	+$(RSYNC) ./geni/ $(SSHURL)/usr/lib/python2.5/site-packages/geni/
	+$(RSYNC) geni-config-tty $(SSHURL)/usr/bin
endif

