<?php

function genHead()
{
	echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" . "\n";
	echo "<program language=\"IPPcode19\">" . "\n";
}

function countInstruction()
{
	static $count = 0;
	$count++;
	return $count;
}

function genInstruction($ins)
{
	echo "\t<instruction order=\"" . countInstruction() . "\" opcode=\"" . strtoupper($ins) . "\">\n";
}

function genEndInstruction()
{
	echo "\t</instruction>\n";
}

function getNameType($name)
{
	if ($name->getId() == "label")
		return "label";
	
	if ($name->getId() == "var")
		return "var";

	if (preg_replace('/int@.*/', ' ', $name->getName()) == " ")
		return "int";
	
	if (preg_replace('/float@.*/', ' ', $name->getName()) == " ")
		return "float";
	
	if (($name->getName() == "bool@true") || ($name->getName() == "bool@false"))
		return "bool";
		 
	if (preg_replace('/string@.*/', ' ', $name->getName()) == " ")
		return "string"; 
	
	if ($name->getName() == "nil@nil")
		return "nil";
	
	return "type";
}

function removeBadchar($changed)
{
	$changed = preg_replace('/&/', '&amp;', $changed);
	$changed = preg_replace('/</', '&lt;', $changed);
	$changed = preg_replace('/>/', '&gt;', $changed);
	$changed = preg_replace('/"/', '&quot;', $changed);
	$changed = preg_replace("/'/", '&apos;', $changed);
	return $changed;
}

//generate argumet
function genArg($arg,$num)
{
	$type = getNameType($arg);
	if ($type == "int")
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . preg_replace('/int@/', '', $arg->getName()) ."</arg" .$num. ">\n";
	
	if ($type == "bool")
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . preg_replace('/bool@/', '', $arg->getName()) ."</arg" .$num. ">\n";
	
	if ($type == "float")
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . preg_replace('/float@/', '', $arg->getName()) ."</arg" .$num. ">\n";
	
	if ($type == "nil") 
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . preg_replace('/nil@/', '', $arg->getName()) ."</arg" .$num. ">\n";
	
	if (($type == "label") || ($type == "type"))
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . $arg->getName() ."</arg" .$num. ">\n";
		
	if ($type == "string")
	{
		$changed = removeBadchar($arg->getName());
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . preg_replace('/string@/', '', $changed) ."</arg" .$num. ">\n";
	}	
	
	if ($type == "var")
	{
		$changed = removeBadchar($arg->getName());
		echo "\t\t<arg" .$num." type=\"" . $type . "\">" . $changed ."</arg" .$num. ">\n";
	}

}

function generate(array $token)
{
	genHead();
	
	$state = 0;
	$j = 0;
	$count_arg = 1;
	while ($token[$j]->getName() != -1)
		switch ($state)
		{
			case 0:
				if ( $token[$j]->getId() == "head")
					{
						$state = 1;
						$j++;
						break;
					}
				
				if ($token[$j]->getId() == "newline")
					{
						$state = 0;
						$j++;
						break;
					}
				break;
				
			case 1:
				if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
				{
					$state = 1;
					$j++;
					break;
				}
				
				genInstruction($token[$j]->getName());
				$j++;
				$state = 2;
				break;
			case 2: //argument
				if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
				{
					$state = 1;
					$j++;
					genEndInstruction();
					break;
				}
				
				genArg($token[$j],$count_arg);
				
				if (($token[$j+1]->getId() == "newline") || ($token[$j+1]->getId() == "end"))
				{
					$state = 1;
					$j++;
					$count_arg = 1;
					genEndInstruction();
					break;
				}
				$count_arg++;
				$j++;
				$state = 2;
				break;	
		}
		
		if ($j >= 1)
			if ($token[$j-1]->getId() != "newline")
				genEndInstruction();
		
	
	echo "</program>\n";
	
}

?>