import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import pyttsx3
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()  # required for rendering Tkinter window

        self.title('Text to MP3')
        self.geometry('830x680')

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

        self.frames = {}
        frame = Main(container, self)
        self.frames[Main] = frame
        frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(Main)

	#Go to frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class Main(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.file_name = tk.StringVar()
        
        self.__create_widgets()
        self.change_on_hover(self.save_button, "Save MP3", False)
        self.change_on_hover(self.female_voice_checkbutton, "Female voice", True)
        self.rate_entry.bind("<<ComboboxSelected>>", self.update_rate)



    def change_on_hover(self, element, name, female):
        element.bind("<Enter>", func=lambda event, name=name: self.say(name, female))
    
    def say(self, saying, female):

        if female:
            self.engine.setProperty('voice', self.voices[1].id)

        self.engine.say(saying)
        self.engine.runAndWait()
        self.engine.stop()

        if self.controller.settings["female_voice"].get() == True:
            self.engine.setProperty('voice', self.voices[1].id)
        else:
            self.engine.setProperty('voice', self.voices[0].id)

    
    def __create_widgets(self):

        self.text_widget = tk.Text(
            self,
            wrap=tk.WORD,  # Wrap text at word boundaries
            height=18,
            width=55,     
            font=('calibre', 20, 'normal'),
        )
        
        self.text_widget.grid(row=0, column=0,columnspan=3)


        ttk.Label(
            self,
            text="File Name:",
            font=('calibre', 30, 'bold')
        ).grid(row=1, column=0)


        self.file_name_entry = ttk.Entry(
            self,
            textvariable=self.file_name,
            width=20,
            font=('calibre', 30, 'normal')
        )
        
        self.file_name_entry.grid(row=1, column=1)


        self.save_button = ttk.Button(
            self,
            text='Save',
            command=self._text_to_speech
        )
        self.save_button.grid(row=1, column=2, padx=(0, 0), ipadx=15, ipady=14)

        # Create input fields or widgets to modify settings
        ttk.Label(
            self,
            text="Text Speed",
            font=('calibre', 30, 'bold')
        ).grid(row=2, column=0)


        self.rate_entry = ttk.Combobox(self, values=['Slow', 'Normal', 'Fast'], font=('calibre', 20, 'normal'), width=28)

        self.rate_entry.set("Normal")
        self.rate_entry.state(['readonly'])

        self.female_voice_checkbutton = ttk.Checkbutton(self, text='Female Voice', variable=self.controller.settings['female_voice'])

        # Add these widgets to the layout
        self.rate_entry.grid(row=2, column=1)
        self.female_voice_checkbutton.grid(row=2, column=2)

    def update_rate(self, event):
        rate_speeds = {
            "Slow" : 100,
            "Normal" : 210,
            "Fast" : 280
        }

        selected_speed = self.rate_entry.get()
        self.controller.settings['rate'].set(rate_speeds[selected_speed])

        if self.controller.settings["female_voice"].get() == True:
            self.say(selected_speed, True)
        else:
            self.say(selected_speed, False)

    

    def _text_to_speech(self):
        value = self.text_widget.get("1.0", tk.END)
        location = filedialog.askdirectory()
        
        if not self.file_name.get():
            file = self.controller.settings["default_title"].get()
        else:
            file = self.file_name.get()

        file_path = os.path.join(location,f'{file}.mp3')
        

        # Male / Female voice
        
        if self.controller.settings["female_voice"].get() == True:
            self.engine.setProperty('voice', self.voices[1].id)
        else:
            self.engine.setProperty('voice', self.voices[0].id)

        # Get rest of settings
        self.engine.setProperty('rate', int(self.controller.settings["rate"].get()))
        self.engine.save_to_file(value, file_path)
        self.engine.runAndWait()

        # Clear fields when done
        self.text_widget.delete("1.0","end")
        self.file_name_entry.delete(0,'end')

        if self.controller.settings["female_voice"].get() == True:
            self.say(f"Success, saved to {file_path}", True)
        else:
            self.say(f"Success, saved to {file_path}", False)



if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.mainloop()
