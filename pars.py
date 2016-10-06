import xml.etree.ElementTree as ET
from copy import deepcopy, _deepcopy_dispatch

variable_used = 0

tree = ET.parse('input.xml')

def parser(Tree):
	global variable_used
	if Tree.tag == 'Set':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return formula
	elif Tree.tag == 'Element':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return formula
	elif Tree.tag == 'Disjunction':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return {'__or__':formula}
	elif Tree.tag == 'Conjunction':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return {'__and__':formula}
	elif Tree.tag == 'Negation':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return {'__not__':formula}
	elif Tree.tag == 'Equivalence':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return {'__equ__':formula}
	elif Tree.tag == 'Implies':
		formula = []
		for child in Tree:
			formula.append(parser(child))
		return {'__imp__':formula}
	elif Tree.tag == 'Letter':
		formula = []
		return {str(Tree.attrib['val']):formula}
	elif Tree.tag == 'Variable':
		formula = []
		return {'__pred__':[str(Tree.attrib['name'])]}
	elif Tree.tag == 'Predicate':
		formula = []
		formula.append(str(Tree,attrib['name']))
		for child in Tree:
			formula.append(parser(child))
		return {'__pred__':formula}
	elif Tree.tag == 'Function':
		formula = []
		formula.append(str(Tree,attrib['name']))	
		for child in Tree:
			formula.append(parser(child))
		return {'__fun__':formula}
	elif Tree.tag == 'UniversalQuantifier':
		formula = []
		formula.append(str(Tree,attrib['quantifier']))	
		for child in Tree:
			formula.append(parser(child))
		return {'__uniq__':formula}
	elif Tree.tag == 'ExistentialQuantifier':
		formula = []
		formula.append(str(Tree,attrib['quantifier']))	
		for child in Tree:
			formula.append(parser(child))
		return {'__ext__':formula}
	


sample_Fromula =  parser(tree.getroot())

def rewrite(a):
	if a[a.keys()[0]] == []:
		return a
	elif a.keys()[0] == '__not__':
		return {'__not__':[rewrite(a)]}
	elif a.keys()[0] == '__and__':
		return {'__and__':[rewrite(a['__and__'][0]),rewrite(a['__and__'][1])]}
	elif a.keys()[0] == '__or__':
		return {'__or__':[rewrite(a['__or__'][0]),rewrite(a['__or__'][1])]}
	elif a.keys()[0] == '__imp__':
		return {'__or__':[{'__not__':rewrite(a['__imp__'][0])},rewrite(a['__imp__'][1])]}
	elif a.keys()[0] == '__equ__':
		return rewrite({'__and__':[{'__imp__':[rewrite(a['__equ__'][0]),rewrite(a['__equ__'][1])]},{'__imp__':[rewrite(a['__equ__'][1]),rewrite(a['__equ__'][0])]}]})
	elif a.keys()[0] == '__pred__':
		temp = []
		temp.append(a['__pred__'][0])
		for ila in a['__pred__'][1:]:
			temp.append(deepcopy(rewrite(ila)))
		return ({'__pred__':temp})
	elif a.keys()[0] == '__fun__':
		temp = []
		temp.append(a['__fun__'][0])
		for ila in a['__fun__'][1:]:
			temp.append(deepcopy(rewrite(ila)))
		return ({'__fun__':temp})
	elif a.keys()[0] == '__uniq__':
		temp = []
		temp.append(a['__uniq__'][0])
		for ila in a['__uniq__'][1:]:
			temp.append(deepcopy(rewrite(ila)))
		return ({'__uniq__':temp})
	elif a.keys()[0] == '__ext__':
		temp = []
		temp.append(a['__ext__'][0])
		for ila in a['__ext__'][1:]:
			temp.append(deepcopy(rewrite(ila)))
		return ({'__ext__':temp})



