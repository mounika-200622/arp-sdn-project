from pox.core import core
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class ARPHandler(object):

    def __init__(self):
        self.arp_table = {}  # IP -> (MAC, connection, port)
        core.openflow.addListeners(self)
        log.info("ARP Handler initialized")

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s connected", event.dpid)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        if packet.type == ethernet.ARP_TYPE:
            self._handle_arp(event, packet)
        else:
            self._flood(event)

    def _handle_arp(self, event, packet):
        arp_packet = packet.payload
        src_ip = arp_packet.protosrc
        src_mac = arp_packet.hwsrc
        dst_ip = arp_packet.protodst

        # Store discovered host
        self.arp_table[src_ip] = (src_mac, event.connection, event.port)
        log.info("Host discovered: IP=%s MAC=%s Port=%s", src_ip, src_mac, event.port)

        if arp_packet.opcode == arp.REQUEST:
            log.info("ARP Request: Who has %s? Tell %s", dst_ip, src_ip)

            if dst_ip in self.arp_table:
                # Generate ARP Reply from controller (proxy ARP)
                dst_mac, _, _ = self.arp_table[dst_ip]
                self._send_arp_reply(event, packet, arp_packet, dst_mac)
            else:
                # Flood the ARP request
                self._flood(event)

        elif arp_packet.opcode == arp.REPLY:
            log.info("ARP Reply: %s is at %s", src_ip, src_mac)
            # Validate and update table
            self._validate_and_forward(event, packet)

    def _send_arp_reply(self, event, eth_packet, arp_req, dst_mac):
        """Generate ARP reply from the controller (Proxy ARP)"""
        arp_reply = arp()
        arp_reply.hwtype = arp.HW_TYPE_ETHERNET
        arp_reply.prototype = arp.PROTO_TYPE_IP
        arp_reply.hwlen = 6
        arp_reply.protolen = 4
        arp_reply.opcode = arp.REPLY
        arp_reply.hwdst = arp_req.hwsrc          # Requester's MAC
        arp_reply.protodst = arp_req.protosrc    # Requester's IP
        arp_reply.protosrc = arp_req.protodst    # Target IP
        arp_reply.hwsrc = dst_mac                 # Target MAC (from table)

        eth = ethernet()
        eth.type = ethernet.ARP_TYPE
        eth.dst = eth_packet.src
        eth.src = dst_mac
        eth.payload = arp_reply

        msg = of.ofp_packet_out()
        msg.data = eth.pack()
        msg.actions.append(of.ofp_action_output(port=event.port))
        event.connection.send(msg)

        log.info("ARP Reply sent: %s is at %s", arp_req.protodst, dst_mac)

    def _validate_and_forward(self, event, packet):
        """Forward valid ARP replies"""
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_ALL))
        event.connection.send(msg)

    def _flood(self, event):
        """Flood packet out all ports"""
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("Flooding packet from port %s", event.port)


def launch():
    core.registerNew(ARPHandler)
    log.info("ARP Handler launched")
