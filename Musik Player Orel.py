from tkinter import *
from tkinter import filedialog, ttk
import pygame
import os
import random
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
        self.shuffle_mode = False  

    
        self.musicplayer.bind("<space>", lambda event: self.toggle_play_pause())
        self.musicplayer.bind("<Left>", lambda event: self.back_music())
        self.musicplayer.bind("<Right>", lambda event: self.skip_music())

        
        
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

        self.volume_label = Label(self.musicplayer, text="Lautstärke:", bg="dark blue", fg="white")
        self.volume_label.pack(pady=5)

        self.volume_scale = ttk.Scale(self.musicplayer, from_=0, to=1, orient=HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(0.5)  
        self.volume_scale.pack(pady=5)
        
        
        self.play_button_bild = PhotoImage(file="play.png")
        self.pause_button_bild = PhotoImage(file="pause.png")

       
        button_groeße = (40, 40) 
        self.play_button_bild = self.play_button_bild.subsample(int(self.play_button_bild.width() / button_groeße[0]), int(self.play_button_bild.height() / button_groeße[1]))
        self.pause_button_bild = self.pause_button_bild.subsample(int(self.pause_button_bild.width() / button_groeße[0]), int(self.pause_button_bild.height() / button_groeße[1]))
        
        self.frame = Frame(self.musicplayer, bg="white")
        self.frame.pack(pady=10)
        
        
        self.play_pause_button = Button(self.frame, image=self.play_button_bild, borderwidth=0, command=self.toggle_play_pause, bg="dark blue")
        self.play_pause_button.grid(row=0, column=1, padx=7)
        
        
        self.back_button_bild = PhotoImage(file="back.png")
        self.back_button_bild = self.back_button_bild.subsample(int(self.back_button_bild.width() / button_groeße[0]), int(self.back_button_bild.height() / button_groeße[1]))
        self.backbutton = Button(self.frame, image=self.back_button_bild, borderwidth=0, command=self.back_music, bg="dark blue")
        self.backbutton.grid(row=0, column=0, padx=7)
        
        
        self.next_button_bild = PhotoImage(file="skip.png")
        self.next_button_bild = self.next_button_bild.subsample(int(self.next_button_bild.width() / button_groeße[0]), int(self.next_button_bild.height() / button_groeße[1]))
        self.skipbutton = Button(self.frame, image=self.next_button_bild, borderwidth=0, command=self.skip_music, bg="dark blue")
        self.skipbutton.grid(row=0, column=2, padx=7)

        
        self.shuffle_button_bild = PhotoImage(file="shuffle.png")
        self.shuffle_button_bild = self.shuffle_button_bild.subsample(int(self.shuffle_button_bild.width() / button_groeße[0]), int(self.shuffle_button_bild.height() / button_groeße[1]))
        self.shuffle_button = Button(self.frame, image=self.shuffle_button_bild, borderwidth=0, command=self.toggle_shuffle, bg="dark blue")
        self.shuffle_button.grid(row=0, column=3, padx=7)


        self.musicplayer.mainloop()

    
    def toggle_play_pause(self):
        if self.playing and not self.paused:
            self.pause_music()
        else:
            self.play_music()

    
    def play_music(self):
        if self.aktueller_song:
            if not self.paused:
                pygame.mixer.music.load(self.aktueller_song)
                pygame.mixer.music.play()
                self.playing = True  
                self.paused = False
                self.update_zeit() 
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                self.playing = True  
            self.update_play_pause_button()

    
    def pause_music(self):
        if self.aktueller_song:
            pygame.mixer.music.pause()
            self.paused = True
            self.playing = False  
            self.update_play_pause_button()

    
    def update_play_pause_button(self):
        if self.playing and not self.paused:
            self.play_pause_button.config(image=self.pause_button_bild)
        else:
            self.play_pause_button.config(image=self.play_button_bild)

    
    def skip_music(self):
        if self.songs:
            try:
                if self.shuffle_mode:
                    next_index = random.randint(0, len(self.songs) - 1)
                else:
                    next_index = self.songs.index(self.aktueller_song) + 1
                    if next_index >= len(self.songs):
                        next_index = 0  

                self.songliste.selection_clear(0, END)
                self.songliste.selection_set(next_index)
                self.aktueller_song = self.songs[next_index]
                self.play_music()
            except:
                pass

    
    
    def back_music(self):
        if self.songs:
            try:
                if self.shuffle_mode:
                    prev_index = random.randint(0, len(self.songs) - 1)
                else:
                    prev_index = self.songs.index(self.aktueller_song) - 1
                    if prev_index < 0:
                        prev_index = len(self.songs) - 1  

                self.songliste.selection_clear(0, END)
                self.songliste.selection_set(prev_index)
                self.aktueller_song = self.songs[prev_index]
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

    
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    
    
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.shuffle_button.config(bg="green")  
        else:
            self.shuffle_button.config(bg="dark blue") 




if __name__ == "__main__":
    GUI()