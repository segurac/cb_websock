#!/bin/bash


for product in $(cat products.txt)
do
	echo $product
	cat /tmp/emlog_$product | python ./store_from_stdin.py $product &

done
