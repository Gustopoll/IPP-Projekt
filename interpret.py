#!/bin/env python3

import xml.etree.ElementTree as ET
import sys
import re
from i_variable import *

class Instuction:
	def __init__(self):
		self.argv = []
	name = ""
	argc = 0
	order = 0
	
class Argument:
	name = ""
	type = ""
	order = ""
	
class Label:
	name = ""
	index = 0

def convert(value,type):
	if type == "int":
		try:
			value = int(value)
		except:
			value = 0
	if type == "bool":
		if value.lower() == "true":
			value = "true"
		else:
			value = "false"
	if type == "string":
		for char in value:
			if char == " ":
				return ""
	if type == "nil":
		exit(32)
	return value

def checkLexical(name,type):
	if type == "string":
		if name == None:
			return
		arr = re.findall("\S*",name)
		if len(arr) == 2: 
			return
	if name == None:
		exit(32)
		
	if type == "int":
		arr = re.findall("([0-9]|-)([0-9])*",name)
		if len(arr) == 1: 
			return
	if type == "bool":
		if name == "true" or name == "false":
			return
	if type == "nil":
		if name == "nil":
			return
	if type == "label":
		arr = re.findall("[_$&%*!?-]*([a-z]|[A-Z])+([a-z]|[A-Z]|[_$&%*!?-]|[0-9])*",name)
		if len(arr) == 1: 
			return
	if type == "type":
		if name == "string" or name == "bool" or name == "int" or name == "nil":
			return
	if type == "var":
		if re.match(r'(LF@|GF@|TF@)([_$&%*!?-]*([a-z]|[A-Z])+)([a-z]|[A-Z]|[_$&%*!?-]|[0-9])*',name).group() == name:
			return
	exit(32)

def isConst(name):
	if name == "string":
		return "true"
	if name == "bool":
		return "true"
	if name == "int":
		return "true"
	if name == "nil":
		return "true"
	return "false"
	
def getLabelIndex(name):
	for item in listLabel:
		if name == item.name:
			return item.index
	#nedefinovane navestie
	exit(52)
	
def isContainLabel(name):
	for item in listLabel:
		if item.name == name:
			return "true"
	return "false"
	
def isSymbolDefine(name,type):
	if type == "var":
		if findVar(name) == "false":
			exit(54)
		if getType(name) == "undefined":
			return "false"
	else:
		if isConst(type) == "false":
			exit(53)
	return "true"
	
def getSymbolType(name,type):
	if type == "var":
		if findVar(name) == "false":
			exit(54)
		return getType(name)
	else:
		return type
		
def getSymbolValue(name,type):
	if type == "var":
		name = getValue(name)
		try:
			name = str(name)
			if name == "None":
				name = ""
		except:
			return name
		return name
	else:
		return name

def setSymbolVar(where,type,name):
	setVar(where,getSymbolType(name,type),getSymbolValue(name,type))

def replaceEscape(str):
	my = ""
	for c in str:
		my = my +c
		arr = re.findall('\\\\[0-2][0-9][0-9]',my)
		if len(arr) != 0:
			num = my[-3:]
			my = my[:-4]
			my = my + chr(int(num))
	return my
	
#---------------------#
#---------MAIN--------#
#---------------------#

if len(sys.argv) == 2:
	if sys.argv[1] == "--help":
		print("use: python3 interpret.py [--source=<file>] [--input=<file>]")
		print("at least one of the param --source or --input must be use")
		exit(0)


sourceFile = sys.stdin
inputFile = sys.stdin
stackCall = []
stackData = []
listLabel = []

#check arguments
isSrc = 0
isInput = 0
statiFile = ""
stats = 0
insts = 0
vars = 0
orderStati = []
for arg in sys.argv[1:]:

	if re.match("--source=.+",arg) != None:
		sourceFile = arg.replace("--source=","")
		isSrc = isSrc + 1
		continue
	
	if re.match("--input=.+",arg) != None:
		inputFile = arg.replace("--input=","")
		isInput = isInput + 1
		continue
	
	if re.match("--stats=.+",arg) != None:
		statiFile =  arg.replace("--stats=","")
		stats = stats + 1
		continue
		
	if re.match("--insts",arg) != None:
		orderStati.append("insts")
		insts = insts + 1
		continue
		
	if re.match("--vars",arg) != None:
		orderStati.append("vars")
		vars = vars + 1
		continue
	
	exit(10)

