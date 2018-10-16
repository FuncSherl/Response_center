#coding:utf-8
'''
Created on Oct 17, 2018

@author: sherl
'''


from gnuradio import gr,audio, uhd
from gnuradio import audio
from gnuradio.eng_option import eng_option
from optparse import OptionParser


from gnuradio import analog




class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        self.usrp_out=uhd.usrp_sink()

if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
