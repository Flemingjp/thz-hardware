from pycromanager import Acquisition

class THzAcquisition(Acquisition):
    '''
    '''

    def __init__(self, image_processor=None, **kwargs):
        '''
        '''
        self.image_processor = image_processor
        self.data = {}

        self._raw = False
        self._current_index = None
        self._current_thz_on = None
        self._current_thz_off = None

        super().__init__(pre_hardware_hook_fn=self._pre_camera_hook, image_process_fn=self._process_thz_image, **kwargs)


    def _event_generation_hook(self, events):
        return events

    def _pre_camera_hook(self, event):
        return event

    def _process_thz_image(self, image, metadata):
        '''
        '''
        i = metadata['Axes']['i']
        thz = metadata['Axes']['thz_on'] == 1

        # Cache the current image
        if thz:
            self._current_thz_on = image
        else:
            self._current_thz_off = image

        # Check if start of new image pair
        if not self._current_index == i:
            self._current_index = i
        else:
            # Call child processing function
            if self.image_processor:
                data = self.image_processor(self._current_thz_on, self._current_thz_off, self.data)
            else:
                data = self.data

            # Update data reference
            self.data = data

            # Process image pair
            thz_difference = self._current_thz_on - self._current_thz_off

            # Reset cache for next pair
            self._current_index = None
            self._current_thz_on = None
            self._current_thz_off = None

            return thz_difference, metadata
    

    def acquire(self, n: int):
        '''
        '''        
        events = []
 
        for i in range(n):
            events.append({'axes': {'i': i, 'thz_on': 0}})
            events.append({'axes': {'i': i, 'thz_on': 1}})

        super().acquire(events)


    def get_data(self) -> dict:
        '''
        '''
        return self.data




#%% Demo Code
def demo_processor(thz_on, thz_off, data):
    return data

with THzAcquisition(name='test', directory='./', image_processor=demo_processor) as acq:
    acq.acquire(3)

data = acq.get_data()
