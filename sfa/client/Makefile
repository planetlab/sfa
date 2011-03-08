BUNDLES += http://planet-lab.eu:12345/@sfa-ple-reg 
BUNDLES += http://planet-lab.eu:12346/@sfa-ple-am
BUNDLES += http://planet-lab.eu:12347/@sfa-ple-sa
BUNDLES += http://planet-lab.org:12345/@sfa-plc-reg 
BUNDLES += http://planet-lab.org:12346/@sfa-plc-am
BUNDLES += http://planet-lab.org:12347/@sfa-plc-sa
BUNDLES += http://planet-lab.kr:12345/@sfa-ppk-reg 
BUNDLES += http://planet-lab.kr:12346/@sfa-ppk-am
BUNDLES += http://planet-lab.kr:12347/@sfa-ppk-sa
BUNDLES += http://planet-lab.jp:12345/@sfa-plj-reg 
BUNDLES += http://planet-lab.jp:12346/@sfa-plj-am
BUNDLES += http://planet-lab.jp:12347/@sfa-plj-sa
BUNDLES += http://geni-myvini.umkc.gpeni.net:12345/@sfa-gpeni-reg
BUNDLES += http://geni-myvini.umkc.gpeni.net:12346/@sfa-gpeni-am
BUNDLES += http://geni-myvini.umkc.gpeni.net:12347/@sfa-gpeni-sa
BUNDLES += http://198.248.241.100:12345/@sfa-glc-reg
BUNDLES += http://198.248.241.100:12346/@sfa-glc-am
BUNDLES += http://198.248.241.100:12347/@sfa-glc-sa

EXTENSIONS := png svg

define bundle_scan_target
$(word 2,$(subst @, ,$(1))):
	./sfascan.py -e $(word 1,$(subst @, ,$(1))) $(foreach extension,$(EXTENSIONS),-o $(word 2,$(subst @, ,$(1))).$(extension)) >& $(word 2,$(subst @, ,$(1))).out
.PHONY: $(word 2,$(subst @, ,$(1)))
endef

ALL := $(foreach bundle,$(BUNDLES),$(word 2,$(subst @, ,$(bundle))))

all: $(ALL)

# the actual targets
$(foreach bundle,$(BUNDLES),$(eval $(call bundle_scan_target,$(bundle))))

####################

define bundle_version_target
$(word 2,$(subst @, ,$(1))).version:
	./sfi.py -s $(word 1,$(subst @, ,$(1))) version >& $$@
endef

VERSIONS := $(foreach bundle,$(BUNDLES),$(word 2,$(subst @, ,$(bundle))).version)

versions: $(VERSIONS)
clean-versions: 
	rm -f $(VERSIONS)

# the actual targets
$(foreach bundle,$(BUNDLES),$(eval $(call bundle_version_target,$(bundle))))


#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
