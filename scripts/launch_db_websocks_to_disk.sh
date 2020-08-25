#!/bin/bash


capture_multilog () {
   product=$1
   while true
    do
        echo "(Re)Starting capture $1"
#         ./cb_websock $product |  multilog s104857600 n1000 '!/bin/gzip'  ./events_$product 
        ./cb_websock $product |  python ../scripts/preprocess_stdin.py coinbaseDump $product 
        sleep 0.5
    done 
}


for product in $(cat products.txt)
do
	echo $product
    capture_multilog $product &
    sleep 0.5
done


wait

