# attempt to update at build-time

INTERFACES=sfa registry slice-manager aggregate

WSDLS = $(foreach interface,$(INTERFACES),$(interface).wsdl)
HTMLS = $(foreach interface,$(INTERFACES),$(interface).html)

all: $(WSDLS) $(HTMLS)

# temporary: turn off wsdl generation as it is failing
#TEMPORARY_OFF = yes

ifdef TEMPORARY_OFF
registry.wsdl slice-manager.wsdl aggregate.wsdl sfa.wsdl:
	touch $@
else
registry.wsdl: sfa2wsdl.py
	PYTHONPATH=../ ./sfa2wsdl.py --registry > $@

slice-manager.wsdl: sfa2wsdl.py
	PYTHONPATH=../ ./sfa2wsdl.py --slice-manager > $@

aggregate.wsdl: sfa2wsdl.py
	PYTHONPATH=../ ./sfa2wsdl.py --aggregate > $@

sfa.wsdl: sfa2wsdl.py
	PYTHONPATH=../ ./sfa2wsdl.py --registry --slice-manager --aggregate > $@
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
clean::
	rm -f $(WSDLS)

install-clean:
	rm -f $(INSTALLED)

.PHONY: all clean install install-clean

#################### generate html document
%.html: %.wsdl wsdl2html.xsl
	xsltproc $(XSLTFLAGS) wsdl2html.xsl $*.wsdl > $@ || rm $@

clean::
	rm -f $(HTMLS)


backup:
	$(foreach wsdl,$(WSDLS), cp $(wsdl) $(wsdl).bak;)
	$(foreach html,$(HTMLS), cp $(html) $(html).bak;)

diff:
	$(foreach wsdl,$(WSDLS), diff $(wsdl) $(wsdl).bak;)
	$(foreach html,$(HTMLS), diff $(html) $(html).bak;)
