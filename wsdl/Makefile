# attempt to update at build-time
SFA := sfa.wsdl
ALL := $(SFA) registry.wsdl slice-manager.wsdl aggregate.wsdl 

all: $(SFA)

# create missing __init__.py files
../sfa/__init__.py:
	make -C .. index

registry.wsdl: ../sfa/__init__.py
	PYTHONPATH=../ ./gw2wsdl.py --registry > $@

slice-manager.wsdl: ../sfa/__init__.py
	PYTHONPATH=../ ./gw2wsdl.py --slice-manager > $@

aggregate.wsdl: ../sfa/__init__.py
	PYTHONPATH=../ ./gw2wsdl.py --aggregate > $@

sfa.wsdl: ../sfa/__init__.py
	PYTHONPATH=../ ./gw2wsdl.py --registry --slice-manager --aggregate > $@

clean:
	rm -f *wsdl
