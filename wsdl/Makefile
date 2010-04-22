# attempt to update at build-time

WSDLS = sfa.wsdl registry.wsdl slice-manager.wsdl aggregate.wsdl 

all: $(WSDLS)

# temporary: turn off wsdl generation as it is failing
#TEMPORARY_OFF = yes

ifdef TEMPORARY_OFF
registry.wsdl slice-manager.wsdl aggregate.wsdl sfa.wsdl:
	touch $@
else
registry.wsdl:
	PYTHONPATH=../ python sfa2wsdl.py --registry > $@

slice-manager.wsdl:
	PYTHONPATH=../ python sfa2wsdl.py --slice-manager > $@

aggregate.wsdl:
	PYTHONPATH=../ python sfa2wsdl.py --aggregate > $@

sfa.wsdl:
	PYTHONPATH=../ python sfa2wsdl.py --registry --slice-manager --aggregate > $@
endif

#################### install
# DESTDIR set but the calling Makefile in ../
INSTALL_PATH=/var/www/html/wsdl
INSTALLED=$(foreach wsdl,$(WSDLS),$(DESTDIR)$(INSTALL_PATH)/$(wsdl))

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

