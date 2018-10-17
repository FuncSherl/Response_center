#coding:utf-8
'''
Created on 2018年10月17日

@author:China
'''

 
from gnuradio import gr,blocks,digital,uhd
import struct,sys
 
class transmit_path(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
                ## Modulator
        self.modulator=digital.qpsk_mod(mod_code="gray",differential=True,samples_per_symbol=4,excess_bw=0.35,verbose=False,log=False)
                ## USRP Sink
        self.u=uhd.usrp_sink(device_addr="",stream_args=uhd.stream_args('fc32'))
                self.u.set_samp_rate(500e3)
                self.u.set_center_freq(5.04e9,0)
                self.u.set_gain(35,0)
                self.u.set_antenna("TX/RX",0)
                ## Packet Transmitter
                self.packet_transmitter=digital.mod_pkts(self.modulator,access_code=None,msgq_limit=4,pad_for_usrp=True)
                ## Connects
        self.connect(self.packet_transmitter,self.u)
        def send_pkt(self,payload='',eof=False):
                "Call to send a packet"
                return self.packet_transmitter.send_pkt(payload,eof)
 
def main():
    tb=transmit_path()
    tb.start()
        n=0
        pkt_size=1024
        pktno=0
        while n < 1e6:
                data = (pkt_size - 2) * chr(pktno & 0xff) 
                payload = struct.pack('!H', pktno & 0xffff) + data
                tb.send_pkt(payload)
                n += len(payload)
                sys.stderr.write('.')
                pktno += 1        
        send_pkt(eof=True)
        tb.wait()
 
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass