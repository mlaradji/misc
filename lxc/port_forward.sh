#!/bin/bash

# Port forward 1080 and 10433 to ports 80 and 443 of web-server

Server_ip="192.168.0.10"
web_server_ip="192.168.10.100"
interface="wlp3s0"

sudo iptables-save > /home/mohamed/.iptables.bak

sudo sysctl net.ipv4.ip_forward=1


sudo iptables -t nat -A PREROUTING -i "$interface" -p tcp -d "$Server_ip" --dport 1080 -j DNAT --to-destination "$web_server_ip":80
sudo iptables -t nat -A PREROUTING -i "$interface" -p tcp -d "$Server_ip" --dport 10443 -j DNAT --to-destination "$web_server_ip":443

#sudo iptables -t nat -A PREROUTING -p tcp --dport 1080 -j DNAT --to "$web_server_ip":80
#sudo iptables -t nat -A PREROUTING -p tcp --dport 10443 -j DNAT --to "$web_server_ip":443



sudo iptables -t nat -A POSTROUTING -j MASQUERADE