if isSrc > 1:
	exit(10)

if isInput > 1:
	exit(10)

if isInput == 0:
	if isSrc == 0:
		exit(10)

if stats > 1:
	exit(10)
	
if insts > 1:
	exit(10)

if vars > 1:
	exit(10)

if stats == 0:
	if insts == 1:
		exit(10)
	if vars == 1:
		exit(10)
		
#read xml file
try:
	tree = ET.parse(sourceFile)
	root = tree.getroot()
except:
	#print("bad input file")
	exit(31)

#insert all xml data to class instruction
ins = []
i = 0
for instruction in root:
	ins.append(Instuction())
	ins[i].name = instruction.get('opcode')
	ins[i].argc = 0
	ins[i].order = int(instruction.get('order'))
	if instruction.tag != "instruction":
		exit(32)
	j = 0
	for arg in instruction:
		ins[i].argv.append(Argument())
		ins[i].argv[j].type = arg.get('type')
		ins[i].argv[j].name = arg.text
		ins[i].argv[j].order = arg.tag
		ins[i].argc = j+1
		checkLexical(ins[i].argv[j].name,ins[i].argv[j].type)
		if ins[i].argv[j].type == "string":
			if ins[i].argv[j].name != None:
				ins[i].argv[j].name = replaceEscape(ins[i].argv[j].name)
		if re.match("arg[0-9][0-9]*",arg.tag) == None:
			exit(32)
		j = j + 1
	#sort and check argumets of instruction
	ins[i].argv.sort(key=lambda x: x.order)
	cnt = 1
	for arguments in ins[i].argv:
		if arguments.order != "arg" + str(cnt):
			exit(32)
		cnt = cnt + 1
	i = i + 1
#sort and check instruction
ins.sort(key=lambda x: x.order)
cnt = 1
for instruct in ins:
	if cnt != int(instruct.order):
		exit(32)
	cnt = cnt +1
	

#find all label
index = 0
while index < len(ins):
	if ins[index].name == "LABEL":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type != "label":
			exit(53)
		if isContainLabel(ins[index].argv[0].name) == "true":
			exit(52)
			
		item = Label()
		item.name = ins[index].argv[0].name
		item.index = index
		listLabel.append(item)
	index = index + 1



