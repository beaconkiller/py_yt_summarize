import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import asyncio
from services.SrvDir import SrvDir
from services.SrvHelper import SrvHelper

class SrvRecord:

    duration = 5                # In seconds
    obj_record_config = {
        'sample_rate' : 44100,  # frequency
        'duration' : 5,         # in seconds
        'gain' : 6.0,           # Use this to increase gain in Db
    }

    is_recording = False

    def record(self):

        print(SrvHelper.getDateString())

        sample_rate = self.obj_record_config['sample_rate']     # frequency
        duration = self.obj_record_config['duration']           # in seconds
        filename = f"record_{SrvHelper.getDateString()}.wav"

        audio_data = sd.rec(
            int(duration * sample_rate), 
            samplerate=sample_rate, 
            channels=1, 
            dtype='float32'
        )

        audio_data = self.multiply_gain(audio_data)
        audio_data = np.clip(audio_data, -1.0, 1.0)

        sd.wait()  

        save_target = os.path.join(SrvDir.dir_recording_out, filename)

        write(save_target, sample_rate, audio_data)



    async def record_sequential(self):

        self.is_recording = True

        stream = sd.InputStream(
            samplerate=self.obj_record_config['sample_rate'],
            dtype='float32',
            channels=1,
            blocksize=1024
        )


        arr_data = []               # Array to put the recorded data before it get flushed before saving it to a .wav.
        i = 0                       # Counter.
        record_ceil = 500           # Treshold before it gets cut and then saved to a .wav.
        with stream:
            while self.is_recording:
                data,overflowed = stream.read(stream.blocksize)
                data = data * 6     # Gain. Change it to increase the volume.

                actual_volume = np.mean(np.abs(data.astype(np.float64)))
                # print(actual_volume * 250)
                self.draw_data(actual_volume * 250)
                
                await SrvHelper.delay(0.001)

                arr_data.append(data.copy())
                # if (i > 0) & (i % record_ceil == 0):
                #     chunk = np.concatenate(arr_data)                # To collect the array and put it into a small chunk.
                #     asyncio.create_task(self.save_chunk(chunk))
                #     arr_data = []
                i+=1



    async def record_continuously(self):

        self.is_recording = True

        stream = sd.InputStream(
            samplerate=self.obj_record_config['sample_rate'],
            dtype='float32',
            channels=1,
            blocksize=1024
        )


        arr_data = []
        i = 0
        record_ceil = 500
        with stream:
            while self.is_recording:
                data,overflowed = stream.read(stream.blocksize)
                data = data * 3     # Gain. Change it to increase the volume.

                actual_volume = (np.mean(np.abs(data.astype(np.float64))))
                threshold = 20
                record = False
                
                if((actual_volume*1000) > threshold) : 
                    print(actual_volume * 1000)
                    self.draw_data(actual_volume * 1000)  
                    
                # print(actual_volume * 1000 > threshold )
                # print(actual_volume * 1000, threshold )

                await SrvHelper.delay(0.001)

                arr_data.append(data.copy())
                # if (i > 0) & (i % record_ceil == 0):
                #     chunk = np.concatenate(arr_data)                # To collect the array and put it into a small chunk.
                #     asyncio.create_task(self.save_chunk(chunk))
                #     arr_data = []
                
                i+=1
        
        
        
    async def save_chunk(self, data):
        print(f"------------ {data} ------------")
        filePath = os.path.join(SrvDir.dir_recording_out, f"recording_{SrvHelper.getDateString()}.wav")
        write(
            filePath, 
            self.obj_record_config["sample_rate"], 
            data
        )



    def test(self, data):
        print(data)



    def draw_data(self, data):
        str_data = ''
        for i in range(int(data)):
            str_data = str_data + '|'
        print(str_data)



    def multiply_gain(self, data):
        multipler = 10 ** (self.gain / 20)
        return data * multipler
        

SrvRecord = SrvRecord()