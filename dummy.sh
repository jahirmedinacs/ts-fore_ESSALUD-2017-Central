#! /bin/bash

pdftohtml -c -s -i -nomerge -wbt 9999999 $1 | wc -l;
