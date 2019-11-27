#! /bin/bash

for f in *;
    do
		ffmpeg -i "$f" "${f%.*}.wav";
    done
