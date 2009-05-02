#
# Geniwrapper XML-RPC and SOAP interfaces
#
#

import sys
import os
import traceback
import string
import xmlrpclib
from geni.util.auth import Auth
from geni.util.config import *
from geni.util.faults import *
from geni.util.debug import *
from geni.util.rights import *
from geni.util.credential import *
from geni.util.misc import *

# See "2.2 Characters" in the XML specification:
#
# #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD]
# avoiding
# [#x7F-#x84], [#x86-#x9F], [#xFDD0-#xFDDF]

invalid_xml_ascii = map(chr, range(0x0, 0x8) + [0xB, 0xC] + range(0xE, 0x1F))
xml_escape_table = string.maketrans("".join(invalid_xml_ascii), "?" * len(invalid_xml_ascii))

def xmlrpclib_escape(s, replace = string.replace):
    """
    xmlrpclib does not handle invalid 7-bit control characters. This
    function augments xmlrpclib.escape, which by default only replaces
    '&', '<', and '>' with entities.
    """

    # This is the standard xmlrpclib.escape function
    s = replace(s, "&", "&amp;")
    s = replace(s, "<", "&lt;")
    s = replace(s, ">", "&gt;",)

    # Replace invalid 7-bit control characters with '?'
    return s.translate(xml_escape_table)

def xmlrpclib_dump(self, value, write):
    """
    xmlrpclib cannot marshal instances of subclasses of built-in
    types. This function overrides xmlrpclib.Marshaller.__dump so that
    any value that is an instance of one of its acceptable types is
    marshalled as that type.

    xmlrpclib also cannot handle invalid 7-bit control characters. See
    above.
    """

    # Use our escape function
    args = [self, value, write]
    if isinstance(value, (str, unicode)):
        args.append(xmlrpclib_escape)

    try:
        # Try for an exact match first
        f = self.dispatch[type(value)]
    except KeyError:
        raise
        # Try for an isinstance() match
        for Type, f in self.dispatch.iteritems():
            if isinstance(value, Type):
                f(*args)
                return
        raise TypeError, "cannot marshal %s objects" % type(value)
    else:
        f(*args)

# You can't hide from me!
xmlrpclib.Marshaller._Marshaller__dump = xmlrpclib_dump

# SOAP support is optional
try:
    import SOAPpy
    from SOAPpy.Parser import parseSOAPRPC
    from SOAPpy.Types import faultType
    from SOAPpy.NS import NS
    from SOAPpy.SOAPBuilder import buildSOAP
except ImportError:
    SOAPpy = None


