#!/bin/bash


for product in $(cat products.txt)
do
	echo $product
	sudo mkemlog /tmp/emlog_$product 10240 666 1001

done
