#!/usr/bin/php
<?php

class Files
{
	var $fileName;
	var $path;
	var $isOk;
	var $valueRet;
	var $realRet;
	
	function setFileName($fileName){
		$this->fileName = $fileName;
	}
	function getFileName(){
		return $this->fileName;
	}
	
	function setPath($path){
		$this->path = $path;
	}
	function getPath(){
		return $this->path;
	}
	
	function setIsOk($isOk){
		$this->isOk = $isOk;
	}
	function getIsOk(){
		return $this->isOk;
	}
	
	function setValueRet($valueRet){
		$this->valueRet = $valueRet;
	}
	function getValueRet(){
		return $this->valueRet;
	}
	
	function setRealRet($realRet){
		$this->realRet = $realRet;
	}
	function getRealRet(){
		return $this->realRet;	
	}
	
}

function genHead()
{
echo "<html>\n";
echo "<head>\n";
echo "<meta charset=\"UTF-8\">\n";
echo "<title>IPP - Test page</title>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font size=\"15\" color=\"blue\">\n";
echo "<center> Results of all tests:</center></br> </font>\n";
}

function genTotal($succ,$all)
{
	if ($succ == null)
	$succ = 0;
if ($all == null)
	$all = 0;
	if ($all == $succ)
	{
		echo "<font size=\"10\" color=\"green\">\n";
		echo "<center>" . $succ ."/". $all . "passed </center></br> </font>\n";
	}
	else
	{
		echo "<font size=\"10\" color=\"red\">\n";
		echo "<center>" . $succ ."/". $all . "passed </center></br> </font>\n";
	}
}

function genDir($path,$succ,$fail)
{
if ($succ == null)
	$succ = 0;
if ($fail == null)
	$fail = 0;
$all = $fail + $succ;
echo "<font size=\"6\" color=\"darkblue\">\n";
echo "Path and directory -> " . $path .":</br>\n";
if ($all == $succ)
	echo  "<font size=\"6\" color=\"green\">". $succ ."/". $all ." successful </font></br>\n";
else
	echo  "<font size=\"6\" color=\"red\">". $succ ."/". $all ." successful </font></br>\n";
echo "</font>\n";
}

function genTail()
{
echo "</body>\n";
echo "</html>\n";
}

function printHelp()
{
	echo "HELP: todo\n";
	exit(0);
}

function checkArgument($arr)
{
	multipleArgument($arr);
	
	//check --help
	if ($arr[0] == 1)
	{
		for ($i = 1; $i < count($arr);$i++)
			if ($arr[$i] > 0)
			{
				echo "Ivalid arguments\n";
				exit(1);
			}
		printHelp();	
	}
	//parse-only
	if ($arr[5] == 1)
	{
		if (($arr[6] == 1) || ($arr[4] == 1))
		{
			echo "parse only cannot have int-only and --int-script=[file]\n";
			exit(1);
		}
	}
	
	//int-only
	if ($arr[6] == 1)
	{
		if (($arr[5] == 1) || ($arr[3] == 1))
		{
			echo "int only cannot have parse-only and --parse-script=[file]\n";
			exit(1);
		}
	}
	
}

function multipleArgument($arr)
{
	for ($i = 0; $i < count($arr);$i++)
		if ($arr[$i] > 1)
		{
			echo "bad arguments\n";
			exit(1);
		}
}	

function createFile($file,$msg)
{
	$f = @fopen($file,"rw");
		if ($f == null)
		{
			$f = @fopen($file,"w");
			fwrite($f,$msg);
		}
	fclose($f);
}

function loadfile($path)
{
	$files = @scandir($path);
	if ($files == null)
	{
		echo "bad path to file\n";
		exit(1);
	}
	return $files;
}

