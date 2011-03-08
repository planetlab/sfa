# recompute the SFA graphs from different locations

BUNDLES += http://planet-lab.eu:12346/@auto-ple-am
BUNDLES += http://planet-lab.eu:12345/@auto-ple-reg 
BUNDLES += http://planet-lab.eu:12347/@auto-ple-sa
BUNDLES += http://planet-lab.org:12345/@auto-plc-reg 
BUNDLES += http://planet-lab.org:12347/@auto-plc-sa
BUNDLES += http://planet-lab.kr:12345/@auto-ppk-reg 
BUNDLES += http://planet-lab.kr:12347/@auto-ppk-sa
BUNDLES += http://geni-myvini.umkc.gpeni.net:12345/@auto-gpeni-reg
BUNDLES += http://geni-myvini.umkc.gpeni.net:12347/@auto-gpeni-sa
BUNDLES += http://198.248.241.100:12345/@auto-glc-reg
BUNDLES += http://198.248.241.100:12347/@auto-glc-sa
BUNDLES += http://vini-veritas.net:12345/@auto-vini-reg
BUNDLES += http://vini-veritas.net:12347/@auto-vini-sa
BUNDLES += http://www.planet-lab.jp:12345/@auto-plj-reg 
BUNDLES += http://www.planet-lab.jp:12347/@auto-plj-sa
BUNDLES += http://www.emanicslab.org:12345/@auto-elc-reg 
BUNDLES += http://www.emanicslab.org:12347/@auto-elc-sa

# dont output svg yet
#EXTENSIONS := png svg
EXTENSIONS := png 

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
	-./sfi.py -s $(word 1,$(subst @, ,$(1))) version >& $$@
endef

VERSIONS := $(foreach bundle,$(BUNDLES),$(word 2,$(subst @, ,$(bundle))).version)

versions: $(VERSIONS)
clean-versions: 
	rm -f $(VERSIONS)

# the actual targets
$(foreach bundle,$(BUNDLES),$(eval $(call bundle_version_target,$(bundle))))

clean:
	rm -f auto-*.{out,version}
	$(foreach extension,$(EXTENSIONS),rm -rf auto-*.$(extension);)

#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
