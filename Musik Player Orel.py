from tkinter import *
from tkinter import filedialog, ttk
import pygame
import os
from mutagen.mp3 import MP3



class GUI:
    def __init__(self):
        self.musicplayer = Tk()
        self.musicplayer.title("Music Player")
        self.musicplayer.geometry("500x500")  
        self.musicplayer.configure(bg="dark blue") 
        
        pygame.mixer.init()

        self.menue = Menu(self.musicplayer)
        self.musicplayer.config(menu=self.menue)

        self.songs = []
        self.aktueller_song = ""
        self.paused = False
        self.playing = False
        
        self.lautstärke_label = Label(self.musicplayer, text ="Lautstärke", bg ="dark blue", fg = "white")
        self.lautstärke_label.pack(pady=5)
        self.lautstärke_bar = ttk.Scale(self.musicplayer, from=0, to=1, orient = HORIZONTAL, command = self.set_lautstärke)
        
        
        
        def musik_laden():
            self.aktueller_song = ""
            self.songs.clear()
            self.songliste.delete(0, END)
            directory = filedialog.askdirectory()
            if directory:
                for song in os.listdir(directory):
                    name, ext = os.path.splitext(song)
                    if ext == ".mp3":
                        self.songs.append(os.path.join(directory, song))
                        self.songliste.insert("end", song)
                
                if self.songs:
                    self.songliste.selection_set(0)
                    self.aktueller_song = self.songs[0]

        
        
        self.organisieren = Menu(self.menue, tearoff=False)
        self.organisieren.add_command(label="Ordner auswählen", command=musik_laden)
        self.menue.add_cascade(label="Organisieren", menu=self.organisieren)
    
        
        self.songliste = Listbox(self.musicplayer, bg="black", fg="white", width=60, height=15)
        self.songliste.pack(pady=10, padx=10)
        
       
        self.progress = ttk.Progressbar(self.musicplayer, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10)

        
        self.time_label = Label(self.musicplayer, text="00:00 / 00:00", bg="dark blue", fg="white")
        self.time_label.pack(pady=5)
        
       
        
        self.play_button_bild = PhotoImage(file="play.png")
        self.pause_button_bild = PhotoImage(file="pause.png")
        self.back_button_bild = PhotoImage(file="back.png")
        self.next_button_bild = PhotoImage(file="skip.png")

        
        button_groeße = (40, 40) 
        self.play_button_bild = self.play_button_bild.subsample(int(self.play_button_bild.width() / button_groeße[0]), int(self.play_button_bild.height() / button_groeße[1]))
        self.pause_button_bild = self.pause_button_bild.subsample(int(self.pause_button_bild.width() / button_groeße[0]), int(self.pause_button_bild.height() / button_groeße[1]))
        self.back_button_bild = self.back_button_bild.subsample(int(self.back_button_bild.width() / button_groeße[0]), int(self.back_button_bild.height() / button_groeße[1]))
        self.next_button_bild = self.next_button_bild.subsample(int(self.next_button_bild.width() / button_groeße[0]), int(self.next_button_bild.height() / button_groeße[1]))
        
        
        self.frame = Frame(self.musicplayer, bg="white")
        self.frame.pack(pady=10)
        
        
        self.playbutton = Button(self.frame, image=self.play_button_bild, borderwidth=0, command=self.play_music, bg="dark blue")
        self.playbutton.grid(row=0, column=1, padx=7)
        
        self.pausebutton = Button(self.frame, image=self.pause_button_bild, borderwidth=0, command=self.pause_music, bg="dark blue")
        self.pausebutton.grid(row=0, column=2, padx=7)
        
        self.backbutton = Button(self.frame, image=self.back_button_bild, borderwidth=0, command=self.back_music, bg="dark blue")
        self.backbutton.grid(row=0, column=0, padx=7)
        
        self.skipbutton = Button(self.frame, image=self.next_button_bild, borderwidth=0, command=self.skip_music, bg="dark blue")
        self.skipbutton.grid(row=0, column=3, padx=7)

        self.musicplayer.mainloop()

    
    
    def play_music(self):
        if self.aktueller_song:
            if not self.paused:
                pygame.mixer.music.load(self.aktueller_song)
                pygame.mixer.music.play()
                self.playing = True  
                self.update_zeit() 
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                self.playing = True  

    
    def pause_music(self):
        if self.aktueller_song:
            pygame.mixer.music.pause()
            self.paused = True
            self.playing = False  

    
    
    def skip_music(self):
        if self.songs:
            try:
                next_index = self.songs.index(self.aktueller_song) + 1
                if next_index < len(self.songs):
                    
                    self.songliste.selection_clear(0, END)
                    self.songliste.selection_set(next_index)
                    self.aktueller_song = self.songs[next_index]
                else:
                    
                    self.songliste.selection_clear(0, END)
                    self.songliste.selection_set(0)
                    self.aktueller_song = self.songs[0]
                self.play_music()  
            except:
                pass

    
    
    def back_music(self):
        if self.songs:
            try:
                prev_index = self.songs.index(self.aktueller_song) - 1
                if prev_index >= 0:
                    
                    self.songliste.selection_clear(0, END)
                    self.songliste.selection_set(prev_index)
                    self.aktueller_song = self.songs[prev_index]
                else:
                    
                    self.songliste.selection_clear(0, END)
                    self.songliste.selection_set(len(self.songs) - 1)
                    self.aktueller_song = self.songs[-1]
                self.play_music()  
            except:
                pass

    
    
    def update_zeit(self):
        if self.playing: 
            current_time = pygame.mixer.music.get_pos() / 1000
            audio = MP3(self.aktueller_song)
            total_time = audio.info.length

            self.progress['maximum'] = total_time
            self.progress['value'] = current_time

            self.time_label.config(text=f"{int(current_time // 60):02}:{int(current_time % 60):02} / {int(total_time // 60):02}:{int(total_time % 60):02}")

        self.musicplayer.after(1000, self.update_zeit)
    
    def set_lautstärke (self, volume):
    
    
        
        
        
        



if __name__ == "__main__":
    GUI()