#
## (Re)builds Python metafile (__init__.py) and documentation
# 
# overwritten by the specfile
DESTDIR="/"

##########
all: keyconvert python wsdl

install: keyconvert-install python-install wsdl-install

clean: keyconvert-clean python-clean wsdl-clean

.PHONY: all install clean 

##########
keyconvert:
	$(MAKE) -C keyconvert

keyconvert-install:
	$(MAKE) -C keyconvert install

keyconvert-clean:
	$(MAKE) -C keyconvert clean

.PHONY: keyconvert keyconvert-install keyconvert-clean 

##########
python: 

python-install:
	python setup.py install --root=$(DESTDIR)
	chmod 444 $(DESTDIR)/etc/sfa/default_config.xml

python-clean:
	python setup.py clean
	rm $(init)

.PHONY: python python-install python-clean
##########
wsdl: 
	$(MAKE) -C wsdl 

# propagate DESTDIR from the specfile
wsdl-install:
	$(MAKE) -C wsdl install 

wsdl-clean:
	$(MAKE) -C wsdl clean

.PHONY: wsdl wsdl-install wsdl-clean
##########

# are the .java files used ?
tags:	
	find . -type f | egrep -v '/\.svn/|TAGS|\.py[co]$$|\.doc$$|\.html$$|\.pdf$$' | xargs etags
.PHONY: tags


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

BINS =	./config/sfa-config-tty ./sfa/plc/sfa-import-plc.py ./sfa/plc/sfa-nuke-plc.py \
	./sfa/server/sfa-server.py \
	./sfa/client/sfi.py ./sfa/client/getNodes.py ./sfa/client/getRecord.py \
	./sfa/client/setRecord.py ./sfa/client/genidump.py

sync:
ifeq (,$(SSHURL))
	@echo "sync: You must define, either PLC, or PLCHOST & GUEST, on the command line"
	@echo "  e.g. make sync PLC=private.one-lab.org"
	@echo "  or   make sync PLCHOST=testbox1.inria.fr GUEST=vplc03.inria.fr"
	@exit 1
else
	+$(RSYNC) ./sfa/ $(SSHURL)/usr/lib/python2.5/site-packages/sfa/
	+$(RSYNC)  $(BINS) $(SSHURL)/usr/bin
	$(SSHCOMMAND) exec service sfa restart
endif

.PHONY: sync
##########
