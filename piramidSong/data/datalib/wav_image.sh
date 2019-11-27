#! /bin/bash

TOTAL_SAMPLES=$( ls $1 | grep "wav" | wc -l );

SAMPLES=$(( $(( $TOTAL_SAMPLES / $2 ))  / $3 ));

echo "SAMPLES AMOUNT :	$SAMPLES";

echo "Making room for the images";

#IMAGES_DESTINATION= "images";

#rm -rf "$1/${!IMAGES_DESTINATION}";
#mkdir "$1/${!IMAGES_DESTINATION}";

for INDEX in $(seq 1 $SAMPLES);
do
	echo "SAMPLE #r :	$INDEX";
	echo "";
	for FILE_NAME_WAV in $(ls | grep "_""$INDEX""_");
	do
		echo "CONVERTING >	$FILE_NAME_WAV";
		echo "";
		
		#echo "$1/${!IMAGES_DESTINATION}/${FILE_NAME_WAV%.*}.bmp";		


		arss $FILE_NAME_WAV  --output "$1/images/${FILE_NAME_WAV%.*}.bmp" --analysis --min-freq 27.500 -max 22000 --bpo 120 --pps 441 &
	done;
	wait;
done;
