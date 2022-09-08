#!/usr/bin/php

<?php
define("NOPARAM",10);
define("ERRIN",11);
define("ERROUT",12);
define("INTER_ERROR",99);
define("NOHEAD",21);

include 'lexical.php';
include 'generat.php';
include 'syntax.php';
include 'statp.php';

//argument help
if ($argv[1] == "--help")
{
	if ($argc > 2)
		exit(NOPARAM);
	echo "Use: php parse.php <name-file>\n";
	exit(0);
}

//bonus
if ($argc > 1)
	 $outfile = check_bonus_statp($argv,$argc);

//set stdin and input file
$namefile = 'php://stdin';
$file = @fopen($namefile,"r");

if ($file == NULL)
{
	echo "Bad file\n";
	exit(ERRIN);
}

//create array of class of token
$token = array();
$i = 0;
 while (! feof ($file))
 {
   $token[$i] = new Token();
   $token[$i] = getToken($file);
   $i++;
 }
 $i = 0;
 

 
 $washead = false;
 $isfirst = true;
  //check head or error 23
 while ($token[$i]->getName() != -1)
 {
	if ($token[$i]->getId() == "head")
		$washead = true;
	
	if ($token[$i]->getId() == "unknown")
	{
		if (($isfirst == true) && ($washead == false))
			exit (NOHEAD);
		else
			exit (23);
	}
	if ($token[$i]->getId() != "newline")
		$isfirst = false;
	
	$i++;
 }	 
 if ($washead == false )
	exit(NOHEAD); 


check_syntax($token);

generate($token);

//bonus
if ($argc > 1)
	generate_bonus_statp($argv,$argc,$outfile);

fclose($file);
?>