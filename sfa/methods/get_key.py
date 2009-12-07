### $Id:  $
### $URL:  $
import os
import tempfile
import commands
from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.auth import Auth
from sfa.util.genitable import *

class get_key(Method):
    """
    Generate a new keypair and gid for requesting caller (component).     
    @return 1 If successful  
    """

    interfaces = ['registry']
    
    accepts = []

    returns = Parameter(int, "1 if successful, faults otherwise")
    
    def call(self):
        # verify that the callers's ip address exist in the db and is an inteface
        # for a node in the db
        (ip, port) = self.api.remote_addr
        interfaces = self.api.plshell.GetInterfaces(self.api.plauth, {'ip': ip}, ['node_id'])
        if not interfaces:
            raise NonExistingRecord("no such ip %(ip)s" % locals())
        nodes = self.api.plshell.GetNodes(self.api.plauth, [interfaces[0]['node_id']], ['node_id', 'hostname'])
        if not nodes:
            raise NonExistingRecord("no such node using ip %(ip)s" % locals())
        node = nodes[0]
       
        # look up the sfa record
        table = GeniTable()
        records = table.find({'type': 'node', 'pointer': node['node_id']})
        if not records:
            raise RecordNotFound("pointer:" + str(node['node_id']))  
        record = records[0]
        
        # generate a new keypair and gid
        uuid = create_uuid()
        pkey = Keypair(create=True)
        gid_object = self.api.auth.hierarchy.create_gid(record['hrn'], uuid, pkey)
        gid = gid_object.save_to_string(save_parents=True)
        record['gid'] = gid
        record.set_gid(gid)

        # update the record
        table.update(record)
  
        # attempt the scp the key
        # this will only work for planetlab based compoenents
        (fd, filename) = tempfile.mkstemp() 
        pkey.save_to_file(filename)
        host = node['hostname']
        dest="/etc/sfa/nodekey.key" 
        identity = "/etc/planetlab/root_ssh_key.pub"
        scp_command = "scp -i %(identity)s %(filename)s root@%(host)s:%(dest)s" % locals()
        (status, output) = commands(scp_command)
        if status:
            raise Exception, output
        os.unlink(filename)

        return 1 
