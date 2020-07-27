cat borrar.txt | sed -e 's@\"time\":\"@\"time\":ISODate(\"@g' -e 's@Z\"@Z\")@g' > mytest.json


zcat $1 | grep -v subscriptions | grep -v -e subscriptions -e sell | sed -e 's@\"time\":\"@\"time\":ISODate(\"@g' -e 's@Z\"@Z\")@g'
