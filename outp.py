from xml.etree import ElementTree as ET
#[[], [{'__not__': [{'a': []}]}], [{'__not__': [{'b': []}]}], [{'a': []}], [{'b': []}, {'c': []}]]

def out(term):
	if term.keys()[0] == '__not__':
		return "<Negation><Letter val="+'"'+term['__not__'][0].keys()[0]+'"/></Negation>'
	else:
		return "<Letter val="+'"'+term.keys()[0]+'"/>'

def outpu(formula):
	main_root = ET.Element('Sets')
	a_root = ET.Element('Sets')
	for i in formula:
		root = ET.SubElement(main_root,'Set')
		if i[-1] != {'__False__':[12]}:
			root = ET.SubElement(a_root,'Set')
		for j in i:
			if j.keys()[0] == '__False__':
				pass
			else:
				sub = ET.SubElement(root,'Element')
				if j.keys()[0] == '__not__':
					main_sub = ET.SubElement(sub,'Negation')
					mains_sub = ET.SubElement(main_sub,'Letter',{'val':j['__not__'][0].keys()[0]})
				else:
					mains_sub = ET.SubElement(sub,'Letter',{'val':j.keys()[0]})				
		if i[-1] != {'__False__':[12]}:
			tree = ET.ElementTree(a_root)
			tree.write('output.xml')
			return
	tree = ET.ElementTree(main_root)
	tree.write('output.xml')
