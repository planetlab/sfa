# remoteshell.py
#
# interface to the PLC api via xmlrpc
#
# RemoteShell() exports an API that looks identical to that exported by
# PLC.Shell.Shell(). It's meant to be a drop in replacement for running
# geniwrapper on a different machine than PLC.

import xmlrpclib

class RemoteShell:
    def __init__(self):
        self.servers = {}

    def get_default_opts(self):
        dict = {}
        dict['Role'] = "user"
        dict['Url'] = "https://www.planet-lab.org:443/PLCAPI/"
        return dict

    def call(self, name, pl_auth, *args):
        auth_opts = self.get_default_opts().copy()
        auth_opts.update(pl_auth)

        url = auth_opts["Url"]
        key = url + "#" + auth_opts["Username"]

        if not (key in self.servers):
            server = xmlrpclib.Server(url, verbose = 0, allow_none=True)
            server.AdmAuthCheck(auth_opts)
            self.servers[key] = server

        server = self.servers[key]

        arglist = ["auth_opts"]
        for arg in args:
            arglist.append(repr(arg))

        result = eval("server." + name + "(" + ",".join(arglist) + ")")

        return result

    # TODO: there's probably an automatic way to import all these stubs

    def AddInitScript(self, pl_auth, *args):
        return self.call("AddInitScript", pl_auth, *args)

    def AddNode(self, pl_auth, *args):
        return self.call("AddNode", pl_auth, *args)

    def AddPerson(self, pl_auth, *args):
        return self.call("AddPerson", pl_auth, *args)

    def AddSite(self, pl_auth, *args):
        return self.call("AddSite", pl_auth, *args)

    def AddSlice(self, pl_auth, *args):
        return self.call("AddSlice", pl_auth, *args)

    def DeleteNode(self, pl_auth, *args):
        return self.call("DeleteNode", pl_auth, *args)

    def DeletePerson(self, pl_auth, *args):
        return self.call("DeletePerson", pl_auth, *args)

    def DeleteSite(self, pl_auth, *args):
        return self.call("DeleteSite", pl_auth, *args)

    def DeleteSlice(self, pl_auth, *args):
        return self.call("DeleteSlice", pl_auth, *args)

    def GetInitScripts(self, pl_auth, *args):
        return self.call("GetInitScripts", pl_auth, *args)

    def GetKeys(self, pl_auth, *args):
        return self.call("GetKeys", pl_auth, *args)

    def GetNodes(self, pl_auth, *args):
        return self.call("GetNodes", pl_auth, *args)

    def GetPersons(self, pl_auth, *args):
        return self.call("GetPersons", pl_auth, *args)

    def GetSites(self, pl_auth, *args):
        return self.call("GetSites", pl_auth, *args)

    def GetSliceAttributes(self, pl_auth, *args):
        return self.call("GetSliceAttributes", pl_auth, *args)

    def GetSlices(self, pl_auth, *args):
        return self.call("GetSlices", pl_auth, *args)

    def UpdateNode(self, pl_auth, *args):
        return self.call("UpdateNode", pl_auth, *args)

    def UpdatePerson(self, pl_auth, *args):
        return self.call("UpdatePerson", pl_auth, *args)

    def UpdateSite(self, pl_auth, *args):
        return self.call("UpdateSite", pl_auth, *args)

    def UpdateSlice(self, pl_auth, *args):
        return self.call("UpdateSlice", pl_auth, *args)


