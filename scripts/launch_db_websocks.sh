#!/bin/bash


for product in $(cat products.txt)
do
	echo $product
	./cb_websock $product > /tmp/emlog_$product &

done
