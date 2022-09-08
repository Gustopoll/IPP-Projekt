<?php
class Token
{
	var $name;
	var $id;
	
	function getName()
	{
		if ($this->name == "")
			return -1;
		return $this->name;
	}	
	
	function setName($name)
	{
		$this->name = $name;
	}
	
	function getId()
	{
		return $this->id;
	}	
	
	function setId($id)
	{
		$this->id = $id;
	}
}
//retrun true if is space
//else return false
function isSpace($c)
{
	if ($c == "\n")
		return true;
	if ($c == "\t")
		return true;
	if ($c == " ")
		return true;
	if ($c == "\0")
		return true;
	return false;
}

//get id from name and check if name is 
//correctly written
function getId($name)
{
	if ($name == -1)
		return "end";
	
	if ($name == "\n")
		return "newline";
	$pattern="/([_$&%*!?-]*([a-z]|[A-Z])+)([a-z]|[A-Z]|[_$&%*!?-]|[0-9])*/";
	if (preg_replace($pattern,"",$name) == "")
		return "word";
	
	$pattern="/(LF@|GF@|TF@)([_$&%*!?-]*([a-z]|[A-Z])+)([a-z]|[A-Z]|[_$&%*!?-]|[0-9])*/";
	if (preg_replace($pattern,"",$name) == "")
		return "var";
		
	$pattern= "/(int|string)@((\\\{1}[0-9][0-9][0-9])|([^\\\]))*/";
	if (preg_replace($pattern,"",$name) == "")
		return "const";
	
	if (($name == "bool@true") || ($name == "bool@false") || ($name == "nil@nil"))
		return "const";
	
	if (preg_replace("/\.IPPcode19/i", " ", $name) == " ")
		return "head";
	//this is lex error
	return "unknown";
}

//function to count comment
function countComment()
{
	static $cnt =0;
	$cnt++;
	return $cnt;
}

//return loaded word from file 
function getWord($file)
{
	static $newline = false;

	if ($newline == true)
	{
		$newline = false;
		return "\n";
	}
	
	$word = "";
	while (! feof($file))
	{
		$c = fgetc($file);
		//comment
		if ($c == "#")
		{
			countComment();
			while (! feof($file))
			{
				$c = fgetc($file);
				if ($c == "\n")
				{
					fwrite($file,'\n',1);
					break;
				}
			}
		}
		//end of word
		if (isSpace($c) == true)
			break;
		$word = $word . $c;
	}
	if ($c == "\n")
		$newline = true;
	
	return $word;
}

//create and retrun token
function getToken($file)
{
	$token = new Token();
	$name = getWord($file);
	
	while ($name == "")
	{
		if (feof($file))
			break;
		$name = getWord($file);
	}
	
	$id = getId($name);
	$token->setName($name);
	$token->setId($id);
	return $token;
}

?>