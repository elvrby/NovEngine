import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame 

pygame.mixer.init()

dialog_list = []
current_dialog_index = 0

def update_preview():
    global current_dialog_index

    background = bg_entry.get()
    character = char_entry.get()
    text = dialog_list[current_dialog_index] if dialog_list else "" 

    try:
        bg_img = Image.open(background)
        bg_img = bg_img.resize((800, 450), Image.LANCZOS) 
        bg_photo = ImageTk.PhotoImage(bg_img)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
        preview_canvas.image = bg_photo
    except Exception as e:
        print(f"Error loading background image: {e}")
        preview_canvas.create_rectangle(0, 0, 800, 450, fill="white")  

    try:
        char_img = Image.open(character)
        char_img = char_img.resize((150, 300), Image.LANCZOS) 
        char_photo = ImageTk.PhotoImage(char_img)
        preview_canvas.create_image(10, 100, anchor=tk.NW, image=char_photo)
        preview_canvas.character_image = char_photo 
    except Exception as e:
        print(f"Error loading character image: {e}")
        pass 


    preview_canvas.create_rectangle(0, 400, 800, 450, fill="white")  # Kotak teks
    preview_canvas.create_text(20, 410, anchor=tk.NW, text=text, fill="black", font=("comicsansms", 14), width=760)

def choose_background():
    filepath = filedialog.askopenfilename(title="Pilih Background", filetypes=[("Image files", "*.jpg;*.png")])
    if filepath:
        bg_entry.delete(0, tk.END)
        bg_entry.insert(0, filepath)
        update_preview() 

def choose_character():
    filepath = filedialog.askopenfilename(title="Pilih Character", filetypes=[("Image files", "*.jpg;*.png")])
    if filepath:
        char_entry.delete(0, tk.END)
        char_entry.insert(0, filepath)
        update_preview() 

def choose_music():
    filepath = filedialog.askopenfilename(title="Pilih Background Music", filetypes=[("Audio files", "*.mp3;*.wav")])
    if filepath:
        music_entry.delete(0, tk.END)
        music_entry.insert(0, filepath)
        play_music(filepath) 

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1) 

def on_text_change(event):
    text = text_entry.get("1.0", tk.END).strip()
    if text: 
        dialog_list.append(text)
        text_entry.delete("1.0", tk.END) 
        update_preview()
        update_dialog_history()

def update_dialog_history():
    dialog_history_list.delete(0, tk.END) 
    for dialog in dialog_list:
        dialog_history_list.insert(tk.END, dialog) 

def navigate_dialog(event):
    global current_dialog_index
    if dialog_list:  
        current_dialog_index += 1
        if current_dialog_index >= len(dialog_list):
            current_dialog_index = 0  
        update_preview()

def delete_dialog():
    global current_dialog_index
    selected_index = dialog_history_list.curselection()  # Ambil indeks dialog yang dipilih
    if selected_index:
        dialog_index = selected_index[0]  # Ambil indeks pertama
        dialog_list.pop(dialog_index)  # Hapus dialog dari daftar
        update_dialog_history()  # Perbarui riwayat dialog
        if current_dialog_index >= len(dialog_list):  # Jika indeks saat ini lebih besar dari panjang list
            current_dialog_index = len(dialog_list) - 1  # Set ke indeks terakhir
        update_preview()  # Perbarui pratinjau

root = tk.Tk()
root.title("Visual Novel Editor")

preview_frame = tk.Frame(root)
preview_frame.grid(row=0, column=0, padx=10, pady=10)

preview_canvas = tk.Canvas(preview_frame, width=800, height=450, bg="white")
preview_canvas.pack()

bg_frame = tk.Frame(root)
bg_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
bg_label = tk.Label(bg_frame, text="Background:")
bg_label.pack(side=tk.LEFT)
bg_entry = tk.Entry(bg_frame, width=50)
bg_entry.pack(side=tk.LEFT, padx=5)
bg_button = tk.Button(bg_frame, text="Browse", command=choose_background)
bg_button.pack(side=tk.LEFT)

char_frame = tk.Frame(root)
char_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
char_label = tk.Label(char_frame, text="Character:")
char_label.pack(side=tk.LEFT)
char_entry = tk.Entry(char_frame, width=50)
char_entry.pack(side=tk.LEFT, padx=5)
char_button = tk.Button(char_frame, text="Browse", command=choose_character)
char_button.pack(side=tk.LEFT)

music_frame = tk.Frame(root)
music_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
music_label = tk.Label(music_frame, text="Background Music:")
music_label.pack(side=tk.LEFT)
music_entry = tk.Entry(music_frame, width=50)
music_entry.pack(side=tk.LEFT, padx=5)
music_button = tk.Button(music_frame, text="Browse", command=choose_music)
music_button.pack(side=tk.LEFT)

# Frame untuk teks cerita
text_label = tk.Label(root, text="Story Text:")
text_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
text_entry = tk.Text(root, width=60, height=5)
text_entry.grid(row=5, column=0, padx=10, pady=5)

# Bind event ke text box agar memperbarui pratinjau ketika teks berubah
text_entry.bind("<Return>", on_text_change)  # Menggunakan Enter untuk menambahkan dialog

# Bind event klik untuk navigasi dialog
preview_canvas.bind("<Button-1>", navigate_dialog)  # Menggunakan klik kiri untuk navigasi dialog

# Frame untuk riwayat dialog
history_frame = tk.Frame(root)
history_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
history_label = tk.Label(history_frame, text="Dialog History:")
history_label.pack()
dialog_history_list = tk.Listbox(history_frame, width=50, height=15)
dialog_history_list.pack(side=tk.LEFT, fill=tk.Y)

# Tombol untuk menghapus dialog yang dipilih
delete_button = tk.Button(history_frame, text="X", command=delete_dialog, width=2)
delete_button.pack(side=tk.LEFT, padx=5)  # Tombol 'X' untuk menghapus dialog

# Jalankan loop utama Tkinter
update_preview()  # Tampilkan pratinjau awal
root.mainloop()

# Berhenti memutar musik saat aplikasi ditutup
pygame.mixer.quit()
