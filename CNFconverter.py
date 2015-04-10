import sys,getopt

inFile = sys.argv[1]

""" Functions for each Case """
def var(expr):
#    print expr
    return expr

def impliesop(expr1,expr2):
#    print "implies"
    n = list()
    n.append('or')
    n2 = list()
    n2.append('not')
    n2.append(expr1)
    n.append(n2)
    n.append(expr2)
    return convertexpr(n)

def andop(expr):
#	print "and"
	n=list()
	n.append('and')
	for i in expr[1:]:
		expr1=convertexpr(i)
		if isinstance(expr1,list) and expr1[0]=='and':
			n.extend(expr1[1:])
		else:
			n.append(expr1)
#	print "Before And Chop : " + str(n)
	to_remove = list()
	for p,i in enumerate(n):
		if isinstance(i,list) and i not in to_remove:		
			for j in n[p+1:]:
				if isinstance(j,list) and chckSim(i,j):
#					print "This is the culprit : " + str(j)
					to_remove.append(j)		
#		elif not isinstance(i,list) not in to_remove:
#			for j in n[p+1:]:
#				if not isinstance(j,list) and i == j:
#					to_remove.append(j)	
#	print "Am about to remove this : " + str(to_remove)
	for i in to_remove:
		n.remove(i)
#	print "After And Chop : " + str(n)
	n = chcklst(n)
		
#	print "Final : "
#	print new_expr
	if len(n) == 2:
		return n[1]
	

	return n


def notop(expr1):
#    print "not"
    l = len(expr1[1])

    if not isinstance(expr1[1],list):
        return expr1
    else:
        if(expr1[1][0] == 'not'):
		
		return convertexpr(expr1[1][1])
        elif(expr1[1][0] == 'and'):
		lis = expr1[1][1:]
		n = list()
		n.append('or')
		for i in lis:
			n1 = list()
			n1.append('not')
			n1.append(i)
			n.append(n1)
		return convertexpr(n)

        if(expr1[1][0] == 'or'):
		lis = expr1[1][1:]
		n = list()
		n.append('and')
		for i in lis:
			n1 = list()
			n1.append('not')
			n1.append(i)
			n.append(n1)
		return convertexpr(n)

	else:
		n = list()
        	n.append('not')
        	n.append(convertexpr(expr1[1]))
        	return convertexpr(n)

def iffop(expr1,expr2):
#    print "iff"
    n = list()
    n.append('or')
    n1 = list()
    n1.append('and')
    n1.append(expr1)
    n1.append(expr2)
    n2 = list()
    n3 = list()
    n3.append('not')
    n3.append(expr1)
    n4 = list()
    n4.append('not')
    n4.append(expr2)
    n2.append('and')
    n2.append(n3)
    n2.append(n4)
    n.append(n1)
    n.append(n2)
    return convertexpr(n)


def orop(expr):
#    print "or"
#	print "Before : " + str(expr)
	new_expr = list()
	new_expr.append('or')
	for i in expr[1:]:
		if isinstance(i,list):
			expr1 = convertexpr(i)
		else:
			expr1 = i
		if isinstance(expr1,list) and expr1[0] == 'or':
			new_expr.extend(expr1[1:])
#			print "In or : " + str(new_expr)
		else:
			new_expr.append(expr1)
	to_remove = list()
	singles = list()
#	print new_expr
	for p,i in enumerate(new_expr):
		if isinstance(i,list) and i not in to_remove:		
			for j in new_expr[p+1:]:
				if isinstance(j,list) and chckSim(i,j):
					to_remove.append(j)
		

	for i in to_remove:
#		print "In Remove : "
#		print new_expr
		new_expr.remove(i)
	
	new_expr = chcklst(new_expr)
		
#	print "Final : "
#	print new_expr
	if len(new_expr) == 2:
		return new_expr[1]
	
#	print "After : " + str(new_expr)	
	return new_expr

