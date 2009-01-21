from xml.dom.minidom import Document

#rspec = {}
#rspec['netspec'] = {'name':'planetlab.us'}
#rspec['netspec']['node'] = {'name':'planetlab-1.cs.princeton.edu', 'type':'std'}
#rspec['netspec']['node']['ifspec'] = {'addr':'128.112.139.71', 'type':'ipv4', 'min_rate':'0', 'max_rate':'10000000'}
#rspec['netspec']['node'] = {'name':'planetlab-2.cs.princeton.edu', 'type':'std'}
#rspec['netspec']['node']['ifspec'] = {'addr':'128.112.139.72', 'type':'ipv4', 'min_rate':'0', 'max_rate':'10000000'}
#rspec['netspec']['node']['ifspec'] = {'addr':'128.112.139.73', 'type':'proxy', 'min_rate':'0', 'max_rate':'10000000'}
#rspec['netspec']['node']['ifspec'] = {'addr':'128.112.139.74', 'type':'proxy', 'min_rate':'0', 'max_rate':'10000000'}
#rspec['netspec'] = {'name':'planetlab.eu'}
#rspec['netspec']['node'] = {'name':'onelab03.onelab.eu', 'type':'std'}
#rspec['netspec']['node']['ifspec'] = {'addr':'128.112.139.321', 'type':'ipv4', 'min_rate':'0', 'max_rate':'10000000'}



# Create the minidom document
doc = Document()

# <rspec> base element
rspec = doc.createElement("RSpec")
rspec.setAttribute("start_time", "1235696400")
rspec.setAttribute("duration", "2419200")
doc.appendChild(rspec)

# networks
networks = doc.createElement("networks")
rspec.appendChild(networks)

# netspec
NetSpec = doc.createElement("NetSpec")
NetSpec.setAttribute("name", "plc.us")
networks.appendChild(NetSpec)

# nodes 
nodes = doc.createElement("nodes")
NetSpec.appendChild(nodes)

# NodeSpec
NodeSpec = doc.createElement("NodeSpec")
NodeSpec.setAttribute("name", "planetlab-1.cs.princeton.edu")
nodes.appendChild(NodeSpec)

# Create a <p> element
paragraph1 = doc.createElement("p")
maincard.appendChild(paragraph1)

## Give the <p> elemenet some text
#ptext = doc.createTextNode("This is a test!")
#paragraph1.appendChild(ptext)

# Print our newly created XML
print doc.toprettyxml(indent="  ")


