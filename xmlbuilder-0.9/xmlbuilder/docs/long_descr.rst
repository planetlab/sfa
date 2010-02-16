Example of usage:
-----------------


from __future__ import with_statement
from xmlbuilder import XMLBuilder
x = XMLBuilder(format=True)
with x.root(a = 1):
    with x.data:
        [x << ('node',{'val':i}) for i in range(10)]

print str(x)

will print

<root a="1">
    <data>
        <node val="0" />
        <node val="1" />
        <node val="2" />
        <node val="3" />
        <node val="4" />
        <node val="5" />
        <node val="6" />
        <node val="7" />
        <node val="8" />
        <node val="9" />
    </data>
</root>

Mercurial repo:http://hg.assembla.com/MyPackages/

Documentations
--------------
`XMLBuilder` is simple library build on top of `ElementTree.TreeBuilder` to
simplify xml files creation as much as possible. Althow it can produce
structured result with identated child tags. `XMLBuilder` use python `with`
statement to define xml tag levels and `<<` operator for simple cases -
text and tag without childs.

First we need to create xmlbuilder

    from xmlbuilder import XMLBuilder
    # params - encoding = 'utf8',
    # builder = None, - ElementTree.TreeBuilder 
    # tab_level = None, - current tab l;evel - for formatted output only
    # format = False, - create formatted output
    # tab_step = " " * 4 - indentation step
    xml = XMLBuilder()


Use `with` statement to make document structure
    #create and open tag 'root_tag' with text 'text' and attributes
    with xml.root_tag(text,attr1=val1,attr2=val2):
        #create and open tag 'sub_tag'
        with xml.sub_tag(text,attr3=val3):
            #create tag which are not valid python identificator
            with xml('one-more-sub-tag',attr7=val37):
                xml << "Some textual data"
            #here tag 'one-more-sub-tag' are closed
			#Tags without children can be created using `<<` operator
            for val in range(15):
                xml << ('message',"python rocks!"[:i])
            #create 15 child tag like <message> python r</message>
    #all tags closed
    node = ~x # get etree.ElementTree object
    xml_data = str(x)
    unicode_xml_data = unicode(x)
