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

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

		#column & row 0
        container.grid_rowconfigure(0, weight = 1,uniform='x')
        container.grid_columnconfigure(0, weight = 1, uniform='x')


        # Create variables for settings
        self.settings = {
            'rate': tk.DoubleVar(value=210),
            'default_title': tk.StringVar(value='myFile'),
            'female_voice': tk.BooleanVar(value=False),
        }


        # initializing frames to an empty array
        self.frames = {}
	
		# iterating through a tuple consisting
		# of the different page layouts
        for F in (Main, Settings):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(Main)

	#Go to any frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class Main(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.engine = pyttsx3.init()
        self.file_name = tk.StringVar()
        
        self.__create_widgets()
        self.change_on_hover(self.save_button, "Save MP3")
        



    def change_on_hover(self, element, name):
        element.bind("<Enter>", func=lambda event, name=name: self.say(name))
    
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

        self.settings_button = ttk.Button(
            self,
            text='Settings',
            command=lambda: self.controller.show_frame(Settings)
        )
        self.settings_button.grid(row=2, column=0, padx=(0, 0))
    

    def _text_to_speech(self):
        value = self.text_widget.get("1.0", tk.END)
        location = filedialog.askdirectory()
        
        if not self.file_name.get():
            file = self.controller.settings["default_title"].get()
        else:
            file = self.file_name.get()

        file_path = os.path.join(location,f'{file}.mp3')
        

        # Male / Female voice
        voices = self.engine.getProperty('voices')
        if self.controller.settings["female_voice"].get() == True:
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)

        # Get rest of settings
        self.engine.setProperty('rate', int(self.controller.settings["rate"].get()))
        self.engine.save_to_file(value, file_path)
        self.engine.runAndWait()

        # Clear fields when done
        self.text_widget.delete("1.0","end")
        self.file_name_entry.delete(0,'end')

        self.say(f"Success, saved to {file_path}")


class Settings(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.__create_widgets()

    def __create_widgets(self):

        # Create input fields or widgets to modify settings
        rate_entry = ttk.Entry(self, textvariable=self.controller.settings['rate'])
        #title_entry = ttk.Entry(self, textvariable=self.controller.settings['default_title'])
        female_voice_checkbutton = ttk.Checkbutton(self, text='Female Voice', variable=self.controller.settings['female_voice'])

        # Add these widgets to the layout
        rate_entry.grid(row=0, column=1)
        #title_entry.grid(row=1, column=1)
        female_voice_checkbutton.grid(row=2, column=1)

        self.home_button = ttk.Button(
            self,
            text='Home',
            command=lambda: self.controller.show_frame(Main)
        )
        self.home_button.grid(row=2, column=0, padx=(0, 0))

        


if __name__ == "__main__":
    app = App()
    #app.resizable(False,False)
    app.mainloop()
