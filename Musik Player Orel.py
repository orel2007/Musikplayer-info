from tkinter import *
from tkinter import filedialog
import pygame
import os 




class GUI:
    def __init__(self):
        
        self.musicplayer = Tk()
        self.musicplayer.title = ("Music Player")
        self.musicplayer.geometry((f"{self.musicplayer.winfo_screenwidth()}x{self.musicplayer.winfo_screenheight()}"))
        
        pygame.mixer.init()

        self.menue = Menu(self.musicplayer)
        self.musicplayer.config(menu = self.menue)

        self.songs = []
        self.aktueller_song = ""
        self.paused = False

        def musik_laden():
            self.aktueller_song = ""
            self.musicplayer.directory = filedialog.askdirectory
            for song in os.listdir(self.musicplayer.directory):
                name, ext = os.path.splitext(song)
                if ext == ".mp3":
                    self.songs.append(song)

            for song in self.songs:
                self.songliste.insert("end", song)
            
            self.songliste.selection_set(0)
            self.aktueller_song = self.songs [self.songliste.curselection()[0]]



        self.organisieren = Menu(self.menue, tearoff = False)
        self.organisieren.add_command(label = "Ordner auswählen", command = musik_laden)
        self.menue.add_cascade(label = "Organisieren", menu = self.organisieren)
    
        
        self.songliste = Listbox(self.musicplayer, bg = "black", fg="white", width =150, height = 30)
        self.songliste.pack()
        
        self.play_button_bild = PhotoImage(file = "play.png")
        self.pause_button_bild = PhotoImage(file = "pause.png")
        self.back_button_bild = PhotoImage(file = "back.png")
        self.next_button_bild = PhotoImage(file = "skip.png")
        
        self.playlist = Listbox(self.musicplayer, bg ="black", fg="white", width = 100, height=15)
        
        self.frame = Frame(self.musicplayer)
        self.frame.pack()
        
        
        self.playbutton = Button (self.frame, image=self.play_button_bild, borderwidth =0)
        self.playbutton.grid(row=0, column=1, padx=7, pady= 10)
        
        self.pausebutton = Button (self.frame, image=self.pause_button_bild, borderwidth =0)
        self.pausebutton.grid(row=0, column=2, padx=7, pady= 10)
        
        self.backbutton = Button (self.frame, image=self.back_button_bild, borderwidth =0)
        self.backbutton.grid(row=0, column=3, padx=7, pady= 10)
        
        self.skipbutton = Button (self.frame, image=self.next_button_bild, borderwidth =0)
        self.skipbutton.grid(row=0, column=4, padx=7, pady= 10)


        
        
        
 


        self.musicplayer.mainloop()
        

if __name__ == "__main__":
    GUI()