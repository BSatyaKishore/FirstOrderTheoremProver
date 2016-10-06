execfile('1.py')
execfile('pars.py')
execfile('outp.py')
import sys
import copy


def pred_subs(Formula,a,b):
	las = Formula.keys()[0]
	if Formula  == a:
        	return b
        elif las in ['__and__','__or__','__not__']:
                temp = []
                for sat in Formula[las]:
        	        temp.append(pred_subs(sat,a,b))
                return {las:temp}
        elif las in ['__pred__','__fun__']:
        	temp = []
                temp.append(Formula[las][0])
                for sat in Formula[las][1:]:
                	temp.append(pred_subs(sat,a,b))
                return {las:temp}
	elif las in ['__ext__','__uniq__']:
 	       temp = []
               if Formula[las][0] != a:
        	       temp.append(Formula[las][0])
               else:
                       temp.append(b)
               for sat in Formula[las][1:]:
                       temp.append(substitution(sat,a,b))
               return {las:temp}
	else:
                return Formula

def substitution(Formula,a,b):
	las =  Formula.keys()[0]
	if (a == b):
		return Formula
	try:
		if a.keys()[0] == '__pred__' and len(a['__pred__']) == 1:
			return pred_subs(Formula,a,b)
	except AttributeError:
		if Formula.keys()[0] == a:
			return b
		elif las in ['__and__','__or__','__not__']:
			temp = []
			for sat in Formula[las]:
				temp.append(substitution(sat,a,b))
			return {las:temp}
		elif las in ['__pred__','__fun__']:
			temp = []
			temp.append(Formula[las][0])
			for sat in Formula[las][1:]:
				temp.append(substitution(sat,a,b))
			return {las:temp}
		elif las in ['__ext__','__uniq__']:
			temp = []
			if Formula[las][0] != a:
				temp.append(Formula[las][0])	
			else:
				temp.append(b)
			for sat in Formula[las][1:]:
				temp.append(substitution(sat,a,b))
			return {las:temp}
		else:
			return Formula

	
def name_change(Formula):
	global variable_used
	las =  Formula.keys()[0]
	if Formula[Formula.keys()[0]] == []:
		return Formula
	elif las in ['__and__','__or__','__not__']:
		temp = []
		for sat in Formula[las]:
			temp.append(name_change(sat))
		return {las:temp}
	elif las in ['__pred__','__fun__']:
		temp = []
		temp.append(Formula[las][0])
		for sat in Formula[las][1:]:
			temp.append(name_change(sat))
		return {las:temp}
	elif las in ['__ext__','__uniq__']:
		temp = []
		variable_used += 1	
		b = '__new__'+str(variable_used)	
		temp.append(b)
		print "printing",Formula[las][1:]
		for sat in Formula[las][1:]:
			temp.append(substitution(deepcopy(name_change(sat)),deepcopy(Formula[las][0]),b))
		return {las:temp}

ext_array = []
uniq_array = []

def pcnf(Formula):
	global ext_array,uniq_array
	las = Formula.keys()[0]
	if Formula[Formula.keys()[0]] == []:
		return Formula
	elif las in ['__and__','__or__','__not__']:
		temp = []
		for sat in Formula[las]:
			temp.append(pcnf(sat))
		return {las:temp}
	elif las in ['__pred__','__fun__']:
		temp = []
		temp.append(Formula[las][0])
		for sat in Formula[las][1:]:
			temp.append(pcnf(sat))
		return {las:temp}
	elif las == '__ext__':
		temp = []
		ext_array.append(deepcopy(Formula[las][0]))	
		for sat in Formula[las][1:]:
			temp.append(pcnf(sat))
		return temp[0]
	elif las == '__uniq__':
		temp = []
		uniq_array.append(deepcopy(Formula[las][0]))	
		for sat in Formula[las][1:]:
			temp.append(pcnf(sat))
		return temp[0]


def scnf(Formula):
	Formula = pcnf(Formula)
	fun_count = 0
	temp = []
	for sat in uniq_array:
		temp.append({sat:[]})
	for sat in ext_array:
		fun_count += 1
		Formula = substitution(Formula,sat,{'__fun__':['__fun_name__'+str(fun_count)]+temp})
	for sat in uniq_array:
		Formula = {'__uniq__': [sat]+ [Formula]}
	return Formula

