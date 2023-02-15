import nidaqmx

class DAC():
    '''
    Analog voltage ouput using NI-USB DAC. Provides basic voltage control either between
    a pre-defined on/off state. Or control to set an arbitary voltage.
    '''
    
    def __init__(self, v_on: float = 0.0, v_off: float = 5.0, channel: str = "Dev2/ao1"):
        self.v_on = v_on
        self.v_off = v_off
        self.channel = channel
        
    def set_voltage(self, v: float):
        with nidaqmx.Task() as t:
            t.ao_channels.add_ao_voltage_chan(self.channel, min_val=0.0, max_val=5.0)
            t.write(v)
            
    def on(self):
        self.set_voltage(self.v_on)
        
    def off(self):
        self.set_voltage(self.v_off)