'''
Created on Oct 15, 2018

@author: sherl
'''
import math,time
from gnuradio import gr, analog
from gnuradio import audio 
from gnuradio.eng_option import eng_option
from optparse import OptionParser
class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        parser = OptionParser(option_class=eng_option)
        parser.add_option("-O", "--audio-output", type="string",  default="",         help="pcm output device name. E.g., hw:0,0        or /dev/dsp")
        parser.add_option("-r", "--sample-rate", type="eng_float",   default=48000,   help="set sample rate to RATE (48000)")
        (options, args) = parser.parse_args ()
        print (options, args)
        if len(args) != 0:
            parser.print_help()
            raise SystemExit, 1
        sample_rate = int(options.sample_rate)
        ampl = 0.1
        
        self.start_fre=440
        
        self.src0 = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, self.start_fre,     ampl)
        self.src1 = analog.sig_source_f (sample_rate, analog.GR_SIN_WAVE, self.start_fre,     ampl)
        dst = audio.sink (sample_rate, options.audio_output)
        self.connect (self.src0, (dst, 0))
        self.connect (self.src1, (dst, 1))
    

        
if __name__ == '__main__':
    try:
        tep=my_top_block()
        tep.run()

    except KeyboardInterrupt:
        pass 