def import_deep(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class GeniAPI:

    # flat list of method names
    import geni.methods
    methods = geni.methods.all
    
    def __init__(self, config = "/etc/geni/geni_config", encoding = "utf-8", peer_cert = None, interface = None, key_file = None, cert_file = None):
        self.encoding = encoding

        # Better just be documenting the API
        if config is None:
            return

        # Load configuration
        self.config = Config(config)
        self.auth = Auth(peer_cert)
        self.interface = interface
        self.key_file = key_file
        self.cert_file = cert_file
        self.credential = None
        self.plshell = self.getPLCShell()
        self.basedir = self.config.GENI_BASE_DIR + os.sep
        self.server_basedir = self.basedir + os.sep + "geni" + os.sep
        self.hrn = self.config.GENI_INTERFACE_HRN
        self.time_format = "%Y-%m-%d %H:%M:%S"


    def getPLCShell(self):
        self.plauth = {'Username': self.config.GENI_PLC_USER,
                         'AuthMethod': 'password',
                         'AuthString': self.config.GENI_PLC_PASSWORD}
        try:
            import PLC.Shell
            shell = PLC.Shell.Shell(globals = globals())
            shell.AuthCheck(self.plauth)
            return shell
        except ImportError:
            # connect via xmlrpc
            plc_host = self.config.GENI_PLC_HOST
            plc_port = self.config.GENI_PLC_PORT
            plc_api_path = self.config.GENI_PLC_API_PATH
            url = "https://%(plc_host)s:%(plc_port)s/%(plc_api_path)s/" % \
                   locals()
             
            shell = xmlrpclib.Server(url, verbose = 0, allow_none = True)
            shell.AuthCheck(self.plauth)
            return shell

    def getCredential(self):
        if self.interface in ['registry']:
            return self.getCredentialFromLocalRegistry()
        else:
            return self.getCredentialFromRegistry()
    

    def getCredentialFromRegistry(self):
        """ 
        Get our credential from a remote registry using a geniclient connection
        """
        type = 'authority'
        cred_filename = ".".join([self.server_basedir, self.interface, self.hrn, type, "cred"])
        try:
            credential = Credential(filename = cred_filename)
            return credential
        except IOError:
            from geni.registry import Registries
            registries = Registries(self)
            registry = registries[self.hrn]
            self_cred = registry.get_credential(None, type, self.hrn)
            cred = registry.get_credential(self_cred, type, self.hrn)
            cred.save_to_file(cred_filename, save_parents=True)

    def getCredentialFromLocalRegistry(self):
        """
        Get our current credential directly from the local registry.
        """

        hrn = self.hrn
        auth_hrn = self.auth.get_authority(hrn)
        if not auth_hrn:
            auth_hrn = hrn
        auth_info = self.auth.get_auth_info(auth_hrn)
        table = self.auth.get_auth_table(auth_hrn)
        records = table.resolve('*', hrn)
        if not records:
            raise RecordnotFound
        record = records[0]
        type = record.get_type()
        object_gid = record.get_gid_object()
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(object_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_cred.set_pubkey(object_gid.get_pubkey())
        r1 = determine_rights(type, hrn)
        new_cred.set_privileges(r1)

        auth_kind = "authority,ma,sa"

        new_cred.set_parent(self.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))

        new_cred.encode()
        new_cred.sign()

        return new_cred
   

    def loadCredential(self):
        """
        Attempt to load credential from file if it exists. If it doesnt get
        credential from registry.
        """

        # see if this file exists
        # XX This is really the aggregate's credential. Using this is easier than getting
        # the registry's credential from iteslf (ssl errors).   
        ma_cred_filename = self.server_basedir + os.sep + self.interface + self.hrn + ".ma.cred"
        try:
            self.credential = Credential(filename = ma_cred_filename)
        except IOError:
            self.credential = self.getCredentialFromRegistry()

    ##
    # Convert geni fields to PLC fields for use when registering up updating
    # registry record in the PLC database
    #
    # @param type type of record (user, slice, ...)
    # @param hrn human readable name
    # @param geni_fields dictionary of geni fields
    # @param pl_fields dictionary of PLC fields (output)

    def geni_fields_to_pl_fields(self, type, hrn, geni_fields, pl_fields):
        if type == "user":
            if not "email" in pl_fields:
                if not "email" in geni_fields:
                    raise MissingGeniInfo("email")
                pl_fields["email"] = geni_fields["email"]

            if not "first_name" in pl_fields:
                pl_fields["first_name"] = "geni"

            if not "last_name" in pl_fields:
                pl_fields["last_name"] = hrn

        elif type == "slice":
            if not "instantiation" in pl_fields:
                pl_fields["instantiation"] = "delegated"  # "plc-instantiated"
            if not "name" in pl_fields:
                pl_fields["name"] = hrn_to_pl_slicename(hrn)
            if not "max_nodes" in pl_fields:
                pl_fields["max_nodes"] = 10

        elif type == "node":
            if not "hostname" in pl_fields:
                if not "dns" in geni_fields:
                    raise MissingGeniInfo("dns")
                pl_fields["hostname"] = geni_fields["dns"]
            if not "model" in pl_fields:
                pl_fields["model"] = "geni"

        elif type == "authority":
            pl_fields["login_base"] = hrn_to_pl_login_base(hrn)

            if not "name" in pl_fields:
                pl_fields["name"] = hrn

            if not "abbreviated_name" in pl_fields:
                pl_fields["abbreviated_name"] = hrn

            if not "enabled" in pl_fields:
                pl_fields["enabled"] = True

            if not "is_public" in pl_fields:
                pl_fields["is_public"] = True



    def fill_record_pl_info(self, record):
        """
        Fill in the planetlab specific fields of a Geni record. This
        involves calling the appropraite PLC method to retrie the 
        dtabase record for the object.
        
        PLC data is filled into the pl_fino field of the record.
    
        @param record record to fill in field (in/out param)     
        """
        type = record.get_type()
        pointer = record.get_pointer()
        auth_hrn = self.hrn
        login_base = ''
        # records with pointer==-1 do not have plc info associated with them.
        # for example, the top level authority records which are
        # authorities, but not PL "sites"
        if pointer == -1:
            record.set_pl_info({})
            return

        if (type in ["authority", "sa", "ma"]):
            pl_res = self.plshell.GetSites(self.plauth, [pointer])
        elif (type == "slice"):
            pl_res = self.plshell.GetSlices(self.plauth, [pointer])
        elif (type == "user"):
            pl_res = self.plshell.GetPersons(self.plauth, [pointer])
        elif (type == "node"):
            pl_res = self.plshell.GetNodes(self.plauth, [pointer])
        else:
            raise UnknownGeniType(type)
        
        if not pl_res:
            raise PlanetLabRecordDoesNotExist(record.get_name())

        # convert ids to hrns
        pl_record = pl_res[0]
        if 'site_id' in pl_record:
            sites = self.plshell.GetSites(self.plauth, pl_record['site_id'], ['login_base'])
            site = sites[0]
            login_base = site['login_base']
            pl_record['site'] = ".".join([auth_hrn, login_base])
        if 'person_ids' in pl_record:
            persons =  self.plshell.GetPersons(self.plauth, pl_record['person_ids'], ['email'])
            emails = [person['email'] for person in persons]
            usernames = [email.split('@')[0] for email in emails]
            person_hrns = [".".join([auth_hrn, login_base, username]) for username in usernames]
            pl_record['persons'] = person_hrns 
        if 'slice_ids' in pl_record:
            slices = self.plshell.GetSlices(self.plauth, pl_record['slice_ids'], ['name'])
            slicenames = [slice['name'] for slice in slices]
            slice_hrns = [slicename_to_hrn(auth_hrn, slicename) for slicename in slicenames]
            pl_record['slices'] = slice_hrns
        if 'node_ids' in pl_record:
            nodes = self.plshell.GetNodes(self.plauth, pl_record['node_ids'], ['hostname'])
            hostnames = [node['hostname'] for node in nodes]
            node_hrns = [hostname_to_hrn(auth_hrn, login_base, hostname) for hostname in hostnames]
            pl_record['nodes'] = node_hrns
        if 'site_ids' in pl_record:
            sites = self.plshell.GetSites(self.plauth, pl_record['site_ids'], ['login_base'])
            login_bases = [site['login_base'] for site in sites]
            site_hrns = [".".join([auth_hrn, lbase]) for lbase in login_bases]
            pl_record['sites'] = site_hrns
        if 'key_ids' in pl_record:
            keys = self.plshell.GetKeys(self.plauth, pl_record['key_ids'])
            pubkeys = []
            if keys:
                pubkeys = [key['key'] for key in keys]
            pl_record['keys'] = pubkeys     

        record.set_pl_info(pl_record)


    def lookup_users(self, auth_table, user_id_list, role="*"):
        record_list = []
        for person_id in user_id_list:
            user_records = auth_table.find("user", person_id, "pointer")
            for user_record in user_records:
                self.fill_record_info(user_record)

                user_roles = user_record.get_pl_info().get("roles")
                if (role=="*") or (role in user_roles):
                    record_list.append(user_record.get_name())
        return record_list

    def fill_record_geni_info(self, record):
        geni_info = {}
        type = record.get_type()

        if (type == "slice"):
            auth_table = self.auth.get_auth_table(self.auth.get_authority(record.get_name()))
            person_ids = record.pl_info.get("person_ids", [])
            researchers = self.lookup_users(auth_table, person_ids)
            geni_info['researcher'] = researchers

        elif (type == "authority"):
            auth_table = self.auth.get_auth_table(record.get_name())
            person_ids = record.pl_info.get("person_ids", [])
            pis = self.lookup_users(auth_table, person_ids, "pi")
            operators = self.lookup_users(auth_table, person_ids, "tech")
            owners = self.lookup_users(auth_table, person_ids, "admin")
            geni_info['pi'] = pis
            geni_info['operator'] = operators
            geni_info['owner'] = owners
            # TODO: OrganizationName

        elif (type == "node"):
            geni_info['dns'] = record.pl_info.get("hostname", "")
            # TODO: URI, LatLong, IP, DNS
    
        elif (type == "user"):
            geni_info['email'] = record.pl_info.get("email", "")
            # TODO: PostalAddress, Phone

        record.set_geni_info(geni_info)

    def fill_record_info(self, record):
        """
        Given a geni record, fill in the PLC specific and Geni specific
        fields in the record. 
        """
        self.fill_record_pl_info(record)
        self.fill_record_geni_info(record)

    def update_membership_list(self, oldRecord, record, listName, addFunc, delFunc):
        # get a list of the HRNs tht are members of the old and new records^M
        if oldRecord:
            if oldRecord.pl_info == None:
                oldRecord.pl_info = {}
            oldList = oldRecord.get_geni_info().get(listName, [])
        else:
            oldList = []
        newList = record.get_geni_info().get(listName, [])

        # if the lists are the same, then we don't have to update anything
        if (oldList == newList):
            return

        # build a list of the new person ids, by looking up each person to get
        # their pointer
        newIdList = []
        for hrn in newList:
            auth_hrn = self.auth.get_authority(hrn)
            if not auth_hrn:
                auth_hrn = hrn
            auth_info = self.auth.get_auth_info(auth_hrn)
            table = self.auth.get_auth_table(auth_hrn)
            records = table.resolve('user', hrn)
            if records:
                userRecord = records[0]    
                newIdList.append(userRecord.get_pointer())

        # build a list of the old person ids from the person_ids field of the
        # pl_info
        if oldRecord:
            oldIdList = oldRecord.pl_info.get("person_ids", [])
            containerId = oldRecord.get_pointer()
        else:
            # if oldRecord==None, then we are doing a Register, instead of an
            # update.
            oldIdList = []
            containerId = record.get_pointer()

    # add people who are in the new list, but not the oldList
        for personId in newIdList:
            if not (personId in oldIdList):
                print "adding id", personId, "to", record.get_name()
                addFunc(self.plauth, personId, containerId)

        # remove people who are in the old list, but not the new list
        for personId in oldIdList:
            if not (personId in newIdList):
                print "removing id", personId, "from", record.get_name()
                delFunc(self.plauth, personId, containerId)

    def update_membership(self, oldRecord, record):
        if record.type == "slice":
            self.update_membership_list(oldRecord, record, 'researcher',
                                        self.plshell.AddPersonToSlice,
                                        self.plshell.DeletePersonFromSlice)
        elif record.type == "authority":
            # TODO
            pass


    def callable(self, method):
        """
        Return a new instance of the specified method.
        """
        # Look up method
        if method not in self.methods:
            raise GeniInvalidAPIMethod, method
        
        # Get new instance of method
        try:
            classname = method.split(".")[-1]
            module = __import__("geni.methods." + method, globals(), locals(), [classname])
            callablemethod = getattr(module, classname)(self)
            return getattr(module, classname)(self)
        except ImportError, AttributeError:
            raise
            raise GeniInvalidAPIMethod, method

    def call(self, source, method, *args):
        """
        Call the named method from the specified source with the
        specified arguments.
        """
        function = self.callable(method)
        function.source = source
        return function(*args)

    def handle(self, source, data):
        """
        Handle an XML-RPC or SOAP request from the specified source.
        """

        # Parse request into method name and arguments
        try:
            interface = xmlrpclib
            (args, method) = xmlrpclib.loads(data)
            methodresponse = True
        except Exception, e:
            if SOAPpy is not None:
                interface = SOAPpy
                (r, header, body, attrs) = parseSOAPRPC(data, header = 1, body = 1, attrs = 1)
                method = r._name
                args = r._aslist()
                # XXX Support named arguments
            else:
                raise e

        try:
            result = self.call(source, method, *args)
        except Exception, fault:
            traceback.print_exc(file = log)
            # Handle expected faults
            if interface == xmlrpclib:
                result = fault
                methodresponse = None
            elif interface == SOAPpy:
                result = faultParameter(NS.ENV_T + ":Server", "Method Failed", method)
                result._setDetail("Fault %d: %s" % (fault.faultCode, fault.faultString))

        # Return result
        if interface == xmlrpclib:
            if not isinstance(result, GeniFault):
                result = (result,)

            data = xmlrpclib.dumps(result, methodresponse = True, encoding = self.encoding, allow_none = 1)
        elif interface == SOAPpy:
            data = buildSOAP(kw = {'%sResponse' % method: {'Result': result}}, encoding = self.encoding)

        return data
