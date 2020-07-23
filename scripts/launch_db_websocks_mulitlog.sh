#!/bin/bash


capture_multilog () {
   product=$1
   while true
    do
        echo "(Re)Starting capture $1"
        ./cb_websock $product |  multilog s104857600 n1000 '!/bin/gzip'  ./events_$product 
        sleep 0.5
    done 
}


for product in $(cat products.txt)
do
	echo $product
# 	./cb_websock $product |  multilog s104857600 n1000 '!/bin/gzip'  ./events_$product &
    capture_multilog $product &
done


# function killstuff {
#   jobs -p | xargs kill
# }
# 
# trap killstuff SIGINT
# jobs -l
# jobs -p

wait

