import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence
from pynput import keyboard
import threading
        
# Fonction qui permet d'afficher le shiny sélectionné.
def displayShiny():
    file = filedialog.askopenfilename(
    title="Sélectionnez une image",
    filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")],
    )
    
    # Vérifie si un fichier est sélectionné.
    if not file:
        return
    
    if hasattr(canva, "after_id") and canva.after_id:
        root.after_cancel(canva.after_id)
        canva.after_id = None
        
    img = Image.open(file)
    
    # Permet de récupérer les frames du fichier sélectionné sous format "Gif" sinon affiche une image sous format ".png, .jpeg, .jpg".
    if getattr(img, "is_animated", False):
        frames = []
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")
            frame = frame.copy().resize((170, 200), Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            
        canva.frames = frames
        animate_gif(0)
    else:
        img = img.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        canva.itemconfig(image_canva, image=photo)
        canva.image = photo
        canva.after_id = None
        
# Fonction qui anime le GIF.
def animate_gif(index):
    frames = canva.frames
    frame = frames[index]
    
    canva.itemconfig(image_canva, image=frame)
    canva.image = frame
    
    next_index = (index + 1) % len(frames)
    canva.after_id = root.after(50, animate_gif, next_index)

# Variable nommée count.
count = 0
# Fonction qui applique les touches 'a', 'e', et 'r' pour incrémenter, décrémenter, ou réinitialiser le compteur.
def gest(event):
    if event.keysym == 'a':
        shinyCount()
    elif event.keysym == 'e':
        removeCount()
    elif event.keysym == 'r':
        shinyReset()

# Fonction qui incrémente le compteur.
def shinyCount():
    global count
    count += 1
    suffixe = "" if count <= 1 else "s"
    labelShiny.config(text=f"Reset{suffixe}: {count}")
    
# Fonction qui décrémente le compteur.
def removeCount():
    global count
    count -= 1
    if count < 0:
        count = 0
    mot = "Resets" if count > 1 else "Reset"
    labelShiny.config(text=f"{mot}: {count}")

# Fonction qui réinitialise le compteur à 0.
def shinyReset():
    global count
    count = 0
    labelShiny.config(text="Reset: 0")
    


# Fonction qui détecte les inputs en arrière plan.
def on_press(key):
    try:
        if key.char == 'a':
            shinyCount()
        elif key.char == 'e':
            removeCount()
        elif key.char == 'r':
            shinyReset()
    except AttributeError:
        pass 
    
# Permet d'éviter que le programme se bloque.
def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

threading.Thread(target=start_listener, daemon=True).start()

# Interface Tkinter
root = tk.Tk()
try:
    root.iconbitmap("kenma.ico")
except:
    pass

root.geometry("600x500")
root.minsize(600, 500)
root.title("Wish shiny counter")
root.config(background="#1e2a38")
# root.bind('<a>', gest)
# root.bind('<e>', gest)
# root.bind('<r>', gest)


# Bouton appliqué dans l'interface permettant de sélectionner un fichier.
btn = tk.Button(root, font="Arial", text="Shiny selector", command=displayShiny)
btn.pack(pady=50)

# Ajoute un canvas de la même couleur que le fond.
canva = tk.Canvas(root, width=200, height=200, highlightthickness=0, bg="#1e2a38")
canva.pack(pady=20)
canva.after_id = None

# Crée un l'objet au centre du canvas
image_canva = canva.create_image(100, 100)

# Crée une frame permettant aux boutons d'être alignés.
frameBtn = tk.Frame(root, bg='#1e2a38')
frameBtn.pack(pady=10)

# Bouton qui incrémente le compteur.
countBtn = tk.Button(frameBtn, font="Arial", text="+", command=shinyCount, )
countBtn.pack(side="left", padx=5)

# Bouton qui réinitialise le compteur à 0.
resetBtn = tk.Button(frameBtn, font="Arial", text="Reset", command=shinyReset)
resetBtn.pack(side="left", padx=5)

# Bouton qui décrémente le compteur.
removeBtn = tk.Button(frameBtn, font="Arial", text="-", command=removeCount)
removeBtn.pack(side="left", padx=5,)

# Crée un Label permettant d'afficher le compteur.
labelShiny = tk.Label(root, font="Arial", text=f"Reset: {count}")
labelShiny.pack(pady=10)

# Garde la fenêtre active.
root.mainloop()