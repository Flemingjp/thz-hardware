import nidaqmx

class UCA():
    '''
    User Attenuation Control (UAC) of a THz source via a NI USB DAC. Provides 
    basic control between an on and off state, or for setting the UCA to an
    arbitary voltage.
    '''
    
    def __init__(self, v_on: float = 0.0, v_off: float = 5.0, channel: str = "Dev2/ao1"):
        self.v_on = v_on
        self.v_off = v_off
        self.channel = channel
        
    def set_uca(self, v: float):
        with nidaqmx.Task() as t:
            t.ao_channels.add_ao_voltage_chan(self.channel, min_val=0.0, max_val=5.0)
            t.write(v)
            
    def on(self):
        self.set_uca(self.v_on)
        
    def off(self):
        self.set_uca(self.v_off)


if __name__ == "__main__":
    # Example Usage    
    uca = UCA(v_on=1.6)
    uca.on()
    uca.off()
    
        
