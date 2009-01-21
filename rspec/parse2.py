from xml.dom.minidom import *


sample_xml_file = 'sample_rspec.xml'
f = open(sample_xml_file, 'r')
lines = f.readlines()
xml = ""
for line in lines:
    xml += line.replace('\n', '',).replace('\t', '').strip()
    
dom = parseString(xml)

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def handleRspec(rspec):
    # create rspec dict
    rdict = {}
    tempdic = []
    # loop through each network element 
    for i in rspec.getElementsByTagName("NetSpec"):
        # handle networks call
        temp = handleNetworks(i)
        tempdic.append(temp)
    # append the temp dict
    rdict['networks'] = tempdic
    return rdict

def handleIfs(interf):
    # create if dict
    ifdict = {}
    # loop through attribs and put key value pair into array
    for i in interf.attributes:
        a = node.attributes[i]
        ifdict[a.name] = a.value
        
    return ifdict

def handleNodes(node):
    # create node dict
    nodict = {}
    # loop through attribs and put key value pair into array
    for i in node.attributes:
        a = node.attributes[i]
        nodict[a.name] = a.value
    tempd = []
    # loop through each IF element
    for i in node.getElementsByTagName("IfSpec"):
        # handle ifs
        tempd.append(handleIfs(i))
    # append temp dict
    nodict['ifs'] = tempd
    return nodict

def handleNetworks(network):
    # create network dict
    ndict = {'name':network.nodeName}
    tempdict = []
    # loop through each node element
    for i in network.getElementsByTagName("NodeSpec"):
        # handle nodes
        tempdict.append(handleNodes(i))
    # append temp dict
    ndict['nodes'] = tempdict
    return ndict

def handleTest(slices):
    for slide in slices:
        sdict = slice.getElementsByTagName("slices")[0]
        print "<p>%s</p>" % getText(slice.childNodes)

handleRspec(dom)

