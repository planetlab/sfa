from pprint import pprint

from sfa.util.client import *
from sfa.trust.credential import *

cred = Credential(filename = 'tmack.pl.sa.cred')
slicehrn = 'planetlab.us.pl.tmack'
print cred.get_privileges().save_to_string()

r = GeniClient('https://128.112.139.120:12345', 'tmack.pkey', 'tmack.cert') 
a = GeniClient('https://128.112.139.120:12346', 'tmack.pkey', 'tmack.cert')

#pprint(r.list(cred, 'planetlab.us.princeton'))
pprint(a.get_policy(cred))

print "components at this aggregate"
components = a.list_components()
pprint(components)

print "resources being used by %(slicehrn)s" % locals()
tmack_components = a.list_resources(cred, slicehrn)
pprint(tmack_components)

#print "removing %(slicehrn)s from all nodes" % locals()
#a.DeleteSliver(cred, slicehrn)

print "adding %(slicehrn)s back to its original nodes" % locals()
a.list_resources(cred, slicehrn)
a.CreateSliver(cred, slicehrn, components)
a.list_resources(cred, slicehrn)

 
