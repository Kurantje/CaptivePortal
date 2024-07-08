#!/bin/bash

HOST="192.168.4.1"
PORT=80

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
ctrl_c () {	echo -n; }	# do nothing

echo "### Configure NetworkManager redirection"
sudo bash -c 'echo "address=/#/'$HOST'" > /etc/NetworkManager/dnsmasq-shared.d/redirect.conf'

echo "### Delete access point from NetworkManager"
nmcli con delete "AccessPoint" > /dev/null 2>&1

echo "### Configure access point in NetworkManager"
nmcli con add type wifi mode ap con-name "AccessPoint" ssid "AccessPoint"  ipv4.method shared ipv4.address $HOST/24 autoconnect no

echo "### Clear iptables, just to be sure"
sudo iptables -F
sudo iptables -t nat -F

if [ $PORT -ne 80 ]
then
	echo "### Redirect all inbound http traffic to our server on port PORT"
	sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j DNAT --to-destination $HOST:$PORT
fi

echo "### Activate wireless access point"
nmcli con up "AccessPoint"

echo "### Start web server"
if [ $PORT -ne 80 ]
then
	python portal.py $HOST $PORT
else
	sudo python portal.py $HOST $PORT
fi

echo "### Disconnect wireless access point"
nmcli con down "AccessPoint"

echo "### Clear iptables"
sudo iptables -t nat -F

echo "### Remove NetworkManager redirection"
sudo rm -f /etc/NetworkManager/dnsmasq-shared.d/redirect.conf

echo "### Delete access point from NetworkManager"
nmcli con delete "AccessPoint"

