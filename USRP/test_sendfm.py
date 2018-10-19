#coding:utf-8
'''
Created on Oct 17, 2018

@author: sherl
'''


from gnuradio import gr, eng_notation
from gnuradio import uhd,audio
from gnuradio import analog
from gnuradio import blocks
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import math
import sys

from gnuradio.wxgui import stdgui2, fftsink2
import wx




class my_top_block(stdgui2.std_top_block):

    def __init__(self, frame, panel, vbox, argv):
        stdgui2.std_top_block.__init__ (self, frame, panel, vbox, argv)

        #---------------------------------------------src block---------------------------------------------------------------
        #self.usrp_out=uhd.usrp_sink()
        self.src=blocks.wavfile_source('/home/sherl/git/Response_center/USRP/py_OfficialDoc/uhd/test_usrp.wav' , True)
        
        '''
        gnuradio.audio.sink(int sampling_rate, std::string const device_name, bool ok_to_block=True) → sink_sptr
        Creates a sink from an audio device.
        '''
        #self.audio_sink = audio.sink(int (44.1e3), "default")
        #self.connect(src, audio_sink)
        
        
        #-----------------------------usrp_sink block-------------------------------------------------------!
        #"--args", type="string", default=""
        self.u = uhd.usrp_sink(device_addr="", stream_args=uhd.stream_args('fc32'))
        self.u.set_samp_rate(250e3)
        self.usrp_rate = self.u.get_samp_rate()
        
        self.sw_interp = 10
        self.audio_rate = self.usrp_rate / self.sw_interp    # 32 kS/s
        
        g = self.u.get_gain_range()
        self.gain = float(g.start()+g.stop())/2
        print 'gain:',str(g.start()),' --> ',str(g.stop),' at:',self.gain
        self.u.set_gain(self.gain, 0)
        
        self.ifrate=108e6  #这里设定发送频率
        r = self.u.set_center_freq(self.ifrate, 0)
        if r:
            print "Frequency =", eng_notation.num_to_str(self.u.get_center_freq())
        
        else:
            print 'set frequency fail!!!'
            
        #self.sum = blocks.add_cc () #这里只有一个端口就行，不同于fm_tx4.py
        
        print ('audio_rate, quad_rate:',self.audio_rate,self.usrp_rate)
        fmtx = analog.nbfm_tx(int(self.audio_rate), int(self.usrp_rate), max_dev=5e3, tau=75e-6, fh=0.925*self.usrp_rate/2.0)

        # Local oscillator本地振荡器
        #src0 = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, 350, ampl)
        lo = analog.sig_source_c(self.usrp_rate,            # sample rate  options.samp_rate    350e3
                                 analog.GR_SIN_WAVE, # waveform type正弦信号
                                 25e3,            # frequency   step = 25e3   offset = (0 * step, 1 * step,
                                 1.0,                # amplitude 幅值
                                 0)                  # DC Offset
        self.mixer = blocks.multiply_cc()

        self.connect(self.src, fmtx, (self.mixer, 0))
        self.connect(lo, (self.mixer, 1))
        
        
        
        ''''''
        post_mod = fftsink2.fft_sink_c(panel, title="Post Modulation",
                                           fft_size=512,
                                           sample_rate=self.usrp_rate,
                                           y_per_div=20,
                                           ref_level=40)
        self.connect (self.mixer, post_mod)
        vbox.Add (post_mod.win, 1, wx.EXPAND)
        
        
        self.connect(self.mixer, self.u)
        
        #下面用于播放wav到声卡，调试用
        '''
        self.audio_sink = audio.sink(int(self.audio_rate))
        self.connect(self.src, self.audio_sink)
        '''
        
        #-------------------------------------------------------------------------------------------------------
        

if __name__ == '__main__':
    try:
        my_top_block().run()
    except KeyboardInterrupt:
        pass
