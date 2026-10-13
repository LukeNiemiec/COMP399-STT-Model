import wave
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from numpy import log10, ndarray, array, float64, split, reshape, append
from os import system

import librosa

from noisereduce import reduce_noise




class WavFile:
    def __init__(self, fn: str):
        self.filename = fn
        self.recording_folder = "recordings/"
        self.frames = self.num_frames = self.sr = None
        
        
    # gets frames, array of integers, from the file always needed
    # TODO: check for completion before continuing functionality
    def get_frames_from_file(self):
    
        frames, self.sr = librosa.load(f"{self.recording_folder}/{self.filename}")

        # reduce noise in the loaded frames
        self.frames = reduce_noise(y=frames, sr=self.sr)

        self.num_frames = len(self.frames)
        
                    
    # slices frames into chunks 
    def slice_frames(self, frames):

        
        
        chunk_size = int(self.sr * 0.025) # 25ms chunk size
        chunk_step = int(self.sr * 0.010) # 10ms frame overlap
       
        print(chunk_size, chunk_step)
        lf = len(frames)
        chunks = []
        slices = []
        
        for i in range(0, lf, chunk_step):
            slices.append((i, i+chunk_size))

        for s in slices:
            chunks.append(frames[s[0]:s[1]].copy())

        
        return chunks

    # slices spectrogram into chunks
    def slice_spectrogram(self, spectrogram):

        chunk_size = round((self.sr * 0.025) / 256)# 25ms chunk size 
        chunk_step = round((self.sr * 0.010) / 256)# 10ms frame overlap
       
        
        lf = len(spectrogram[0])
        chunks = []
        slices = []
        
        for i in range(0, lf, chunk_step):
            slices.append((i, i+chunk_size))
            
   
        chunks = [spectrogram[:, s] for s in slices if s[1] < lf]

        return chunks

    


    # visualizes a wav file in many different representations
    def visualize_file(self):

        # check whether a fil
        
        print(f"[+] Visualizing {self.filename} now...\n")

        # choosing a visuallization option
        while True:
            choices = ("a", "s", "m", "q")
            system("clear")
            choice = input(f"\nSelected File: {self.filename}\n\nChoose a plotting method:\na: Amplitude / Time\ns: Spectograph\nm: Mel Spectrograph\n\n(a, s, m): ")
            
            if choice in choices:
                try:
                
                    if choice == "a":
                        
                            # open a window to see the graphical representation of the signal
                        self.plot_frames()

                    elif choice == "s":

                        # plot a frequency over time graph of the signal
                        self.plot_spectrogram()


                    elif choice == "m":
                        self.plot_mel_spectrogram()

                    elif choice == "q":
                        break
                    
                except KeyboardInterrupt:
                    plt.close()
                    continue
                    
                except Exception as err:
                    print(f"[-] VIS ERROR: {err}")
                    
            else:
                print("\n")
                continue



    # plots frames from the given filename
    def plot_frames(self):
        
             
        emp_frames = self.pre_emphesis(self.frames)
        
        # apply pre-emphesis on the received signal
        # frames = pre_emphisis(frames)
        

        plt.plot([int(x) for x in emp_frames])
        
        # plt.ylim(-300, 300)    # y-axis from 0 to 35
        plt.ylabel("Amplitude")
        plt.xlabel("Time")
        plt.show()


        
    def plot_spectrogram(self):
        filename = f"{self.recording_folder}/{self.filename}"
        sr, frames = wavfile.read(filename)
        
        freqs, t, sxx = signal.spectrogram(frames, sr)
        print(len(t), len(frames))

        plt.pcolormesh(t, freqs, 10* log10(sxx), cmap="plasma")
        plt.ylabel("Frequency(Hz)")
        plt.xlabel("Time(s)")
        plt.show()


    # shows the spectrogram using librosa and pyplot
    def show_spectrogram(self, spectrogram):
        plt.figure(figsize=[25,10])
        librosa.display.specshow(spectrogram, x_axis='time', y_axis='mel', sr=self.sr)
        plt.colorbar(format="%+2.f")
        plt.show()

        # wait for enter...
        input()

        # TODO: plt.close() ?
        
    # slices spectrogram after computing spectrogram from file
    def chunk_spectrogram(self):

        
        mel_spectrogram = librosa.feature.melspectrogram(y=self.frames, sr=self.sr, hop_length=256, n_fft=2048, n_mels=512)        
        
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)

        chunks = self.slice_spectrogram(log_mel_spectrogram)
        
        # print("\n\n[+] Chunks: ", len(chunks), chunks[0].shape)
        # print(len(self.frames), type(log_mel_spectrogram), log_mel_spectrogram.shape, "  [+] CALC with coeff 256:", round(len(self.frames) / 256), chunk_size)
        # 
        
        for chunk in chunks:
           self.show_spectrogram(chunk)


        return chunks


    # returns a mel spectrogram of the audio signal
    def get_mel_spectrogram(self, data):
        filename = f"{self.recording_folder}/{self.filename}"

        mel_spectrogram = librosa.feature.melspectrogram(y=data, sr=self.sr, hop_length=256, n_fft=390, n_mels=100)        

        return mel_spectrogram
            
    # computes spectrogram for each chunk from slicing frames
    def batch_spectrogram(self):

        chunks = []
        
        # compute log mel spectrogram for all of the slices
        for chunk in self.slice_frames(self.frames):
        
            mel_spectrogram = self.get_mel_spectrogram(chunk)
            
            log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
            
            # self.show_spectrogram(log_mel_spectrogram)
            chunks.append(log_mel_spectrogram)
            

        return chunks


    
if __name__ == "__main__":
    wf= WavFile("name.wav")
    wf.get_frames_from_file()

    
