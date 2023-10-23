import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import pyttsx3
import os

"""

3) Settings (Speed,default mp3 title, m/f voice)


"""
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # required for rendering Tkinter window

        self.title('Text to MP3')
        self.geometry('700x650')

        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 210)

        self.file_name = tk.StringVar()
        
        self.__create_widgets()
        self.change_on_hover(self.save_button, "Save MP3")


    def change_on_hover(self, element, name):
 
        # adjusting background of the widget
        # background on entering widget
        element.bind("<Enter>", func=lambda event, name=name: self.say(name))
    
        # background color on leving widget
        #element.bind("<Leave>", func=)
    
    def say(self, saying):
        self.engine.say(saying)
        self.engine.runAndWait()
        self.engine.stop()

    
    def __create_widgets(self):
    

        self.text_widget = tk.Text(
            self,
            wrap=tk.WORD,  # Wrap text at word boundaries
            height=37,
            width=100,     
            font=('calibre', 10, 'normal'),
        )
        
        self.text_widget.grid(row=0, column=0,columnspan=2)


        self.file_name_entry = ttk.Entry(
            self,
            textvariable=self.file_name,
            width=80,
            font=('calibre', 10, 'normal')
        )
        
        self.file_name_entry.grid(row=1, column=0)


        self.save_button = ttk.Button(
            self,
            text='Save',
            command=self._text_to_speech,
        )
        self.save_button.grid(row=1, column=1, padx=(0, 0), ipadx=15, ipady=14)
    

    def _text_to_speech(self):
        value = self.text_widget.get("1.0", tk.END)
        location = filedialog.askdirectory()
        
        if not self.file_name.get():
            file = "myFile"
        else:
            file = self.file_name.get()

        file_path = os.path.join(location,f'{file}.mp3')
        

        # rate = engine.getProperty('rate') -> class variable in settings
        
        self.engine.save_to_file(value, file_path)
        self.engine.runAndWait()
        self.text_widget.delete("1.0","end")
        self.file_name_entry.delete(0,'end')

        

        self.say(f"Success, saved to {file_path}")
        
        
        


if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.mainloop()
