#! /bin/bash

mkdir -p cleaned;

cd ./converteddata

find . -iname "*" | while read FILE_NAME;
do
	(tail -n $(calc $(wc $FILE_NAME | awk '{print $1}') - 3) $FILE_NAME) | sed '/^[,]*$/d' > ../cleaned/$FILE_NAME
done
