# Network Monitor - Monitor your network connection

## Introduction

This project was primary made as semestrial project. This project contain both monitor/server-side and client-side.

## Installation

Fetch the repository, install all components from requirements.txt via pip 
```
pip install requirements.txt 
```
If you want to use a monitor/server-side, you need install a **rrdtool** and python extension You also need a remote WWW server with ping enabled and reachable http server. Create a 10,50,100Mbit files name it 10M.bin, 50M.bin and 100M.bin
```
sudo dd if=/dev/urandom of=10M.bin count=10 bs=1M
sudo dd if=/dev/urandom of=50M.bin count=50 bs=1M
sudo dd if=/dev/urandom of=100M.bin count=100 bs=1M
```
Upload it to the root directory of http server. Example: http://127.0.0.1/10M.bin

## Usage

### Client-side

Prefill config file settings.json with your data, default data expect local HTTP server with files on 127.0.0.1 and also client IP is set to 127.0.0.1. Leave default update interval

To run client type 
```
python3 main.py
```

### Server side

Server expect IPs of clients on file sonda-list.txt, every line must contain one IP

To run server type 
```
python3 monitor.py
```
