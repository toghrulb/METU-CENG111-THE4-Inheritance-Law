def inheritance(example):
	child=[]
	married=[]
	departed=[]
	deceased=[]
	for i in example:
		if i[0] == 'C':
			child.append(i)
		if i[0] == 'M':
			married.append(i)
		if i[:3] == 'DEP':
			departed.append(i)
		if i[:3] == 'DEC':
			deceased.append(i)
	def blanks(lst):
		for i in range(0, len(lst)):
			lst[i] = lst[i].split(" ")
			while "" in lst[i]:
				lst[i].remove("")
		return lst
	deceased=blanks(deceased)
	child=blanks(child)
	married=blanks(married)
	departed=blanks(departed)
	def alive(name):
		isalive=True
		for i in departed:
			if i[1] == name:
				isalive=False
		return isalive
	def perschilds(name):
		r=[]
		for i in child:
			if i[1] == name or i[2] == name:
				r.extend(i[3:])
		if len(r) == 0:
			return False
		return r
	def spouse(name):
		for i in married:
			if i[1] == name:
				return i[2]
			if i[2] == name:
				return i[1]
		return False
	def parents(name):
		for i in child:
			for j in range(3, len(i)):
				if i[j] == name:
					return i[1:3]
		return False
	DeceasedName=deceased[0][1]
	DeceasedMoney=int(deceased[0][2])

	def descendants_checker(name):
		if perschilds(name) == False:
			return False
		else:
			for i in perschilds(name):
				if alive(i) == True:
					return True
			for i in perschilds(name):
				return descendants_checker(i)
	def PGcounter():
		if descendants_checker(DeceasedName) == True:
			return 1
		if parents(DeceasedName) == False:
			return -1
		if alive(parents(DeceasedName)[0]) == True or alive(parents(DeceasedName)[1]) == True:
			return 2
		if descendants_checker(parents(DeceasedName)[0]) == True or descendants_checker(parents(DeceasedName)[1]) == True:
			return 2
		if parents(parents(DeceasedName)[0]) != False:
			if alive(parents(parents(DeceasedName)[0])[0]) == True or alive(parents(parents(DeceasedName)[0])[1])==True:
				return 3
		if parents(parents(DeceasedName)[1]) != False:
			if alive(parents(parents(DeceasedName)[1])[0]) == True or alive(parents(parents(DeceasedName)[1])[1])==True:
				return 3
		if descendants_checker(parents(parents(DeceasedName)[0])[0]) == True or descendants_checker(parents(parents(DeceasedName)[0])[1]) == True or descendants_checker(parents(parents(DeceasedName)[1])[0]) == True or descendants_checker(parents(parents(DeceasedName)[1])[1]) == True:
			return 3
	PGcount = PGcounter()
	result = []
	if PGcount == 1:
		if spouse(DeceasedName) != False:
			if alive(spouse(DeceasedName)) == True:
				result.append((spouse(DeceasedName), DeceasedMoney/4))
				DeceasedMoney*=0.75
	if PGcount == 2:
		if spouse(DeceasedName) != False:
			if alive(spouse(DeceasedName)) == True:
				result.append((spouse(DeceasedName), DeceasedMoney/2))
				DeceasedMoney*=0.5

	if PGcount == 3:
		if spouse(DeceasedName) != False:
			if alive(spouse(DeceasedName)) == True:
				result.append((spouse(DeceasedName), DeceasedMoney*0.75))
				DeceasedMoney*=0.25
	if PGcount == -1:
		if spouse(DeceasedName) != False:
			if alive(spouse(DeceasedName)) == True:
				return [(spouse(DeceasedName), DeceasedMoney)]
	def MoneyDistributor(name, money):
		divider = len(perschilds(name))
		for i in perschilds(name):
			if alive(i) == False:
				if descendants_checker(i) == False:
					divider -= 1
		for i in perschilds(name):
			if alive(i) == True:
				ch = 0
				for j in range(len(result)):
					if i == result[j][0]:
						ch = 1
						ind = j
				if ch == 0:
					result.append((i, money / divider))
				else:
					result[ind] = (i, result[ind][1]+(money / divider))
		for i in perschilds(name):
			if alive(i) == False:
				if descendants_checker(i) == True:
					MoneyDistributor(i, money / divider)
	if PGcount == 1:
		MoneyDistributor(DeceasedName, DeceasedMoney)
	if PGcount == 2:
		divider = 2
		for i in parents(DeceasedName):
			if alive(i) == False:
				if descendants_checker(i) == False:
					divider -= 1
		for i in parents(DeceasedName):
			if alive(i) == True:
				result.append((i,DeceasedMoney/divider))
		for i in parents(DeceasedName):
			if alive(i) == False:
				if descendants_checker(i) == True:
					MoneyDistributor(i, DeceasedMoney/divider)
	if PGcount == 3:
		divider = 2
		if parents(parents(DeceasedName)[0]) != False:
			for i in parents(parents(DeceasedName)[0]):
				if alive(i) == False:
					if descendants_checker(i) == False:
						divider -=1
			for i in parents(parents(DeceasedName)[0]):
				if alive(i) == False:
					if descendants_checker(i) == False:
						divider -=1
			for i in parents(parents(DeceasedName)[0]):
				if alive(i) == True:
					result.append((i,DeceasedMoney/divider))
		divider = 2
		if parents(parents(DeceasedName)[1]) != False:
			for i in parents(parents(DeceasedName)[1]):
				if alive(i) == True:
					result.append((i,DeceasedMoney/divider))
			for i in parents(parents(DeceasedName)[1]):
				if alive(i) == False:
					if descendants_checker(i) == True:
						MoneyDistributor(i, DeceasedMoney/divider)
			for i in parents(parents(DeceasedName)[1]):
				if alive(i) == False:
					if descendants_checker(i) == True:
						MoneyDistributor(i, DeceasedMoney/divider)
	return result