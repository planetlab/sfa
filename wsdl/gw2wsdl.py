#!/usr/bin/python
#
# Sapan Bhatia <sapanb@cs.princeton.edu>
#
# This code is under preliminary development. I am going to clean it up
# once it is tested to work.
# Generates a WSDL for geniwrapper


import os, sys
import time
import pdb
import xml.dom.minidom
import xml.dom.ext
import globals
import apistub
from types import *

from geni.util.auth import Auth
from geni.util.parameter import Parameter,Mixed

complex_types = {}
services = {}

num_types = 0

class SoapError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)
try:
    set
except NameError:
    from sets import Set
    set = Set

def fold_complex_type_names(acc, arg):
    name = arg.doc
    if (type(acc)==list):
        acc.append(name)
    else:
        python_is_braindead = acc.doc
        acc = [python_is_braindead,name]
    return acc


def fold_complex_type(acc, arg):
    global complex_types
    name = name_complex_type(arg)
    complex_types[arg]=name
    if (type(acc)==list):
        acc.append(name)
    else:
        python_is_braindead = name_complex_type(acc)
        acc = [python_is_braindead,name]
    return acc

def name_complex_type(arg):
    global num_types
    global types

    #if (complex_types.has_key(arg)):
    #    return complex_types[arg]

    types_section = types.getElementsByTagName("wsdl:types")[0]

    if (isinstance(arg, Mixed)):
        inner_types = reduce(fold_complex_type, arg)
        inner_names = reduce(fold_complex_type_names, arg)
        if (inner_types[-1]=="none"):
            inner_types=inner_types[:-1]
            min_args = 0
        else:
            min_args = 1
    
        num_types=num_types+1
        type_name = "Type%d"%num_types
        complex_type = types_section.appendChild(types.createElement("xsd:complexType"))
        complex_type.setAttribute("name", type_name)

        choice = complex_type.appendChild(types.createElement("xsd:choice"))
        for n,t in zip(inner_names,inner_types):
            element = choice.appendChild(types.createElement("element"))
            element.setAttribute("name", n)
            element.setAttribute("type", "%s"%t)
            element.setAttribute("minOccurs","%d"%min_args)
        return "tns:%s"%type_name
    elif (isinstance(arg, Parameter)):
        return (name_simple_type(arg.type))
    elif type(arg) == ListType or type(arg) == TupleType:
        return "sequence"
    elif type(arg) == DictType or arg == DictType:
        return "dict"
    else:
        return (name_simple_type(arg))

def name_simple_type(arg_type):
    if arg_type == None:
        return "none"
    if arg_type == DictType:
        return "xsd:dict"
    elif arg_type == IntType or arg_type == LongType:
        return "xsd:int"
    elif arg_type == bool:
        return "xsd:boolean"
    elif arg_type == FloatType:
        return "xsd:double"
    elif arg_type in StringTypes:
        return "xsd:string"
    else:
       #pdb.set_trace()
        raise SoapError, "Cannot handle %s objects" % arg_type

def param_type(arg):
    return (name_complex_type(arg))

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
        inp_el=wsdl.createElement("wsdl:input")
        inp_el.setAttribute("message","tns:" + method + "_in")
        inp_el.setAttribute("name",method+"_request")
        op_el.appendChild(inp_el)
        out_el = wsdl.createElement("wsdl:output")
        out_el.setAttribute("message","tns:" + method + "_out")
        out_el.setAttribute("name",method+"_response")
        op_el.appendChild(out_el)

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
        xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>
        """ % (globals.plc_ns,globals.plc_ns)
        
    wsdl = xml.dom.minidom.parseString(wsdl_text_header)
    
    return wsdl

def get_wsdl_definitions():
    wsdl_text_header = """
        <wsdl:definitions
        name="auto_generated"
        targetNamespace="%s"
        xmlns:xsd="http://www.w3.org/2000/10/XMLSchema"
        xmlns:tns="xmlns:%s"
        xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
        xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>
        """ % (globals.plc_ns,globals.plc_ns)
        
    wsdl = xml.dom.minidom.parseString(wsdl_text_header)
    
    return wsdl

def get_wsdl_definitions_and_types():
    wsdl_text_header = """
    <wsdl:definitions
        name="auto_generated"
        targetNamespace="%s"
        xmlns:xsd="http://www.w3.org/2000/10/XMLSchema"
        xmlns:tns="xmlns:%s"
        xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
        xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
        <wsdl:types>
            <xsd:schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="%s"/>
        </wsdl:types>
    </wsdl:definitions> """ % (globals.plc_ns,globals.plc_ns,globals.plc_ns)
    wsdl = xml.dom.minidom.parseString(wsdl_text_header)
    return wsdl

    
types = get_wsdl_definitions_and_types()

wsdl = get_wsdl_definitions()
add_wsdl_ports_and_bindings(wsdl)
wsdl_types = wsdl.importNode(types.getElementsByTagName("wsdl:types")[0], True)
wsdl.firstChild.appendChild(wsdl_types)
add_wsdl_service(wsdl)

xml.dom.ext.PrettyPrint(wsdl)
