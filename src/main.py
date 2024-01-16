# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(
    title="Choose file to start chopping",
    filetypes=[('audio files', '.mp3;.wav')]) # show an "Open" dialog box and return the path to the selected file
print(filename)

# Load your audio.
song = ""
if filename.endswith(".mp3"):
    song = AudioSegment.from_mp3(filename)
elif filename.endswith(".wav"):
    song = AudioSegment.from_wav(filename)
else:
    # If it's not one of the expected file types, exit this program
    exit("Invalid file extension for file at: ", filename)

exit("Have not tested the stuff after this, woah there")

chunks = split_on_silence (
    # Use the loaded audio.
    song, 
    # Specify that a silent chunk must be at least Xms long.
    min_silence_len = 500,
    # Consider a chunk silent if it's quieter than -16 dBFS.
    # (You may want to adjust this parameter.)
    silence_thresh = -16
)

# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    silence_chunk = AudioSegment.silent(duration=500)

    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    print("Exporting chunk{0}.wav.".format(i))
    normalized_chunk.export(
        ".//chunk{0}.wav".format(i),
        bitrate = "192k",
        format = "wav"
    )