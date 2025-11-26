from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

class Topology(Topo):
    def build(self):

        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        server = self.addHost('server', ip='10.0.0.100/24')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(h1, s1)
        self.addLink(h2, s1)

        self.addLink(h3, s3)
        self.addLink(server, s3)

        self.addLink(s1, s2)
        self.addLink(s2, s3)


def run_topology():
    topo = Topology()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run_topology()

#sudo mn -c
#sudo python3 t2.py
#h1 ifconfig -a
#server ifconfig -a
#server ip addr show
#h2 ip addr show
#h3 ping 0c 2 server
#h1 arp
#server iperf -s &
#h1 iperf -c 10.0.0.100 -t 5
