import sys, getopt
inFile = sys.argv[1]


""" Find Clauses """
def findClauses(expr):
	clauses = list()
#	print expr
	if isinstance(expr,list) and expr[0] == 'and':
		for i in expr[1:]:
			clauses.append(i)
	else:
		clauses.append(expr)		
#	print clauses
	return clauses


""" Find Symbols  """
def findSymbols(clauses):
	symbols = list()
	for i in clauses:
		if isinstance(i,list) and i[0]=='or':
			for j in i[1:]:
				if j not in symbols:
					symbols.append(j)		
		elif i not in symbols:
			symbols.append(i)
#	print symbols
	return symbols


""" Check Clauses to be True or False """
def ChckTorF(clauses,model):
	numTrue = list()
	if len(model)>=1:
		for i in clauses:
			x= evalClause(i,model)
			if x:
				numTrue.append(i)
			elif x == False:
				return False
		if len(clauses) == len(numTrue):
			return True
							


""" Evaluate Clauses """
def evalClause(clause,model):
#	print "in eval"
	solvable = True
	stmt = False
#	print "Model Keys : " + str(model.keys())
	if isinstance(clause,list) and clause[0] == 'or':
		for i in clause[1:]:
#			print "I : " +str(i)
			if isinstance(i,list):
				j = i[1]
			else:
				j = i
			if j not in model.keys():
#				print "Am not here : " + str(j)
				solvable = False
#		print "Solvable : " +str(solvable)
		if solvable:
			if clause[0] == 'or':
				for i in clause[1:]:
					if not isinstance(i,list) and model.get(i):
						stmt = True
					elif isinstance(i,list):
						j = i[1]
						if not model.get(j):
							stmt = True
			return stmt

	elif isinstance(clause,list) and clause[0] == 'not':
		j = clause[1]
		if not model.get(j):
			stmt = True
		return stmt
			
	else:
		if model.get(clause):
			stmt = True
		return stmt		



""" Print Final """
def printFin(ans, model):
	answer = list()
	if ans==False:
		answer.append("false")
		return answer
	elif ans==True:
		answer.append("true")
		for i in model.keys():
			if len(i) == 1:
				if model.get(i):
					bool_temp = "true"
				else:
					bool_temp = "false" 
				str_temp = str(i) + "=" + str(bool_temp)
				answer.append(str_temp)
		return answer

""" Find Pure Symbol """
def findPureSymbol(symbols, clauses, model):
	pos = list()
	neg = list()
	for symbol in symbols:
#		print symbol
		if not isinstance(symbol,list) and symbol not in pos:
#			print symbol
			pos.append(symbol)
		elif isinstance(symbol,list) and symbol[1] not in neg:
			neg.append(symbol[1])
#	print "Positives : " + str(pos) + " Negatives : " + str(neg)
	for p in pos:
		if p not in neg:
#			print p
			sym = p, True
			return sym
	for n in neg:
		if n not in pos:
#			print n
			sym = n, False
			return sym

""" Find Unit Clause """
def findUnitClause(clauses, model):
	for i in clauses:
		if len(i) == 1:
			sym = i, True
			return sym
		elif len(i) == 2:
			sym = i[1],False
			return sym
		elif isinstance(i,list) and i[0] == 'or':
			count = 0
			for x in i[1:]:
				if isinstance(x,list):
					j = x[1]
					bool_temp = False
				else:
					j = x	
					bool_temp = True
				if j not in model.keys():
					count+=count
					index = j
			if count == 1:
				return j,bool_temp


""" Update Symbol """
def updateSymbol(symbols, symb):
	to_remove = list()
	for symbol in symbols:
		if isinstance(symbol, list) and symbol[1] == symb:
			to_remove.append(symbol)
		elif symbol == symb:
			to_remove.append(symbol)
	for i in to_remove:
		symbols.remove(i)

	return symbols

""" Update Model """
def updateModel(model,P): 
	model[P[0]] = P[1]
	lis = list()
	lis.append('not')
	lis.append(P[0])
	model[str(lis)]= not P[1]
	return model



""" Split Rule """
def SplitRule(clauses, symbols, model):
	P = (symbols[0], True)
	Q = (symbols[0], False)
#	print P		
	return DPLL(clauses, updateSymbol(symbols,P[0]), updateModel(model,P)) or DPLL(clauses, updateSymbol(symbols,Q[0]), updateModel(model,Q))


""" DPLL """
def DPLL(clauses, symbols, model):
#	print "Clauses : " + str(clauses)
#	print "Symbols : " + str(symbols)
#	print "Model : " + str(model)
	
	
#	print P
	check = ChckTorF(clauses,model) 
	if check :
		return printFin(True,model)
	elif check == False:
		return printFin(False,model)	
	
	P = findPureSymbol(symbols, clauses, model)
	if isinstance(P,tuple):
#		print P
		return DPLL(clauses, updateSymbol(symbols,P[0]), updateModel(model,P))

	P = findUnitClause(clauses, model)
	if isinstance(P,tuple):
#		print P
		return DPLL(clauses, updateSymbol(symbols,P[0]), updateModel(model,P))

	return SplitRule(clauses,symbols,model)

""" File open and call Convert """
def main(argv):
	inputfile = ""
	try:
		opts, args = getopt.getopt(argv,"i:",["ifile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile>'
	        sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
	        	inputfile = arg
	
	f = open(inputfile,"r")
	num = f.read(1)
	fnl = list()	

	for line in f:
	    st = line
#	    print st
	    if not st.isspace():
		model = dict()
		expr = eval(st)
		clauses = findClauses(expr)
		symbols = findSymbols(clauses)
		x = DPLL(clauses,symbols,model)
#		print str(x)
#		print expr
#	        x = convertexpr(expr)
#	    	y = chckDist(x)
		fnl.append(x)
#		print y
#	print fnl
	
	f1 = open("CNF_satisfiability.txt","w")
	s = ""
	for i in fnl:
		s = s + str(i) +"\n"
#		print i
	
#	print s	
	f1.write(s)
	f1.close()
	f.close()
		

if __name__ == "__main__":
   main(sys.argv[1:])

