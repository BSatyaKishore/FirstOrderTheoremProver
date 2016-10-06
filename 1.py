class structure:
        def __init__(self,var=[],funs={},rel={}):
                self.variables = var
                self.functions = funs
                self.relations = rel
		for i in var:
			self.functions[i] = 0

        def add_variable(self,a):
                self.variables.append(a)
                self.functions[a] = 0

class formula:
        def __init__(self,structure,operator,operands=[]):
                if structure.functions[operator] == len(operands):
                        self.op = operator
                        self.op_and = operands
                else:
                        raise ValueError("structure.functions[operator] != len(operands)")