'''
def mgu(k1,k2):
	if k1[k1.keys()[0]] == []:
		if k2[k2.keys()[0]] == []:
			if k1.keys()[0] == k2.keys()[0]:
				return {}
			else:
				return {'__not__':'unifiable'}
		else:
			return mgu(k2,k1)
	if k1.keys()[0] == '__pred__':
		if len(k1['__pred__']) == 1:
			if k2[k2.keys()[0]] == []:
					return {k1['__pred__'][0]:k2.keys()[0]}
			elif k2.keys()
		elif k2.keys()[0] in ['__and__','__or__',
	return
'''		
#sample_Fromula = [[], [{'__and__': [{'a': []}, {'b': []}]}], [{'c': []}]]#[[{'__or__':[{'__and__':[{'a':[]},{'b':[]}]},{'c':[]}]}]]

Zero_Order = structure(funs={'__and__':2, '__or__':2, '__imp__':2, '__not__':1, '__equ__':2})

#def check(List):
def check(List):
	for i in List:
		if i.keys()[0] == '__not__':
			if i['__not__'][0] in List:
				return False
	return True
			

def TableauRuleApplication(List):
	for instance in List:
		for sub_formula in instance:
			#	print sub_formula,"__________", instance, "=================", sub_formula.keys()[0]
			if instance[-1] != {'__False__':[12]}:
				if check(instance) == True:
					if sub_formula.keys()[0] == '__and__':
						#print "List is", List
						k = deepcopy(sub_formula['__and__'])
						del instance[instance.index(sub_formula)]
						for a in k:
							instance.append(deepcopy(a))
						#return List
					elif sub_formula.keys()[0] == '__or__':
						#print "List is", List
						k = deepcopy(sub_formula['__or__'])
						#print "k=", k
						del instance[instance.index(sub_formula)]
						#del List[List.index(instance)]
						#print "List is ", List
						temp = deepcopy(instance)
						instance.append(deepcopy(k[0]))
						temp.append(deepcopy(k[1]))	
						List.append(deepcopy(temp))
						#print "List is",List
						#del instance[instance.index(sub_formula)]
						#return List
					elif sub_formula[sub_formula.keys()[0]] == '__imp__':
						k = deepcopy(sub_formula['__imp__'])
						del instance[instance.index(sub_formula)]
						temp = deepcopy(instance)
		                                temp.append({'__not__':deepcopy(k[0])})
		                                List.append(deepcopy(temp))
						temp = deepcopy(instance)
	                	                temp.append(deepcopy(k[1]))
	                        	        List.append(deepcopy(temp))
						#return List
					elif sub_formula[sub_formula.keys()[0]] == '__equ__':
						k = deepcopy(sub_formula['__equ__'])
						del instance[instance.index(sub_formula)]
						temp = deepcopy(instance)
	                                	temp.append({ '__and__':[deepcopy(k[0]),deepcopy(k[1])] })
		                                List.append(deepcopy(temp))
						temp = deepcopy(instance)
	                	                temp.append({ '__and__':[{'__not__':deepcopy(k[0])},{'__not__':deepcopy(k[1])} ]})                           
	                        	        List.append(deepcopy(temp))
						#return List
					elif sub_formula[sub_formula.keys()[0]] == '__not__':
						k = deepcopy(sub_formula['__equ__'])
						del instance[instance.index(sub_formula)]
						if k[0].keys()[0] == '__not__':
							instance.append(deepcopy(k[0]['__not__']))
							#return List
						elif k[0].keys()[0] == '__and__':
							instance.append({'__or__':[{'__not__':deepcopy(k[0]['__and__'][0])},{'__not__':deepcopy(k[0]['__and__'][1])}]})
							#return List
						elif k[0].keys()[0] == '__or__':
							instance.append({'__and__':[{'__not__':deepcopy(k[0]['__or__'][0])},{'__not__':deepcopy(k[0]['__or__'][1])}]})
							#return List
						elif k[0].keys()[0] == '__imp__':
							instance.append({'__and__':[deepcopy(k[0]['__imp__'][0]),{'__not__':deepcopy(k[0]['__imp__'][1])}]})
							#return List
						elif k[0].keys()[0] == '__equ__':
							instance.append({'__equ__':[deepcopy(k[0]['__equ__'][0]),{'__not__':deepcopy(k[0]['__equ__'][1])}]})
							#return List
				else:
					instance.append({'__False__':[12]})
	return List

sam = [[]]
while sam != sample_Fromula:
	sam = sample_Fromula
	sample_Fromula = TableauRuleApplication(sam)
	sam = sample_Fromula
	sample_Fromula = TableauRuleApplication(sam)
	
print sam
outpu(sam)