"""	
	to_remove = list()
	for p,i in enumerate(new_expr):
		if i in new_expr[p+1:]:
			to_remove.append(i)
		else:
			if isinstance(i,list) :		
				for j in new_expr[p+1:]:
					if isinstance(j,list) and chckSim(i,j):
						to_remove.append(j)		
	for i in to_remove:
		new_expr.remove(i)
"""

""" Check list """
def chcklst(expr):
	singles = list()
	double = list()
	for i in expr:
		if not isinstance(i,list) and i not in singles and i not in logicfunc:
			singles.append(i)
#			print "Single : " + str(singles)
		elif not isinstance(i,list) and i in singles and i not in logicfunc:
			double.append(i)
#			print "Duplicate : " + str(double)
	if len(double)>=1:
		for i in double:
			expr.remove(i)
	return expr	
	
""" Check for similar """
def chckSim(lis1,lis2):
#    print "Checking Similarity between : " + str(lis1) + " and " + str(lis2)
    if len(lis1) != len(lis2):
	return False
    unmatched = list(lis2)
    for element in lis1:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return True	    


""" Check to Distribute """
def chckDist(expr):
	if isinstance(expr,list) and expr[0]=='or':
		for i in expr:
			if isinstance(i,list) and i[0]=='and':
				a=distAnd(expr)
				expr = a
				break
	for n,i in enumerate(expr):
		if isinstance(i,list) and i[0]=='or':
			for j in i:
				if isinstance(j,list) and j[0]=='and':
					a = distAnd(i)
					expr[n] = a
	return convertexpr(expr)	

""" Distribute AND over OR """
def distAnd(expr):
	if len(expr) == 3:
		x = expr[1]
		y = expr[2]
		and_set = list()
		and_set.append('and')
			
		if (isinstance(x,list) and x[0]=='and') and (isinstance(y,list) and y[0]=='and'):
			for i in x[1:]:
				for j in y[1:]:
					or_set = list()
					or_set.append('or')			
					or_set.append(j)
					or_set.append(i)
					and_set.append(or_set)
		elif (isinstance(x,list) and x[0]=='and'):
#			print "X : " +str(x) + " Y : " + str(y)
			for i in x[1:]:
#				print "I in for : " + str(i) 
				or_set = list()
				or_set.append('or')
				or_set.append(i)
				or_set.append(y)
				and_set.append(or_set)
		elif (isinstance(y,list) and y[0]=='and'):
			for i in y[1:]:
				or_set = list()
				or_set.append('or')
				or_set.append(i)
				or_set.append(x)
				and_set.append(or_set)
#		print "And_Set : " + str(and_set)
		a = convertexpr(and_set)
#		print "in Two : " + str(a)
	 	return a
	else:
			for n,i in enumerate(expr[2:]):
				if n>0:
#					print "Evalexpr : " + str(evalexpr)
#					print "I : " + str(i)
					expr2 = evalexpr
				else:
					expr2 = expr[1] 
				expr1 = list()
				expr1.append('or')
				expr1.append(expr2)		
				expr1.append(i)
#				print "Expression passed : " + str(expr1)
				evalexpr = distAnd(expr1)
			a = convertexpr(evalexpr)
#			print str(a)
			return a

""" Mapping of Funciton with digit """
FUNC={
    0 : var,
    1 : impliesop,
    2 : andop,
    3 : notop,
    4 : iffop,
    5 : orop,
}

logicfunc = {'implies', 'not', 'or', 'iff', 'and'}

""" Convert Function """
def convertexpr(expr):
    l = len(expr)
    if l == 1:
        return expr
    elif l == 2:
        return FUNC[3](expr)
    elif l >= 3:
        if(expr[0] == 'implies'):
            return FUNC[1](expr[1],expr[2])
        elif(expr[0] == 'iff'):
            return FUNC[4](expr[1],expr[2])
        elif(expr[0] == 'and'):
            return FUNC[2](expr)
        elif(expr[0] == 'or'):
            return FUNC[5](expr)
    else:
        print "wrong expression"

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
		expr = eval(st)
	        x = convertexpr(expr)
	    	y = chckDist(x)
		fnl.append(y)
#		print y
#	print fnl
	
	f1 = open("sentences_CNF.txt","w")
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







