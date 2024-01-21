from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import Tk, simpledialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
from pathlib import Path
from datetime import datetime

# make directory for output files
def prepare_output_dir() -> str:
    current_datetime = datetime.now() # get current datetime
    current_datetime_formatted = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") # format it to be a readable file folder name
    output_path = "./output/" + current_datetime_formatted # append the parent folder name to path
    Path(output_path).mkdir(parents=True, exist_ok=True) # make the path folders if they dont exist
    return output_path

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(
    title="Choose file to start chopping",
    filetypes=[('audio files', '.mp3;.wav')]) # show an "Open" dialog box and return the path to the selected file

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
    min_silence_len = 150,
    silence_thresh = -90, # -96 is the lowest possible dBFS value
    keep_silence = 100
)

# Confirm with the user that the output number of chunks looks correct
# Saving the files can take a long time so saves some time if this doesn't look right
confirm_answer = askyesno(title=(str(len(chunks)) + " Chunks Found"),
                          message=(str(len(chunks)) + " chunks were found.\nDo you want to continue?"))

if (not confirm_answer):
    exit("User decided to not continue.")
    
# get the file name from the file path and truncate to 16 characters    
short_filename = (filename.split('/')[-1])[:16] 
# confirm file prefix with user
file_prefix = simpledialog.askstring(
    title = "Confirm File Prefix",
    prompt = "Please enter the desired file prefix",
    initialvalue=short_filename)

# if file prefix is not empty, add a dash after
if (file_prefix):
    file_prefix += "-"
    
output_format_int = simpledialog.askinteger(title="File Format",
                                 prompt="Please select the desired output file format.\n1 = .wav\n2 = .mp3",
                                 initialvalue=1,
                                 minvalue=1, maxvalue=2)  
output_format = "wav" if output_format_int == 1 else "mp3"
print('output format dialog value: ', output_format_int, output_format)

folder_path = prepare_output_dir()

# Process each chunk with parameters
for i, chunk in enumerate(chunks):
    # Export the audio chunk
    print("Exporting chunk{0}.".format(i) + output_format)
    chunk.export(
        folder_path + "/" + file_prefix + "chunk{0}.".format(i) + output_format,
        bitrate = "192k",
        format = output_format
    )