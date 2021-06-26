#! /bin/bash

if [ $# -ne 2 ]
	then
		echo "Incorrect args number";
		exit 1
fi

if [ ! -x $1 ] || [ ! -f $1 ]
	then
		echo "First argumen must be a program";
		exit 2
fi

if [ ! -d $2 ]
	then
		echo "Second argument must be a directory";
		exit 3
fi

tmp='tmp'
flag=0
fails=0
passed=0


for file in $2/*.dat;
do
	"./$1" < $file > $tmp
	var=`basename $file .dat`
	
	c=`grep -i -c -x error $2/$var.ans`
#	echo "$c \n"
	if [ $c -ge 1 ]
	then
#		echo "Alarm"
#		echo "$file"
#		echo "testing Error task"
		c=`grep -i -c error $tmp`
		if [ ! $c -eq 1 ]
		then
			echo "--------------------------------------------------------------------------------------------"
			echo "FAILED $file"
			exit 5
		fi
	else
		diff $2/$var.ans $tmp
		if [ $? -ne 0 ]
		then
			echo "--------------------------------------------------------------------------------------------"
			echo "FAILED $file"
			let "fails += 1" # $fails + 1
			let "flag=1"
			#exit 4
		fi
	fi
	if [ $flag -eq 0 ]
	then
		echo "Passed $file test"
		let "passed += 1"
		rm $tmp
	fi
	let " flag = 0 "
done
echo "fails = $fails"
echo "passed = $passed"
exit 0