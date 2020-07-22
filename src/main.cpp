#include "Websock.h"
#include <iostream>
#include <chrono>
#include <thread>

int main(int argc, const char *argv[])
{
  std::vector<std::string> channels = {"full"};
//   std::string product_id = "BTC-USD";
  std::string product_id = argv[1];
  std::string uri = "wss://ws-feed.pro.coinbase.com";
  Websock sock(channels, product_id, uri);
  sock.Connect();
  while(true)
  {
    std::this_thread::sleep_for(std::chrono::seconds(600));
  }
  sock.Disconnect();
  return 0;
}
