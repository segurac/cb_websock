# cb_websock

## Compilation

sudo apt-get install rapidjson-dev libcpprest-dev

mkdir build
cd build
cmake ../
make

## environment

I prefer using a pypy environment, which for this application is faster than normal python
sudo apt-get install pypy3-dev pypy3 python3-virtualenv virtualenv
virtualenv -p pypy3 venv_pypy
source venv_pypy/bin/activate
pip install mujson

## run

cd build/
cp ../scripts/products.txt
../scripts/launch_db_websocks_to_disk.sh

## Data Format

The script connects to coinbase's websocket event feed for every product defined in product.txt. Raw data is stored as gziped json in the file ./coinbaseDump/yyyy/mm/dd/events_PRODUCT_NAME_0.json.gz

Every time the websocket is disconnected a new file with an incremented index is created, e.g. ./coinbaseDump/yyyy/mm/dd/events_PRODUCT_NAME_1.json.gz. Every day at 00:00h a new directory for this date is created along with a new events file.
