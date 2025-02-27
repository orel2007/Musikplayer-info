from tkinter import *
from tkinter import filedialog
import pygame
import os

class GUI:
    def __init__(self):
        self.musicplayer = Tk()
        self.musicplayer.title("Music Player")
        self.musicplayer.geometry("500x300")
        
        pygame.mixer.init()

        self.menue = Menu(self.musicplayer)
        self.musicplayer.config(menu=self.menue)

        self.songs = []
        self.aktueller_song = ""
        self.paused = False

        def musik_laden():
            self.aktueller_song = ""
            self.musicplayer.directory = filedialog.askdirectory()
            for song in os.listdir(self.musicplayer.directory):
                name, ext = os.path.splitext(song)
                if ext == ".mp3":
                    self.songs.append(song)

            for song in self.songs:
                self.songliste.insert("end", song)
            
            self.songliste.selection_set(0)
            self.aktueller_song = self.songs[self.songliste.curselection()[0]]

        self.organisieren = Menu(self.menue, tearoff=False)
        self.organisieren.add_command(label="Ordner auswählen", command=musik_laden)
        self.menue.add_cascade(label="Organisieren", menu=self.organisieren)
    
        self.songliste = Listbox(self.musicplayer, bg="black", fg="white", width=100, height=15)
        self.songliste.pack()
        
        self.play_button_bild = PhotoImage(file="play.png") 
        self.pause_button_bild = PhotoImage(file="pause.png")
        self.back_button_bild = PhotoImage(file="back.png")
        self.next_button_bild = PhotoImage(file="skip.png")
        
        #self.playlist = Listbox(self.musicplayer, bg="black", fg="white", width=100, height=15)
        
        self.frame = Frame(self.musicplayer)
        self.frame.pack()
        
        self.playbutton = Button(self.frame, image=self.play_button_bild, borderwidth=0, command=self.play_music)
        self.playbutton.grid(row=0, column=1, padx=7, pady=10)
        
        self.pausebutton = Button(self.frame, image=self.pause_button_bild, borderwidth=0, command=self.pause_music)
        self.pausebutton.grid(row=0, column=2, padx=7, pady=10)
        
        self.backbutton = Button(self.frame, image=self.back_button_bild, borderwidth=0, command=self.back_music)
        self.backbutton.grid(row=0, column=3, padx=7, pady=10)
        
        self.skipbutton = Button(self.frame, image=self.next_button_bild, borderwidth=0, command=self.skip_music)
        self.skipbutton.grid(row=0, column=4, padx=7, pady=10)

        self.musicplayer.mainloop()

    def play_music(self):
        if not self.paused:
            pygame.mixer.music.load(os.path.join(self.musicplayer.directory, self.aktueller_song))
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def skip_music(self):
        try:
            self.songliste.selection_clear(0, END)
            self.songliste.selection_set(self.songs.index(self.aktueller_song) + 1)
            self.aktueller_song = self.songs[self.songliste.curselection()[0]]
            self.play_music()
        except:
            pass

    def back_music(self):
        try:
            self.songliste.selection_clear(0, END)
            self.songliste.selection_set(self.songs.index(self.aktueller_song) - 1)
            self.aktueller_song = self.songs[self.songliste.curselection()[0]]
            self.play_music()
        except:
            pass

if __name__ == "__main__":
    GUI()