function getTestFiles($path, $isRecursive)
{
	$returnFiles = array();
	
	//remove last slah if exist
	if ($path[strlen($path)-1] != '/')
		$path = $path . "/";
	
	$files = loadfile($path);
	
	$i = 0;
	foreach ($files as $item)
	{
		if ($isRecursive == true)
			if ( is_dir($path . $item) )
			{
				if (($item == ".") || ($item == ".."))
					continue;
				$tempFile = getTestFiles($path . $item, $isRecursive);
				foreach($tempFile as $tmp)
				{
					$returnFiles[$i] = $tmp;
					$i++;
				}
			
			}
			
		if (preg_replace("/.+\.src/", " ", $item) == " ")
		{
			$returnFiles[$i] = new Files();
			$returnFiles[$i]->setPath($path);
			
			$returnFiles[$i]->setFileName(substr($item,0,-4));
			
			createFile($returnFiles[$i]->getPath(). $returnFiles[$i]->getFileName() . ".out","");
			createFile($returnFiles[$i]->getPath(). $returnFiles[$i]->getFileName() . ".in","");
			createFile($returnFiles[$i]->getPath(). $returnFiles[$i]->getFileName() . ".rc",0);
			
			$i++;	
		}
	}
	return $returnFiles;
}

function compareFile($file1, $file2)
{
	if (file_get_contents($file1) == file_get_contents($file2))
		return true;
	else
		return false;
}

$arrOfArg = array(0,0,0,0,0,0,0);
$path = "./";
$parsefile = "./parse.php";
$interfile = "./interpret.py";
$isRecursive = false;
$parseOnly = false;
$interpretOnly = false;

$skip_name_file = true;
foreach($argv as $value)
{
	if ($skip_name_file == true)
	{
		$skip_name_file = false;
		continue;
	}
	
  if ($value == "--help")
  {
	$arrOfArg[0]++;
	continue;
  }
  
  if (preg_replace("/--directory=.+/", " ", $value) == " ")
  {
	$path = preg_replace("/--directory=/", "", $value);
	$arrOfArg[1]++;
	continue;
  }
  
  if (preg_replace("/--recursive/", " ", $value) == " ")
  {
	$isRecursive = true;
	$arrOfArg[2]++;
	continue;
  }
  
  if (preg_replace("/--parse-script=.+/", " ", $value) == " ")
  {
	$parsefile = preg_replace("/--parse-script=/", "", $value);
	$arrOfArg[3]++;
	continue;
  }
  
  if (preg_replace("/--int-script=.+/", " ", $value) == " ")
  {
	$interfile = preg_replace("/--int-script=/", "", $value);
	$arrOfArg[4]++;
	continue;
  }

  if (preg_replace("/--parse-only/", " ", $value) == " ")
  {
	 $parseOnly = true;
	 $arrOfArg[5]++;
	 continue;	 
  }
  
  if (preg_replace("/--int-only/", " ", $value) == " ")
  {
	$interpretOnly = true;
	$arrOfArg[6]++;
	continue;
  }
  echo $value ." is not valid argument\n";
  exit(10);
}

checkArgument($arrOfArg);

$testFiles = getTestFiles($path,$isRecursive);
 $succTest = array();
  $failTest = array();
  $totalTests = 0;
  $totalSucc = 0;

//parse only
if ($parseOnly == true)
	foreach($testFiles as $one)
	{
		exec("php ". $parsefile ." < ". $one->getPath() . $one->getFileName() . ".src" ,$out,$returnValue);
		$one->setValueRet($returnValue);
		$one->setRealRet(file_get_contents($one->getPath() . $one->getFileName(). ".rc"));
		
		if ($one->getRealRet() == $one->getValueRet())
		{
			$one->setIsOk("true");
		}
		else 
		{
			$one->setIsOk("false");
		}
		
		if ($one->getIsOk() == "true")
		{
			$succTest[$one->getPath()]++;
			$totalSucc++;
		}
		else
			$failTest[$one->getPath()]++;
		$totalTests++;
		
	}


