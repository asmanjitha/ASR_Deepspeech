import sounddevice as sd
from scipy.io.wavfile import write
from deepspeech import Model
import scipy.io.wavfile as wav
import pyaudio
import wave




def get_input():
    print("Press R for record audio, Press Q to quit...")
    return input()

def recordPyaudio():

    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 1
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)


    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return frames

def record(count):
    fs = 16000  # Sample rate
    seconds = 4  # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    print ("Recording....")
    sd.wait()  # Wait until recording is finished
    write('./Recordings/recording '+str(count) + '.wav', fs, myrecording)  # Save as WAV file
    print ("Recording saved... \n")

    return myrecording

def getCount():
    f = open("./Recordings/data.txt")
    lines = f.read().splitlines()
    lastLine = lines[-1]
    # lastLine = f.readline(-1)
    count = int(lastLine[0:3])
    print (count)
    return count

def getCommand():
    print ("Press 1:Count, 2:Colour, 3:Focus, 4:No Op")
    command = input()
    if command == "1":
        return "Count"
    elif command == "2" :
        return "Colour"
    elif command == "3":
        return "Focus"
    elif command == "4":
        return "No OP"
    else:
        return ""

def run():
    while True:
        choice = get_input()
        if choice == "r":
            count = getCount() + 1
            myrecording = record(count)

            ds = Model("models/output_graph.pb", 26, 9, "models/alphabet.txt", 500)
            # fs, audio = wav.read("./output2.wav")

            fs = 16000
            
            sound = []
            for i in myrecording:
                sound.append(i[0])
            
            processed_data = ds.stt(sound, fs)
            # processed_data = ds.sttWithMetadata(sound, fs)
            print (processed_data)
            command = getCommand()

            processed_data = str(count) + '  | ' + command + '  | ' + processed_data

            with open('./Recordings/data.txt', 'a') as f:
                f.write('\n' + processed_data)
        elif choice == "q":
            print ("Application Quit")
            return

if __name__ == "__main__":
    run()
