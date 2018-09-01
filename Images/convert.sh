#!/bin/bash
# converts .bmps in subfolders to monochrome bitmaps
echo "Converting .bmps to monochrome..."

for file in ./[^.]*/*.bmp
do
	echo "converting $file ..."
	convert $file -monochrome $file
done
