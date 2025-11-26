from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class Topology(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1, cls=TCLink, bw=10, delay='10ms')
        self.addLink(h2, s1, cls=TCLink, bw=10, delay='10ms')

def run_topology():
    topo = Topology()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)

    net.interact()

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_topology()

#sudo mn -c
#sudo python3 t1.py
#h1 ifconfig -a
#s1 ifconfig -a
#h1 ping -c 3 h2
#h1 arp
#h2 iperf -s &
#h1 iperf -c 10.0.0.2 -t 5
