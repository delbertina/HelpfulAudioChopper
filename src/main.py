from typing import List
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import Button, IntVar, Label, Radiobutton, Tk, simpledialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
from pathlib import Path
from datetime import datetime
from os import rename, listdir
from os.path import isfile, join

# Ask dialog with list of radio buttons
# Returns ths index of the selected option
# Default selected value is the first index
# Returns the selected value if the dialog is closed
def ask_radio_dialog(title: str, prompt: str, options: List[str]):
    root = Tk()
    root.title(title)
    
    Label(root, text=prompt).pack(padx=10, pady=10)
    
    v = IntVar(value=0)
    for i, option in enumerate(options):
        Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w", padx=10)
    Button(root, text="OK", command=lambda:(root.destroy()), padx=20).pack(padx=10, pady=10)
    root.protocol(name="WM_DELETE_WINDOW", func=lambda:(root.destroy()))
    root.update()
    
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    print(w, h, ws, hs, x, y)
    
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    root.mainloop()
    root.quit() # Not totally sure why this is needed here and the destroy above, but it finally works
    return v.get()

# make directory for output files
def prepare_output_dir() -> str:
    current_datetime = datetime.now() # get current datetime
    current_datetime_formatted = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f") # format it to be a readable file folder name
    output_path = "./output/" + current_datetime_formatted # append the parent folder name to path
    Path(output_path).mkdir(parents=True, exist_ok=True) # make the path folders if they dont exist
    return output_path

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
confirm_answer_chunk = askyesno(title=(str(len(chunks)) + " Chunks Found"),
                          message=(str(len(chunks)) + " chunks were found.\nDo you want to continue?"))

if (not confirm_answer_chunk):
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

output_format_int = ask_radio_dialog(
    title="File Format",
    prompt="Please select the desired output file format.",
    options=[
        ".wav",
        ".mp3"
    ]
)

# Yes, this looks redundant and long
# I plan on expanding this to more audio formats
output_format = None

match output_format_int:
    case 0:
        output_format = "wav"
    case 1:
        output_format = "mp3"

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
    
# ask if continue to rename menu
confirm_answer_rename = askyesno(title="Start Renaming?",
                          message=("Files finished processing.\nDo you want to continue to renaming menu?"))

if (not confirm_answer_rename):
    exit("User decided to not continue to renaming.")
    
print("did user continue to rename?", confirm_answer_rename)

# get list of files to rename, just in case something went wrong somewhere
finished_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
print(folder_path, finished_files)

# menu

# rename action
# rename('file1.txt', 'file2.kml')