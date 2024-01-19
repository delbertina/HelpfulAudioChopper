from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from datetime import datetime

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

# make directory for output files
current_datetime = datetime.now() # get current datetime
current_datetime_formatted = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") # format it to be a readable file folder name
output_path = "./output/" + current_datetime_formatted # append the parent folder name to path
Path(output_path).mkdir(parents=True, exist_ok=True) # make the path folders if they dont exist

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(
    title="Choose file to start chopping",
    filetypes=[('audio files', '.mp3;.wav')]) # show an "Open" dialog box and return the path to the selected file
short_filename = (filename.split('/')[-1])[:16]
print(filename, short_filename)

# Load your audio.
song = ""
if filename.endswith(".mp3"):
    song = AudioSegment.from_mp3(filename)
elif filename.endswith(".wav"):
    song = AudioSegment.from_wav(filename)
else:
    # If it's not one of the expected file types, exit this program
    exit("Invalid file extension for file at: ", filename)

chunks = split_on_silence (
    # Use the loaded audio.
    song, 
    min_silence_len = 200,
    silence_thresh = -60,
    keep_silence = 100
)

print(str(len(chunks)) + " chunks found in audio file " + filename)
# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Export the audio chunk
    print("Exporting chunk{0}.wav.".format(i))
    chunk.export(
        output_path + "/" + short_filename + "-" + "chunk{0}.wav".format(i),
        bitrate = "192k",
        format = "wav"
    )