from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel

def run():
    setLogLevel('info')
    topo = SingleSwitchTopo(4)  # 4 hosts, 1 switch
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    print("\n=== Testing ARP Handling ===")
    net.pingAll()

    net.stop()

if __name__ == '__main__':
    run()
