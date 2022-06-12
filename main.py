#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.net import Node 
from mininet.cli import CLI 
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE 
from mininet.log import setLogLevel,info 
from datetime import datetime 
from mininet.node import CPULimitedHost
 
import os 
import time
 
if '__main__'==__name__:
	os.system("mn -c")
	setLogLevel('info') 
	net = Mininet(link=TCLink) 
	key = "net.mptcp.mptcp_enabled" 
	value = 0 
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE , stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=", stdout,"stderr=",stderr)
 
	#membangun topology
	Host1 = net.addHost('Host1') 
	Host2 = net.addHost('Host2') 
 
	Router1 = net.addHost('Router1') 
	Router2 = net.addHost('Router2') 
	Router3 = net.addHost('Router3') 
	Router4 = net.addHost('Router4') 
 
	#MemilihBandwith (1MBPS, 500kb)
	#nilai buffer 20,40,60,100
	bandwithA={'bw':1, "max_queue_size" :100}
	bandwithB={'bw':0.5, "max_queue_size":100}
 
	#connectdevice 
	net.addLink(Host1,Router1,intfName1 = 'Host1-eth0', intfName2='Router1-eth0',cls=TCLink, **bandwithA) 
	net.addLink(Host1,Router2,intfName1 = 'Host1-eth1', intfName2='Router2-eth0', cls=TCLink, **bandwithA) 
	###
	net.addLink(Host2,Router3,intfName1= 'Host2-eth0', intfName2='Router3-eth0',cls=TCLink, **bandwithA) 
	net.addLink(Host2,Router4,intfName1= 'Host2-eth1', intfName2='Router4-eth0',cls=TCLink, **bandwithA)
	##
	net.addLink(Router1,Router3,intfName1= 'Router1-eth1', intfName2='Router3-eth1',cls=TCLink, **bandwithB)
	net.addLink(Router1,Router4,intfName1= 'Router1-eth2', intfName2='Router4-eth1',cls=TCLink, **bandwithA) 
	##
	net.addLink(Router2,Router3,intfName1='Router2-eth1', intfName2='Router3-eth2',cls=TCLink, **bandwithA) 
	net.addLink(Router2,Router4,intfName1='Router2-eth2',intfName2='Router4-eth2',cls=TCLink, **bandwithB) 
 
	net.build()
 
	Router1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward") 
	Router2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	Router3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	Router4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
 
	#Assign IP ADDRESS HOST 
	Host1.cmd("ifconfig Host1-eth0 0") 
	Host1.cmd("ifconfig Host1-eth1 0")
	Host1.cmd("ifconfig Host1-eth0 192.100.0.1 netmask 255.255.255.252")
	Host1.cmd("ifconfig Host1-eth1 192.100.0.5 netmask 255.255.255.252")
 
	Host2.cmd("ifconfig Host2-eth0 0")
	Host2.cmd("ifconfig Host2-eth1 0") 
	Host2.cmd("ifconfig Host2-eth0 192.100.0.9 netmask 255.255.255.252") 
	Host2.cmd("ifconfig Host2-eth1 192.100.0.13 netmask 255.255.255.252") 
 
	#Assign IP ADDRESS ROUTER1 
 
	Router1.cmd("ifconfig Router1-eth0 0") 
	Router1.cmd("ifconfig Router1-eth1 0") 
	Router1.cmd("ifconfig Router1-eth2 0") 
	Router1.cmd("ifconfig Router1-eth0 192.100.0.2 netmask 255.255.255.252") 
	Router1.cmd("ifconfig Router1-eth1 192.100.0.17 netmask 255.255.255.252") 
	Router1.cmd("ifconfig Router1-eth2 192.100.0.29 netmask 255.255.255.252") 
 
	#Assign IP ADDRESS ROUTER2 
	Router2.cmd("ifconfig Router2-eth0 0") 
	Router2.cmd("ifconfig Router2-eth1 0")
	Router2.cmd("ifconfig Router2-eth2 0") 
	Router2.cmd("ifconfig Router2-eth0 192.100.0.6 netmask 255.255.255.252") 
	Router2.cmd("ifconfig Router2-eth1 192.100.0.25 netmask 255.255.255.252") 
	Router2.cmd("ifconfig Router2-eth2 192.100.0.21 netmask 255.255.255.252")
 
	#Assign IP ADDRESS Router3
	Router3.cmd("ifconfig Router3-eth0 0") 
	Router3.cmd("ifconfig Router3-eth1 0") 
	Router3.cmd("ifconfig Router3-eth2 0") 
	Router3.cmd("ifconfig Router3-eth0 192.100.0.10 netmask 255.255.255.252") 
	Router3.cmd("ifconfig Router3-eth1 192.100.0.18 netmask 255.255.255.252") 
	Router3.cmd("ifconfig Router3-eth2 192.100.0.26 netmask 255.255.255.252") 
 
	#Assign IP ADDRESS Router4 
	Router4.cmd("ifconfig Router4-eth0 0") 
	Router4.cmd("ifconfig Router4-eth1 0") 
	Router4.cmd("ifconfig Router4-eth2 0") 
	Router4.cmd("ifconfig Router4-eth0 192.100.0.14 netmask 255.255.255.252") 
	Router4.cmd("ifconfig Router4-eth1 192.100.0.30 netmask 255.255.255.252") 
	Router4.cmd("ifconfig Router4-eth2 192.100.0.22 netmask 255.255.255.252") 	
 
	#Routing Host1 
	Host1.cmd("ip rule add from 192.100.0.1 table 1") 
	Host1.cmd("ip rule add from 192.100.0.5 table 2") 
	Host1.cmd("ip route add 192.100.0.0/30 dev Host1-eth0 scope link table 1") 
	Host1.cmd("ip route add default via 192.100.0.2 dev Host1-eth0 table 1") 
	Host1.cmd("ip route add 192.100.0.4/30 dev Host1-eth1 scope link table 2") 
	Host1.cmd("ip route add default via 192.100.0.6 dev Host1-eth1 table 2") 
	Host1.cmd("ip route add default scope global nexthop via 192.100.0.2 dev Host1-eth0")
 
	#routing Host2 
	Host2.cmd("ip rule add from 192.100.0.9 table 1") 
	Host2.cmd("ip rule add from 192.100.0.13 table 2") 
	Host2.cmd("ip route add from 192.100.0.8/30 dev Host2-eth0 scope link table 1") 
	Host2.cmd("ip route add default via 192.100.0.10 dev Host2-eth0 table 1") 
	Host2.cmd("ip route add default 192.100.0.12/30 dev Host2-eth1 scope link table 2") 
	Host2.cmd("ip route add default via 192.100.0.14 dev Host2-eth1 table 2") 
	Host2.cmd("ip route add default scope global nexthop via 192.100.0.10 dev Host2-eth0") 
 
	#routing tonggo router1 
	Router1.cmd("ip rule add from 192.100.0.2 table 1") 
	Router1.cmd("ip rule add from 192.100.0.17 table 2") 
	Router1.cmd("ip rule add from 192.100.0.29 table 3") 
	Router1.cmd("ip route add 192.100.0.0/30 dev Router1-eth0 scope link table 1") 
	Router1.cmd("ip route add default via 192.100.0.1 dev Router1-eth0 table 1") 
	Router1.cmd("ip route add 192.100.0.16/30 dev Router1-eth1 table 2") 
	Router1.cmd("ip route add default via 192.100.0.18 dev Router1-eth1 table 2") 
	Router1.cmd("ip route add 192.100.0.28/30 dev Router1-eth2 scope link table 3") 
	Router1.cmd("ip route add default via 192.100.0.30 dev Router1-eth2 table 3") 
	Router1.cmd("ip route add default scope global nexthop via 192.100.0.1 dev Router1-eth0") 
 
	#routing tonggone router2 
	Router2.cmd("ip rule add from 192.100.0.6 table 1") 
	Router2.cmd("ip rule add from 192.100.0.25 table 2") 
	Router2.cmd("ip rule add from 192.100.0.21 table 3") 
	Router2.cmd("ip route add from 192.100.0.4/30 dev Router2-eth0 scope link table 1") 
	Router2.cmd("ip route add default via 192.100.0.5 Router2-eth0 table 1") 
	Router2.cmd("ip route add 192.100.0.24/30 dev Router2-eth1 scope link table 2") 
	Router2.cmd("ip route add default via 192.100.0.26 dev Router2-eth1 table 2") 
	Router2.cmd("ip route add default 192.100.0.20/30 dev Router2-eth2 table 3") 
	Router2.cmd("ip route add default via 192.100.0.22 dev Router2-eth2 table 3") 
	Router2.cmd("ip route add default scope global nexthop via 192.100.0.5 dev Router2-eth0")
 
	#routing tonggone router3 
	Router3.cmd("ip rule add from 192.100.0.10 table 1") 
	Router3.cmd("ip rule add from 192.100.0.18 table 2") 
	Router3.cmd("ip rule add from 192.100.0.26 table 3") 
	Router3.cmd("ip route add 192.100.0.8/30 dev Router3-eth0 scope link table 1") 
	Router3.cmd("ip route add default via 192.100.0.9 dev Router3-eth0 table 1") 
	Router3.cmd("ip route add 192.100.0.16/30 dev Router3-eth1 scope link table 2") 
	Router3.cmd("ip route add default via 192.100.0.17 dev Router3-eth2 table 2") 
	Router3.cmd("ip route add 192.100.0.24/30 deb Router3-eth2 scope link table 3") 
	Router3.cmd("ip route add default via 192.100.0.25 dev Router3-eth2 table 3") 
	Router3.cmd("ip route add default scope global nexthop via 192.100.0.9 dev Router3-eth0") 
 
	#routing tonggone router4
	Router4.cmd("ip rule add from 192.100.0.14 table 1") 
	Router4.cmd("ip rule add from 192.100.0.30 table 2") 
	Router4.cmd("ip rule add from 192.100.0.22 table 3") 
	Router4.cmd("ip route add 192.100.0.12/30 dev Router4-eth0 scope link table 1") 
	Router4.cmd("ip route add default via 192.100.0.13 dev Router4-eth0 table 1") 
	Router4.cmd("ip route add 192.100.0.28/30 dev Router4-eth0 scope link table 2") 
	Router4.cmd("ip route add default via 192.100.0.29 dev Router4-eth1 table 2") 
	Router4.cmd("ip route add 192.100.0.20/30 dev Router4-eth2 scope link table 3") 
	Router4.cmd("ip route add default via 192.100.0.21 dev Router4-eth2 table 3") 
	Router4.cmd("ip route add default scope global nexthop via 192.100.0.13 dev Router4-eth0")
 
	#routing ruter1 
	Router1.cmd("route add -net 192.100.0.8/30 gw 192.100.0.18") 
	Router1.cmd("route add -net 192.100.0.12/30 gw 192.100.0.30") 
	Router1.cmd("route add -net 192.100.0.20/30 gw 192.100.0.30") 
	Router1.cmd("route add -net 192.100.0.4/30 gw 192.100.0.1") 
	Router1.cmd("route add -net 192.100.0.24/30 gw 192.100.0.18") 
 
	#routing router2 
	Router2.cmd("route add -net 192.100.0.0/30 gw 192.100.0.5") 
	Router2.cmd("route add -net 192.100.0.16/30 gw 192.100.0.26") 
	Router2.cmd("route add -net 192.100.0.8/30 gw 192.100.0.26") 
	Router2.cmd("route add -net 192.100.0.12/30 gw 192.100.0.22") 
	Router2.cmd("route add -net 192.100.0.28/30 gw 192.100.0.22")
 
	#routing router3 
	Router3.cmd("route add -net 192.100.0.4/30 gw 192.100.0.25") 
	Router3.cmd("route add -net 192.100.0.0/30 gw 192.100.0.17") 
	Router3.cmd("route add -net 192.100.0.20/30 gw 192.100.0.25") 
	Router3.cmd("route add -net 192.100.0.12/30 gw 192.100.0.9") 
	Router3.cmd("route add -net 192.100.0.28/30 gw 192.100.0.17") 
 
	#routing router4 
	Router4.cmd("route add -net 192.100.0.0/30 gw 192.100.0.29") 
	Router4.cmd("route add -net 192.100.0.4/30 gw 192.100.0.21") 
	Router4.cmd("route add -net 192.100.0.8/30 gw 192.100.0.13") 
	Router4.cmd("route add -net 192.100.0.16/30 gw 192.100.0.29") 
	Router4.cmd("route add -net 192.100.0.24/30 gw 192.100.0.21")
 
	#CLO3# 
	#Host2.cmd("iperf -s &") 
 
	#wireshark 
	#Host2.cmd("tcpdump -w Tubes-1301204303.pcap &") 
 
	#Client 
	#Host1.cmd("iperf -c 192.100.0.9 -t 100 &")
	#time.sleep(10) 
	#Host1.cmd("iperf -c 192.100.0.9")
 
 
	#clo4 
	Host2.cmd("iperf -s &")
	Host1.cmd("iperf -t 60 -c 192.100.0.9")
 
	CLI(net) 
net.stop()
