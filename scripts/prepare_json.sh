cat borrar.txt | sed -e 's@\"time\":\"@\"time\":ISODate(\"@g' -e 's@Z\"@Z\")@g' > mytest.json