//interpret only
if ($interpretOnly == true)
	foreach($testFiles as $one)
	{
		$tempfile = @fopen("tempfile.temp","w");
		
		exec("python3 ". $interfile ." --source=" . $one->getPath() . $one->getFileName() .".src <" . $one->getPath() . $one->getFileName() . ".in >tempfile.temp", $return ,$returnValue);
		$one->setValueRet($returnValue);
		$one->setRealRet(file_get_contents($one->getPath() . $one->getFileName(). ".rc"));
		
		if ($one->getRealRet() == $one->getValueRet())
				$one->setIsOk("true");
		else 
				$one->setIsOk("false");
		
		$eq = compareFile("tempfile.temp",$one->getPath() . $one->getFileName(). ".out");
		if ($eq == false)
			$one->setIsOk("false");
		
		if ($one->getIsOk() == "true")
		{
			$succTest[$one->getPath()]++;
			$totalSucc++;
		}
		else
			$failTest[$one->getPath()]++;
		$totalTests++;
		
		unlink("tempfile.temp");
	}

 //both - parse and interpret
if (($interpretOnly == false) && ($parseOnly == false))
	foreach($testFiles as $one)
	{
		$tempfile = @fopen("tempfile.temp","w");
		$tempfile = @fopen("tempfile2.temp","w");
		
		exec("php ". $parsefile ." < ". $one->getPath() . $one->getFileName() . ".src >tempfile.temp" ,$out,$returnValue);
		exec("python3 ". $interfile ." --source=tempfile.temp <" . $one->getPath() . $one->getFileName() . ".in >tempfile2.temp", $return ,$returnValue);
		$one->setValueRet($returnValue);
		$one->setRealRet(file_get_contents($one->getPath() . $one->getFileName(). ".rc"));
		
		if ($one->getRealRet() == $one->getValueRet())
					$one->setIsOk("true");
			else 
					$one->setIsOk("false");
			
			$eq = compareFile("tempfile2.temp",$one->getPath() . $one->getFileName(). ".out");
			if ($eq == false)
				$one->setIsOk("false");
		
		if ($one->getIsOk() == "true")
		{
			$succTest[$one->getPath()]++;
			$totalSucc++;
		}
		else
			$failTest[$one->getPath()]++;
		$totalTests++;
		unlink("tempfile.temp");
		unlink("tempfile2.temp");
	}

if ($testFiles == null)
	{
	genHead();
	echo "<font size=\"5\" color=\"red\"> no tests to check </br></font>\n";
	genTail();
	exit(0);
	}

usort($testFiles, function($a, $b)
{
    return strcmp($a->path, $b->path);
});

//generate HTML5

genHead();
genTotal($totalSucc,$totalTests);
$currentDir = $testFiles[0]->getPath();

$count = 1;
genDir($currentDir,$succTest[$currentDir],$failTest[$currentDir]);
foreach($testFiles as $one)
{
	if ($currentDir != $one->getPath())
	{
		$currentDir = $one->getPath();
		genDir($one->getPath(),$succTest[$one->getPath()],$failTest[$one->getPath()]);
		$count = 1;
	}

echo "<font size=\"5\" color=\"black\">" .$count . ". test: " . $one->getFileName() ."-> </font>\n";
if ($one->getIsOk() == "true")
	echo "<font size=\"5\" color=\"green\"> successful </br></font>\n";
else 
{
	echo "<font size=\"5\" color=\"red\"> fail </font>\n";
	if ( $one->getRealRet() == $one->getValueRet() )
		echo "<font size=\"5\" color=\"black\"> different output </br></font>\n";
	else
		echo "<font size=\"5\" color=\"black\"> retrun: " . $one->getValueRet() . " (expect" . $one->getRealRet() . ")</br></font>\n";
	
}
$count++;
	//echo $one->getPath() . " " .$one->getFileName() . " " . $one->getIsOk() . "\n";
} 
genTail(); 

?>