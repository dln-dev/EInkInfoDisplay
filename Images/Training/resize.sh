#!/bin/bash

for file in *.bmp
do
	convert $file -resize 40x40 $file
done
