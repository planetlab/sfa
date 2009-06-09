#!/usr/bin/python
#
# Sapan Bhatia <sapanb@cs.princeton.edu>
#
# Generates a WSDL for geniwrapper
# Current limitations:
# - Invalid for the following reasons 
# - The types are python types, not WSDL types

import os, sys
import time
import pdb
import xml.dom.minidom
import xml.dom.ext
import globals
import apistub

from geni.util.auth import Auth
from geni.util.parameter import Parameter,Mixed,python_type,xmlrpc_type


try:
    set
except NameError:
    from sets import Set
    set = Set

# Class functions

def param_type(param):

#     if isinstance(param, Mixed) and len(param):
#         subtypes = [param_type(subparam) for subparam in param]
#         return " or ".join(subtypes)
#     elif isinstance(param, (list, tuple, set)) and len(param):
#         return "array of " + " or ".join([param_type(subparam) for subparam in param])
#     else:
#         return xmlrpc_type(python_type(param))
    return "some type - todo"


def add_wsdl_ports_and_bindings (wsdl):
    for method in apistub.methods:
        # Skip system. methods
        if "system." in method:
            continue

        function = apistub.callable(method) # Commented documentation
        #lines = ["// " + line.strip() for line in function.__doc__.strip().split("\n")]
        #print "\n".join(lines)
        #print

        
        in_el = wsdl.firstChild.appendChild(wsdl.createElement("wsdl:message"))
        in_el.setAttribute("name", method + "_in")

        for service_name in function.interfaces:
            if (services.has_key(service_name)):
                if (not method in services[service_name]):
                    services[service_name].append(method)
            else:
                services[service_name]=[method]

        # Arguments

        if (function.accepts):
            (min_args, max_args, defaults) = function.args()
            for (argname,argtype) in zip(max_args,function.accepts):
                arg_part = in_el.appendChild(wsdl.createElement("wsdl:part"))
                arg_part.setAttribute("name", argname)
                arg_part.setAttribute("type", param_type(argtype))
                
        # Return type            
        return_type = function.returns
        out_el = wsdl.firstChild.appendChild(wsdl.createElement("wsdl:message"))
        out_el.setAttribute("name", method + "_out")
        ret_part = out_el.appendChild(wsdl.createElement("wsdl:part"))
        ret_part.setAttribute("name", "returnvalue")
        ret_part.setAttribute("type", param_type(return_type))

        # Port connecting arguments with return type

        port_el = wsdl.firstChild.appendChild(wsdl.createElement("wsdl:portType"))
        port_el.setAttribute("name", method + "_port")
        
        op_el = port_el.appendChild(wsdl.createElement("wsdl:operation"))
        op_el.setAttribute("name", method)
        op_el.appendChild(wsdl.createElement("wsdl:input")).setAttribute("message","tns:" + method + "_in")
        op_el.appendChild(wsdl.createElement("wsdl:output")).setAttribute("message","tns:" + method + "_out")

        # Bindings

        bind_el = wsdl.firstChild.appendChild(wsdl.createElement("wsdl:binding"))
        bind_el.setAttribute("name", method + "_binding")
        bind_el.setAttribute("type", "tns:" + method + "_port")
        
        soap_bind = bind_el.appendChild(wsdl.createElement("soap:binding"))
        soap_bind.setAttribute("style", "rpc")
        soap_bind.setAttribute("transport","http://schemas.xmlsoap.org/soap/http")

        
        wsdl_op = bind_el.appendChild(wsdl.createElement("wsdl:operation"))
        wsdl_op.setAttribute("name", method)
        wsdl_op.appendChild(wsdl.createElement("soap:operation")).setAttribute("soapAction",
                "urn:" + method)

        
        wsdl_input = wsdl_op.appendChild(wsdl.createElement("wsdl:input"))
        input_soap_body = wsdl_input.appendChild(wsdl.createElement("soap:body"))
        input_soap_body.setAttribute("use", "encoded")
        input_soap_body.setAttribute("namespace", "urn:" + method)
        input_soap_body.setAttribute("encodingStyle","http://schemas.xmlsoap.org/soap/encoding/")

        
        wsdl_output = wsdl_op.appendChild(wsdl.createElement("wsdl:output"))
        output_soap_body = wsdl_output.appendChild(wsdl.createElement("soap:body"))
        output_soap_body.setAttribute("use", "encoded")
        output_soap_body.setAttribute("namespace", "urn:" + method)
        output_soap_body.setAttribute("encodingStyle","http://schemas.xmlsoap.org/soap/encoding/")
        

def add_wsdl_service(wsdl):
    for service in services.keys():
        service_el = wsdl.firstChild.appendChild(wsdl.createElement("wsdl:service"))
        service_el.setAttribute("name", service)

        for method in services[service]:
            name=method
            servport_el = service_el.appendChild(wsdl.createElement("wsdl:port"))
            servport_el.setAttribute("name", name + "_port")
            servport_el.setAttribute("binding", "tns:" + name + "_binding")

            soapaddress = servport_el.appendChild(wsdl.createElement("soap:address"))
            soapaddress.setAttribute("location", "%s/%s" % (globals.plc_ns,service))


def get_wsdl_definitions():
    wsdl_text_header = """
        <wsdl:definitions
        name="auto_generated"
        targetNamespace="%s"
        xmlns:xsd="http://www.w3.org/2000/10/XMLSchema"
        xmlns:tns="xmlns:%s"
        xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
        xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>""" % (globals.plc_ns,globals.plc_ns)
        
    wsdl = xml.dom.minidom.parseString(wsdl_text_header)

    return wsdl
    

services = {}

wsdl = get_wsdl_definitions()
add_wsdl_ports_and_bindings(wsdl)
add_wsdl_service(wsdl)


xml.dom.ext.PrettyPrint(wsdl)

