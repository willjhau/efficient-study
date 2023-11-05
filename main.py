# ==== Importing all the necessary libraries
from tkinter import *
from tkinter import filedialog
import os
import time
from PIL import ImageTk
import moviepy.editor as mp
import gptsummary as gpt
import transcriber as t

# ==== creating main class
class VideoAudioConverter:
    # ==== creating gui window
    def __init__(self, root):
        # Define class attributes
        self.root = root
        self.root.title("Video Summariser")
        self.root.geometry('680x500')
        self.filepath = None # this is the path of the .mp3
        self.file_name = None # this is the video path

        Label(self.root).place(x=0, y=0)
        # Button that lets you select an mp4 file with a graphical navigator
        Button(self.root,text="Browse Files",font=("times new roman", 15),command=self.browse).place(x=40, y=40)

        # Creates a blank text box
        self.text = Text(self.root, wrap="word")
        self.text.place(x=50,y=100)

        # Button that lets you select a file to save the output as    
        button = Button(text="save", command=self.save_file)
        button.pack(side="bottom")


    # Routine to open navigator to save a file
    def save_file(self):
        file = filedialog.asksaveasfile(defaultextension=".txt",
                                        filetypes = [
                                            ("Text file", ".txt"),
                                            ("HTML file", ".html"),
                                            ("All files", ".*"),
                                        ])
        file_text = str(self.text.get(1.0, END))
        # Check that neither the filepath nor the text is empty
        if file != '' and file_text != '':
            file.write(file_text)
            file.close()

    # Open a navigator allowing the user to select an mp4 file to read
    def browse(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4"),))

        # Ensure the a file is selected
        if self.file_name != '':
            
            # Save the audio to a file
            self.filepath = self.convert(os.path.basename(self.file_name))
            timestart = time.time()

            # Instantiate the transcriber class
            model = t.Transcriber()

            # Perform the transcription
            model.transcribe(self.filepath)
            # Clear the output box
            self.text.delete("1.0", END)
            # Prepare the summariser class
            text = ""
            buffer = model.output
            summariser = gpt.Summariser(buffer)
            # Split up long texts into manageable chunks
            while len(buffer) > 15000:

                # Set and summarise the next 15000 characters of the transcription
                summariser.setText(buffer[:15000])
                summariser.summarise()
                # Add this to the running text string
                text += summariser.getSummary()
                buffer = buffer[15000:]
            # Summarise the rest
            summariser = gpt.Summariser(buffer)

            summariser.summarise()
            text += summariser.getSummary()
            # Add the final text to the text box
            self.text.insert("1.0", text)

            timeend = time.time()
            print("Time taken to process: ", timeend - timestart)
            return

    # Convert video to audio
    def convert(self, path):
        clip = mp.VideoFileClip(r'{}'.format(path))
        mp3Path = r'{}mp3'.format(path[:-3])
        clip.audio.write_audiofile(mp3Path)
        return mp3Path


# Main function
def main():
    # Create tkinter window
    root = Tk()
    # Creating object for class VideoAudioConverter
    obj = VideoAudioConverter(root)
    # Start the gui
    root.mainloop()

if __name__ == "__main__":
    # Calling main function
    main()
