<?php

function check_bonus_statp(array $param, $cparam)
{
	$i = 1;
	$infile = 0;
	$loc = 0;
	$comm = 0;
	$lab = 0;
	$jump = 0;
	
	while ($i != $cparam)
	{
		if (preg_replace('/--stats=.+/', ' ', $param[$i]) == " ")
		{
			$infile++;
			$outfile = preg_replace('/--stats=/', '', $param[$i]);
			$i++;
			continue;
		}
		
		if ($param[$i] == "--loc")
		{
			$loc++;
			$i++;
			continue;
		}
		if ($param[$i] == "--comments")
		{
			$comm++;
			$i++;
			continue;
		}	
		if ($param[$i] == "--labels")
		{
			$lab++;
			$i++;
			continue;
		}
		if ($param[$i] == "--jumps")
		{
			$jump++;
			$i++;
			continue;
		}
		//if not contain above arguments, then call exit
		exit(NOPARAM);
	}
	
	if ($infile != 1 )
		exit(NOPARAM);
	if ($loc >= 2)
		exit(NOPARAM);
	if ($comm >= 2)
		exit(NOPARAM);
	if ($lab >= 2)
		exit(NOPARAM);
	if ($jump >= 2)
		exit(NOPARAM);
	
	return $outfile;
}

function generate_bonus_statp(array $param, $cparam, $filename)
{
	$i = 1;
	$output_string = "";
	$file = @fopen($filename,"w");
	if ($file == NULL)
		exit(ERROUT);
	
	while ($i != $cparam)
	{
		if ($param[$i] == "--loc")
		{
			//echo "--loc = " . (countInstruction()-1) ."\n";
			$output_string = $output_string . (countInstruction()-1) . "\n";
		}
		if ($param[$i] == "--comments")
		{
			//echo "--comment = " . (countComment()-1) ."\n";
			$output_string = $output_string . (countComment()-1) . "\n";
		}
		if ($param[$i] == "--labels")
		{
			//echo "--label = " . (countLabel("LABEL","###")-1) ."\n";
			$output_string = $output_string . (countLabel("LABEL","###")-1) . "\n";
		}
		if ($param[$i] == "--jumps")
		{
		 //echo "--jumps = " . (countJump("LABEL","###")-1) ."\n";
		 $output_string = $output_string . (countJump("LABEL","###")-1) . "\n";
		}
		file_put_contents($filename,$output_string);
		$i++;
	}
	
	fclose($file);
}

?>