def normal_form(a):
	if a[a.keys()[0]] == []:
		return a
	elif a.keys()[0] == '__not__':
		b = a['__not__'][0]
		if b[b.keys()[0]] == []:
			return {'__not__':[b]}
		elif b.keys()[0] == '__not__':
			return normal_form(b)
		elif b.keys()[0] == '__and__':
			return normal_form({'__or__':[{'__not__':b['__and__'][0]},{'__not__':b['__and__'][1]}]})
		elif b.keys()[0] == '__or__':
			return normal_form({'__and__':[{'__not__':b['__or__'][0]},{'__not__':b['__or__'][1]}]})
		elif b.keys()[0] == '__uniq__':
			temp = []
			temp.append(b['__uniq__'][0])
			for ila in b['__uniq__'][1:]:
				temp.append(deepcopy(normal_form({'__not__':ila})))
			return normal_form({'__ext__':temp})
		elif b.keys()[0] == '__ext__':
			temp = []
			temp.append(b['__ext__'][0])
			for ila in b['__ext__'][1:]:
				temp.append(deepcopy(normal_form({'__not__':ila})))
			return normal_form({'__uniq__':temp})	
	elif a.keys()[0] == '__and__':
		return {'__and__':[normal_form(a['__and__'][0]),normal_form(a['__and__'][1])]}
	elif a.keys()[0] == '__or__':
		return {'__or__':[normal_form(a['__or__'][0]),normal_form(a['__or__'][1])]}
	elif a.keys()[0] == '__pred__':
		temp = []
		temp.append(a['__pred__'][0])
		for ila in a['__pred__'][1:]:
			temp.append(deepcopy(normal_form(ila)))
		return {'__pred__':temp}
	elif a.keys()[0] == '__fun__':
		temp = []
		temp.append(a['__fun__'][0])
		for ila in a['__fun__'][1:]:
			temp.append(deepcopy(normal_form(ila)))
		return ({'__fun__':temp})
	elif a.keys()[0] == '__uniq__':
		temp = []
		temp.append(a['__uniq__'][0])
		for ila in a['__uniq__'][1:]:
			temp.append(deepcopy(normal_form(ila)))
		return ({'__uniq__':temp})
	elif a.keys()[0] == '__ext__':
		temp = []
		temp.append(a['__ext__'][0])
		for ila in a['__ext__'][1:]:
			temp.append(deepcopy(normal_form(ila)))
		return ({'__ext__':temp})
		


def distOR(a,b):
	if b.keys()[0] == '__and__':
		return {'__and__':[distOR(a,b['__and__'][0]),distOR(a,b['__and__'][1])]}
	elif a.keys()[0] == '__and__':
		return {'__and__':[distOR(a['__and__'][0],b),distOR(a['__and__'][1],b)]}
	elif a.keys()[0] == '__pred__':
		temp = []
		temp.append(a['__pred__'][0])
		for ila in a['__pred__'][1:]:
			temp.append(deepcopy(distOR(ila)))
		return ({'__pred__':temp})
	elif a.keys()[0] == '__fun__':
		temp = []
		temp.append(a['__fun__'][0])
		for ila in a['__fun__'][1:]:
			temp.append(deepcopy(distOR(ila)))
		return ({'__fun__':temp})
	elif a.keys()[0] == '__uniq__':
		temp = []
		temp.append(a['__uniq__'][0])
		for ila in a['__uniq__'][1:]:
			temp.append(deepcopy(distOR(ila)))
		return ({'__pred__':temp})
	elif a.keys()[0] == '__ext__':
		temp = []
		temp.append(a['__ext__'][0])
		for ila in a['__ext__'][1:]:
			temp.append(deepcopy(distOR(ila)))
		return ({'__ext__':temp})
	else:
		return {'__or__':[a,b]}
		

def cod(a):
	if a.keys()[0] == '__and__':
		return {'__and__':[cod(a['__and__'][0]),cod(a['__and__'][1])]}
	elif a.keys()[0] == '__or__':
		return distOR(cod(a['__or__'][0]),cod(a['__or__'][1]))
	else:
		return a

def cnf(a):
	return cod(normal_form(rewrite(a)))
		
def cnf_set(a):
	ki = cnf(a)
	sh = ki['__and__']
	shar = []
	for i in sh:
		ays = []
		for j in i['__or__']:
			ays.append(j)
		shar.append(ays)
	return set(frozenset(i) for i in shar)
#sample_Formula = [[]]
# [[{'__or__': [{'a': []}, {'__and__': [{'b': []}, {'c': []}]}]}], [{'__not__': [{'a': []}]}], [{'__not__': [{'b': []}]}]]

while True:
	if len(sample_Fromula) == 1:
		#sample_Fromula = sample_Fromula
		break
	elif len(sample_Fromula) == 2:
		sample_Fromula = [[{'__and__':[sample_Fromula[0][0],sample_Fromula[1][0]]}] ]
	else:
		sha = [[{'__and__':[sample_Fromula[0][0],sample_Fromula[1][0]]}]]
		for arbit in sample_Fromula[2:]:
			sha.append(arbit)
		sample_Fromula = sha



#[[{'__and__': [{'__and__': [{'__or__': [{'a': []}, {'__and__': [{'b': []}, {'c': []}]}]}, {'__not__': [{'a': []}]}]}, [{'__not__': [{'b': []}]}]]}]]
