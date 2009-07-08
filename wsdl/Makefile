# attempt to update at build-time

ALL := sfa.wsdl registry.wsdl slice-manager.wsdl aggregate.wsdl 

all: $(ALL)

registry.wsdl:
	PYTHONPATH=../ ./gw2wsdl.py --registry > $@

slice-manager.wsdl:
	PYTHONPATH=../ ./gw2wsdl.py --slice-manager > $@

aggregate.wsdl:
	PYTHONPATH=../ ./gw2wsdl.py --aggregate > $@

sfa.wsdl:
	PYTHONPATH=../ ./gw2wsdl.py --registry --slice-manager --aggregate > $@

#################### install
# DESTDIR set but the calling Makefile in ../
INSTALL_PATH=/var/www/html/wsdl
INSTALLED=$(foreach wsdl,$(ALL),$(DESTDIR)$(INSTALL_PATH)/$(wsdl))

foo:
	@echo INSTALLED=$(INSTALLED)

install: $(INSTALLED)

$(DESTDIR)$(INSTALL_PATH):
	install -d -m 0755 $(DESTDIR)$(INSTALL_PATH)

$(DESTDIR)$(INSTALL_PATH)/%: wsdl=$(notdir $@)
$(DESTDIR)$(INSTALL_PATH)/%: $(DESTDIR)$(INSTALL_PATH) %
	install -c -m 0755 $(wsdl) $@

#################### clean
clean:
	rm -f *wsdl

install-clean:
	rm -f $(INSTALLED)

.PHONY: all clean install install-clean

