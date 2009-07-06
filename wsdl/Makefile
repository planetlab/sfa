# attempt to update at build-time
SFA := sfa.wsdl
ALL := $(SFA) registry.wsdl slice-manager.wsdl aggregate.wsdl 

all: $(SFA)

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
