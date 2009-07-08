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

clean:
	rm -f *wsdl

.PHONY: all clean
