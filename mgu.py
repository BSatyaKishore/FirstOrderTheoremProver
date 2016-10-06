execfile('main.py')

output_ = []
def mgu(formula1, formula2):
	print "sat"
	global output_
	#formula1 = substitution(for
	if (formula2.keys()[0] == '__pred__' and len(formula2['__pred__']) == 1):
		return mgu(formula2,formula1)
	if formula1.keys()[0] == '__pred__' and len(formula1['__pred__']) == 1:
		if formula2.keys()[0] == '__pred__' and len(formula2['__pred__']) == 1:
			if formula1['__pred__'][0] == formula2['__pred__'][0]:
				return output_
			else:
				output_.append((formula1 , formula2))
				return output_
		elif formula2.keys()[0] in ['__or__','__and__','__not__','__pred__','__fun__']:
			output_.append(( formula1 , formula2 ))
			return output_
	elif formula1[formula1.keys()[0]] == []:
		if formula2[formula2.keys()[0]] == []:
			if formula1 == formula2:
				return output_
			else:
				raise Exception('Not Unifiable')
		else:
			raise Exception('Not Unif')
	elif formula1.keys()[0] == '__and__':
		if formula2.keys()[0] == '__and__':
			try:
				output_ += [mgu(formula1['__and__'][0],formula2['__and__'][0]),mgu(formula1['__and__'][1],formula2['__and__'][1])]
				return output_
			except: 
				try:
					output_ += [(mgu(formula1['__and__'][0],formula2['__and__'][0])),(mgu(formula1['__and__'][1],formula2['__and__'][1]))]
					return output_
				except:
					raise Exception('Not Unifiable')
		else:
			raise Exception('Not Unifiable')
        elif formula1.keys()[0] == '__or__':
                if formula2.keys()[0] == '__or__':
                        try:
                                output_ += [mgu(formula1['__or__'][0],formula2['__or__'][0]),(mgu(formula1['__or__'][1],formula2['__or__'][1]))]
				return output_
                        except: 
                                try:
                                        output_ += [(mgu(formula1['__or__'][0],formula2['__or__'][0])),(mgu(formula1['__or__'][1],formula2['__or__'][1]))]
					return output_
                                except:
                                        raise Exception('Not Unifiable')
                else:
                        raise Exception('Not Unifiable')
	elif formula1.keys()[0] == '__pred__':
		if formula2.keys()[0] == '__pred__':
			if formula1['__pred__'][0] == formula2['__pred__'][0]:
				try:
					out = []
					for sh in range(len(formula1['__pred__'])):
						output_.append((mgu(formula1['__pred__'][sh],formula2['__pred__'][sh])))
					return output_
				except:
					raise Exception('Not Unifiable')
			else:
				raise Exception('Not Unifiable')
        elif formula1.keys()[0] == '__fun__':
                if formula2.keys()[0] == '__fun__':
                        if formula1['__fun__'][0] == formula2['__fun__'][0]:
                                try:
                                        out = []
                                        for sh in range(len(formula1['__fun__'])):
                                                output_.append[mgu(formula1['__fun__'][sh],formula2['__fun__'][sh])]
					return output_
                                except: 
                                        raise Exception('Not Unifiable')
                        else:
                                raise Exception('Not Unifiable')
	elif formula1.keys()[0] == '__not__':
		if formula2.keys()[0] == '__not__':
			return [mgu (formula1['__not__'][0],formula2['__not__'][0])]
		elif formula1['__not__'][0].keys()[0] == '__pred__' and len(formula1['__not__'][0]['__pred__']) == 1:
			return [mgu (formula1['__not__'][0], {'__not__':formula2})]
		else:
			raise Exception('Not Unifiable')


print mgu({'__and__':[{'la':[]},{'__pred__':['p',{'a':[]}]}]},{'__and__':[{'__pred__':['c']},{'__pred__':['d']}]})
print output_

