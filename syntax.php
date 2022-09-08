<?php
function countLabel($instruction, $label)
{
	static $count = 0;
	static $labels = array();
	$contain = false;
	if (preg_replace("/(LABEL)/i", " ", $instruction) == " ")
	{
		foreach ($labels as $item)
			if ($item == $label)
				$contain = true;
		
		if ($contain == false)
		{
			$labels[$count] = $label;
			$count++;
		}
	}
		return $count;
}

function countJump($instruction)
{
	static $count = 1;
	if (preg_replace("/(JUMP)/i", " ", $instruction) == " ")
		$count++;
	return $count;
}

//chceck syntax of array of token 
function check_syntax(array $token)
{
	$j = 0;
	$state = 10;
	while ($token[$j]->getName() != -1)
		{
			switch ($state)
			{
				case 0:
					if ($token[$j]->getId() == "newline")
					{
							$state = 0;
							$j++;
							break;
					}
					if (preg_replace("/(CREATEFRAME|PUSHFRAME|POPFRAME|RETURN|BREAK)/i", " ", $token[$j]->getName()) == " ")
					{
							$state = 1;
							$j++;
							break;
					}			
					if (preg_replace("/(CALL|LABEL|JUMPIFNEQ|JUMPIFEQ|JUMP)/i", " ", $token[$j]->getName()) == " ")
					{
							$state = 2;
							$j++;
							break;
					}			
					if (preg_replace("/(PUSHS|WRITE|EXIT|DPRINT)/i", " ", $token[$j]->getName()) == " ")
					{
							$state = 5;
							$j++;
							break;
					}
					if (preg_replace("/(MOVE|DEFVAR|POPS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|CONCAT|STRLEN|READ|GETCHAR|SETCHAR|TYPE)/i", " ", $token[$j]->getName()) == " ")
					{
							$state = 6;
							$j++;
							break;
					}
					if ($token[$j]->getId() == "head")
					{
							$state = 0;
							$j++;
							break;
					}
					
					exit(22);
					break;
					
				case 1:
					if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
					{
						$state = 0;
						$j++;
					}
					else
						exit(23);
					break;
				case 2:
					if ($token[$j]->getId() == "word")
					{
						$token[$j]->setId("label");
						$state = 3;
						$j++;
					}
					else
						exit(23);
					break;
				case 3:
					if (preg_replace("/(CALL|LABEL|JUMP)/i", " ", $token[$j-2]->getName()) == " ")
					{	
						if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
						{
							countLabel($token[$j-2]->getName(),$token[$j-1]->getName());
							countJump($token[$j-2]->getName());
							$state = 0;
							$j++;
						}
						else
							exit(23);
						break;
					} 
					if (($token[$j]->getId() == "var") || ($token[$j]->getId() == "const"))
					{
						$state = 4;
						$j++;
					}
					else
						exit(23);
					break;
				case 4:
					if (($token[$j]->getId() == "var") || ($token[$j]->getId() == "const"))
					{
						if (($token[$j+1]->getId() == "newline") || ($token[$j+1]->getId() == "end"))
						{
							$state = 0;
							$j++;
						}
						else
							exit(23);
					}
					else
						exit(23);
					break;
				case 5:
					if (($token[$j]->getId() == "var") || ($token[$j]->getId() == "const"))
					{
						$state = 0;
						$j++;
					}
					else
						exit(23);
					break;
				case 6:
					if ($token[$j]->getId() == "var")
					{
						$state = 7;
						$j++;
					}
					else
						exit(23);
					break;
				case 7:
					if (preg_replace("/(DEFVAR|POPS)/i", " ", $token[$j-2]->getName()) == " ")
					{
						if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
						{
							$state = 0;
							$j++;
						}
						else
							exit(23);
						break;
					}
					if (preg_replace("/(READ)/i", " ", $token[$j-2]->getName()) == " ")
					{
						if (preg_replace("/(STRING|INT|FLOAT|BOOL)/i", " ", $token[$j]->getName()) == " ")
						{
							$state = 8;
							$j++;
						}
						else
							exit(23);
						break;
					}
					if (($token[$j]->getId() == "var") || ($token[$j]->getId() == "const"))
					{
						$state = 9;
						$j++;
					}
					else	
						exit(23);
					break;
				case 8:
					if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
					{
						$state = 0;
						$j++;
					}
					else
						exit(23);
					break;
				case 9:
					if (preg_replace("/(MOVE|INT2CHAR|STRLEN|TYPE|NOT)/i", " ", $token[$j-3]->getName()) == " ")
					{
						if (($token[$j]->getId() == "newline") || ($token[$j]->getId() == "end"))
						{
						$state = 0;
						$j++;
						}
					else
						exit(23);
					break;	
					}
					if (($token[$j]->getId() == "var") || ($token[$j]->getId() == "const"))
					{
						if (($token[$j+1]->getId() == "newline") || ($token[$j+1]->getId() == "end"))
						{
							$state = 0;
							$j++;
						}
						else
							exit(23);
						break;
					}
					else	
						exit(23);
					break;
				case 10:
					if ( $token[$j]->getId() == "head")
					{
						$state = 0;
						$j++;
						break;
					}
				
					if ($token[$j]->getId() == "newline")
					{
						$state = 10;
						$j++;
						break;
					}
					exit(NOHEAD);
					break;
				
			}
			
		}
}
?>
