globalvar = []
tmpvar = []
localvar = []
localvar.append([])

listvar = []

tmpisenabled = []
tmpisenabled.append("false")
localindex = []
localindex.append(0)


class Variable:
	name = ""
	type = "nil"
	value = 0

def addVar(name, type, value):
	index = findVar(name)
	if index == "false":
		item = Variable()
		item.name = name
		item.type = type
		item.value = value
		if name[0:2] == "GF":
			globalvar.append(item)
			return
		if name[0:2] == "TF":
			if tmpisenabled[0] == "true":
				tmpvar.append(item)
				return
			else:
				exit(55)
		if name[0:2] == "LF":
			if localindex[0] > 0:
				localvar[localindex[0]].append(item)
				return
			else:
				exit(55)
	
	#print("multiple variable")
	exit(52)	
	
def setVar(name, type, value):
	index = findVar(name) 
	if index == "false":
		#print(name, "not used before")
		exit(54)
	
	if name[0:2] == "GF":
		globalvar[index].type = type
		globalvar[index].value = value
	if name[0:2] == "TF":
		if tmpisenabled[0] == "true": #edit
			tmpvar[index].type = type
			tmpvar[index].value = value
		else:
			exit(55)
	if name[0:2] == "LF":
		if localindex[0] > 0:
			localvar[localindex[0]][index].type = type
			localvar[localindex[0]][index].value = value
		else:
			exit(55)
	
def findVar(name):
	if name[0:2] == "GF":
		index = findGlobalVar(name)
	if name[0:2] == "TF":
		index = findTmpVar(name)
	if name[0:2] == "LF":
		index = findLocalVar(name)
	return index
	
def findGlobalVar(name):
	index = 0;
	for item in globalvar:
		if item.name == name:
			return index	
		index = index + 1
	return "false"

def findTmpVar(name):
	index = 0;
	if tmpisenabled[0] == "false":
		exit(55)
	for item in tmpvar:
		if item.name == name:
			return index
		index = index + 1
	return "false"

def findLocalVar(name):
	#print(localindex[0])
	index = 0; 
	for item in localvar[localindex[0]]:
		if item.name == name:
			return index
		index = index + 1
	if localindex[0] == 0:
		exit(55)
	return "false"

def getValue(name):
	if name[0:2] == "GF":
		for item in globalvar:
			if item.name == name:
				return item.value
	if name[0:2] == "TF":
		for item in tmpvar:
			if item.name == name:
				return item.value
	if name[0:2] == "LF":
		for item in localvar[localindex[0]]:
			if item.name == name:
				return item.value
	exit(55)
	
def getType(name):
	if name[0:2] == "GF":
		for item in globalvar:
			if item.name == name:
				return item.type
	if name[0:2] == "TF":
		for item in tmpvar:
			if item.name == name:
				return item.type
	if name[0:2] == "LF":
		for item in localvar[localindex[0]]:
			if item.name == name:
				return item.type