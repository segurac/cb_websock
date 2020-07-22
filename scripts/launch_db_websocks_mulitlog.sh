#!/bin/bash


for product in $(cat products.txt)
do
	echo $product
	./cb_websock $product |  multilog s104857600 n100 '!/bin/gzip'  ./events_$product &

done