countVars = 0
countInsts = 0
#creating all instruction from class instruction
index = 0
while index < len(ins):
	countInsts = countInsts + 1
	#print(ins[index].name)
	if ins[index].name == "DEFVAR":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		addVar(ins[index].argv[0].name,"undefined","undefined")
		countVars = countVars + 1
		index = index + 1
		continue
		
	if ins[index].name == "READ":
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if ins[index].argv[1].type != "type":
			exit(53)
		try:
			loaded = input()
		except:
			loaded = ""
		
		loaded = convert(loaded,ins[index].argv[1].name)
		setVar(ins[index].argv[0].name,ins[index].argv[1].name,loaded)
		index = index + 1
		continue
		
	if ins[index].name == "WRITE":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type == "var":
			if findVar(ins[index].argv[0].name) == "false":
				exit(54)
			if getType(ins[index].argv[0].name) == "undefined":
				exit(56)
			value = getValue(ins[index].argv[0].name)
			if getType(ins[index].argv[0].name) == "nil":
				index = index + 1
				continue
			print(value,end='')
		else:
			if isConst(ins[index].argv[0].type) == "false": 
				exit(53)
			value = ins[index].argv[0].name
			if ins[index].argv[0].type == "nil":
				index = index + 1
				continue
			print(value,end='')
		index = index + 1
		continue
	
	if ins[index].name == "MOVE":
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if ins[index].argv[1].type == "var":
			
			if findVar(ins[index].argv[1].name) == "false":
				exit(54)
			if getType(ins[index].argv[1].name) == "undefined":
				exit(56)
			setVar(ins[index].argv[0].name,getType(ins[index].argv[1].name),getValue(ins[index].argv[1].name))
		else: 
			if isConst(ins[index].argv[1].type) == "false":
				exit(53)
			setVar(ins[index].argv[0].name,ins[index].argv[1].type,ins[index].argv[1].name)
		index = index + 1
		continue
		
	if ins[index].name == "CREATEFRAME":
		if ins[index].argc != 0:
			exit(32)
		#TF is now enable
		tmpisenabled[0] = "true"
		#remove previous content
		for tobj in tmpvar:
			tmpvar.pop()
			
		index = index + 1
		continue
	
	if ins[index].name == "PUSHFRAME":
		if ins[index].argc != 0:
			exit(32)
		#create new LF frame
		localvar.append([])
		localindex[0] = localindex[0] + 1
		
		#check if was CREATEFRAME before this call
		if tmpisenabled[0] == "false":
			exit(55)
		
		#copy TF to actual LF 
		for tobj in tmpvar:
			addVar("LF"+ tobj.name[2:], tobj.type, tobj.value)
			
		#TF is now disable
		tmpisenabled[0] = "false"
		index = index + 1
		continue
		
	if ins[index].name == "POPFRAME":
		if ins[index].argc != 0:
			exit(32)
		#TF is now enable
		tmpisenabled[0] = "true"
		
		#copy LF to actual TF
		for tobj in localvar[localindex[0]]:
			if findVar("TF"+ tobj.name[2:]) == "false":
				addVar("TF"+ tobj.name[2:], tobj.type, tobj.value)
			else:
				setVar("TF"+ tobj.name[2:], tobj.type, tobj.value)
			
		#remove LF frame
		localvar.pop()
		localindex[0] = localindex[0] - 1
		if localindex[0] < 0:
			exit(55)
			
		index = index + 1
		continue
		
	if ins[index].name == "CALL":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type != "label":
			exit(53)
		
		#save increment index to stack(list)
		stackCall.append(index+1)
		
		#jump to label
		index = getLabelIndex(ins[index].argv[0].name)
		continue
	
	if ins[index].name == "LABEL":
		index = index + 1
		continue
	
	if ins[index].name == "RETURN":
		if ins[index].argc != 0:
			exit(32)
		try:
			index = stackCall.pop()
		except:
			#if strack is empty
			exit(56)
		continue
	
	if ins[index].name == "PUSHS":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type == "var":
			if findVar(ins[index].argv[0].name) == "false":
				exit(54)
			if getType(ins[index].argv[0].name) == "undefined":
				exit(56)
			if getType(ins[index].argv[0].name) == "nil":
				exit(53)
			insertValue = Argument()
			insertValue.name = getValue(ins[index].argv[0].name)
			insertValue.type = getType(ins[index].argv[0].name)
			stackData.append(insertValue)
		else:
			if isConst(ins[index].argv[0].type) == "false":
				exit(53)
			if ins[index].argv[0].type == "nil":
				exit(53)
			insertValue = Argument()
			insertValue.name = ins[index].argv[0].name
			insertValue.type = ins[index].argv[0].type
			stackData.append(insertValue)
		index = index + 1
		continue
	
	if ins[index].name== "POPS":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type != "var":	
			exit(53)
		if findVar(ins[index].argv[0].name) == "false":
			exit(54)
		insertValue = Argument()
		try:
			insertValue = stackData.pop()
		except:
			exit(56)
			
		setVar(ins[index].argv[0].name,insertValue.type,insertValue.name)
		
		index = index + 1
		continue
				
	if ins[index].name == "ADD" or ins[index].name == "SUB" or ins[index].name == "MUL" or ins[index].name == "IDIV":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "int": 
			exit(53)
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "int": 
			exit(53)
		
		if ins[index].name == "ADD":
			value = int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)) + int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type))
		if ins[index].name == "SUB":
			value = int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)) - int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type))
		if ins[index].name == "MUL":
			value = int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)) * int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type))
		if ins[index].name == "IDIV":
			if int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)) == 0:
				exit(57)
			value = int(int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)) / int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)))
		setSymbolVar(ins[index].argv[0].name,"int",value)
	
		index = index + 1
		continue
	
	if ins[index].name == "LT" or ins[index].name== "GT" or ins[index].name == "EQ":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		
		type1 = getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type)
		type2 = getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type)
		
		if type1 != "nil":
			if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
				exit(56)
		
		if type2 != "nil":
			if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
				exit(56)
		
		if type1 != type2:
			if type1 != "nil":
				if type2 != "nil":
					exit(53)
		
		if ins[index].name == "LT":
			if type1 == "nil" or type2 == "nil":
				exit(53)
			if getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type) < getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type):
				setSymbolVar(ins[index].argv[0].name,"bool","true")
			else:
				setSymbolVar(ins[index].argv[0].name,"bool","false")
			
		if ins[index].name == "GT":	
			if type1 == "nil" or type2 == "nil":
				exit(53)
			if getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type) > getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type):
				setSymbolVar(ins[index].argv[0].name,"bool","true")
			else:
				setSymbolVar(ins[index].argv[0].name,"bool","false")
		
		if ins[index].name == "EQ":
			if getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type) == getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type):
				setSymbolVar(ins[index].argv[0].name,"bool","true")
			else:
				setSymbolVar(ins[index].argv[0].name,"bool","false")
				
		index = index + 1
		continue
		
	if ins[index].name == "AND" or ins[index].name == "OR":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "bool":
			exit(53)
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "bool":
			exit(53)
		
		if getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type) == "true":
			val1 = True
		else:
			val1 = False
		if getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type) == "true":
			val2 = True
		else:
			val2 = False
	
		if ins[index].name == "AND":
			if val1 and val2:
				setSymbolVar(ins[index].argv[0].name,"bool","true")
			else:
				setSymbolVar(ins[index].argv[0].name,"bool","false")
				
		if ins[index].name == "OR":
			if val1 or val2:
				setSymbolVar(ins[index].argv[0].name,"bool","true")
			else:
				setSymbolVar(ins[index].argv[0].name,"bool","false")		
				
		index = index + 1
		continue
	
	if ins[index].name == "NOT":
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "bool":
			exit(53)
			
		if getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type) == "true":
			setSymbolVar(ins[index].argv[0].name,"bool","false")
		else:
			setSymbolVar(ins[index].argv[0].name,"bool","true")
			
		index = index + 1
		continue
		
	if ins[index].name == "INT2CHAR":	
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "int":
			exit(53)
			
		value = int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type))
		if value > 256 or value < 0:
			exit(58)
		
		value = chr(value)
		
		setSymbolVar(ins[index].argv[0].name,"string",value)
		index = index + 1
		continue
	
	if ins[index].name == "STRI2INT":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)	
		
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "string":
			exit(53)
		
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "int":
			exit(53)
		
		ind = int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type))
		str = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
		
		if ind > len(str)-1 or ind < 0:
			exit(58)
		
		value = ord(str[ind])
		setSymbolVar(ins[index].argv[0].name,"int",value)
		
		index = index + 1
		continue
	
	if ins[index].name == "CONCAT":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		
		
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "string":
			exit(53)
			
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "string":
			exit(53)
			
		str1 = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
		str2 = getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)
		
		setSymbolVar(ins[index].argv[0].name,"string",str1+str2) 
		index = index + 1
		continue
	
	if ins[index].name == "STRLEN":
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "string":
			exit(53)
		
		value = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
		if value == None:
			value = 0
		else:
			value = len(value)
		setSymbolVar(ins[index].argv[0].name,"int",value) 
		
		index = index + 1
		continue
		
	if ins[index].name == "GETCHAR":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
			
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "string":
			exit(53)
			
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "int":
			exit(53)
		
		ind = int(getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type))
		str = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
	
		if ind > len(str)-1 or ind < 0:
			exit(58)
		
		setSymbolVar(ins[index].argv[0].name,"string",str[ind])
		
		index = index + 1
		continue
		
	if ins[index].name == "SETCHAR":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		
		if isSymbolDefine(ins[index].argv[0].name,ins[index].argv[0].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[0].name,ins[index].argv[0].type) != "string":
			exit(53)
		if getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type) != "int":
			exit(53)
		if getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type) != "string":
			exit(53)
		
		ind = int(getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type))
		str = getSymbolValue(ins[index].argv[0].name,ins[index].argv[0].type)
		try:
			char = getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)[0]
		except:
			exit(58)
		if ind > len(str)-1 or ind < 0:
			exit(58)
		#change one char on index
		new = list(str)
		new[ind] = char
		str = ''.join(new)
		setSymbolVar(ins[index].argv[0].name,"string",str)
		
		index = index + 1
		continue
	
	if ins[index].name == "TYPE":
		if ins[index].argc != 2:
			exit(32)
		if ins[index].argv[0].type != "var":
			exit(53)
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			setSymbolVar(ins[index].argv[0].name,"string","") 
			index = index + 1
			continue
			
		value = getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type)
		setSymbolVar(ins[index].argv[0].name,"string",value) 
		
		index = index + 1
		continue
	
	if ins[index].name == "JUMP":
		if ins[index].argc != 1:
			exit(32)
		if ins[index].argv[0].type != "label":
			exit(53)
		
		#jump to label
		index = getLabelIndex(ins[index].argv[0].name)
		continue
	
	if ins[index].name == "JUMPIFEQ":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "label":
			exit(53)
		
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		type1 = getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type)	
		type2 = getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type)
	
		#check if label exits
		getLabelIndex(ins[index].argv[0].name)
		
		if type1 != type2:
			exit(53)
		
		val1 = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
		val2 = getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)
		
		if val1 == val2:
			index = getLabelIndex(ins[index].argv[0].name)
		else:
			index = index + 1
		continue
	
	
	if ins[index].name == "JUMPIFNEQ":
		if ins[index].argc != 3:
			exit(32)
		if ins[index].argv[0].type != "label":
			exit(53)
		
		if isSymbolDefine(ins[index].argv[1].name,ins[index].argv[1].type) == "false":
			exit(56)
		if isSymbolDefine(ins[index].argv[2].name,ins[index].argv[2].type) == "false":
			exit(56)
		
		type1 = getSymbolType(ins[index].argv[1].name,ins[index].argv[1].type)	
		type2 = getSymbolType(ins[index].argv[2].name,ins[index].argv[2].type)
		
		#check if label exits
		getLabelIndex(ins[index].argv[0].name)
		
		if type1 != type2:
			exit(53)
		
		val1 = getSymbolValue(ins[index].argv[1].name,ins[index].argv[1].type)
		val2 = getSymbolValue(ins[index].argv[2].name,ins[index].argv[2].type)
		
		if val1 != val2:
			index = getLabelIndex(ins[index].argv[0].name)
		else:
			index = index + 1
		continue
	
	if ins[index].name == "EXIT":
		if ins[index].argc != 1:
			exit(32)
		if isSymbolDefine(ins[index].argv[0].name,ins[index].argv[0].type) == "false":
			exit(56)
		
		if getSymbolType(ins[index].argv[0].name,ins[index].argv[0].type) != "int":
			exit(53)
		
		value = getSymbolValue(ins[index].argv[0].name,ins[index].argv[0].type)
		if int(value) > 49 or int(value) < 0:
			exit(57)
		
		exit(int(value))
	
	if ins[index].name == "DPRINT":
		if ins[index].argc != 1:
			exit(32)
			
		if isSymbolDefine(ins[index].argv[0].name,ins[index].argv[0].type) == "false":
			exit(56)
		
		value =  getSymbolValue(ins[index].argv[0].name,ins[index].argv[0].type)
		sys.stderr.write(value)
		index = index + 1
		continue
		
	if ins[index].name == "BREAK":
		index = index + 1
		continue
	
	exit(32)
	break

#stati
first = None
second = None
if stats == 1:
	try:
		second = orderStati.pop()
		first = orderStati.pop()
	except:
		pass
	file = open(statiFile, "w")
	if first != None:
		if first == "insts":
			file.write(str(countInsts))
			file.write('\n')
		if first == "vars":
			file.write(str(countVars))
			file.write('\n')
	if second != None:
		if second == "insts":
			file.write(str(countInsts))
			file.write('\n')
		if second == "vars":
			file.write(str(countVars))
			file.write('\n')

	