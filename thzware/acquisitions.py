from pycromanager import Acquisition, Core, multi_d_acquisition_events

def acquisiton_events(n: int = 1, **kwargs) -> dict:
    return multi_d_acquisition_events(num_time_points=n, channels = ["Off", "On"], channel_group = "THz UCA", **kwargs)

def validate_configuration() -> bool:
    '''
    Validates the loaded MicroManager profile to check any THz acquisition will run correctly. All failed tests should be reported.
    '''
    core = Core()

    if not core.is_config_defined("THz UCA", "On"):
        raise Exception("MicroManager profile has no group named 'THz UCA' with preset 'On'")
    
    if not core.is_config_defined("THz UCA", "Off"):
        raise Exception("MicroManager profile has no group named 'THz UCA' with preset 'Off'")
    
    return True


class THzAcquisition(Acquisition):
    '''
    THzAcquisition
    '''

    def __init__(self, data_processor: callable = None, **kwargs):
        '''
        '''
        super().__init__(image_process_fn=self._process_images, **kwargs)

        validate_configuration()
        
        self._data = {}
        self._data_processor = data_processor
        self._last_thz_off_image = None


    def _process_images(self, image, metadata):
        '''
        '''
        channel = metadata['Axes']['channel'].lower()

        if channel == 'off':
            self._last_thz_off_image = image
        else:
            if self._data_processor:
                self._data = self._data_processor(self.data, thz_on=image, thz_off=self._last_thz_off_image)

        return image, metadata
    

    def get_data(self) -> dict:
        return self._data
    

if __name__ == "__main__":

    def demo_processor(data: dict, thz_on, thz_off):
        return data
        
    with THzAcquisition(name="test", directory='./', data_processor=demo_processor) as acq:
        acq.acquire(acquisiton_events())
