import tkinter as tk
from tkinter import messagebox
import random

joueur_nom = ""
mode_ia = "facile"
joueur_score = 0
ia_score = 0
grille = [["" for _ in range(3)] for _ in range(3)]
boutons = [[None for _ in range(3)] for _ in range(3)]

fenetre = tk.Tk()
fenetre.title("Tic Tac Toe - Choix du mode de jeu")

def page_accueil():
    for widget in fenetre.winfo_children():
        widget.destroy()
    tk.Label(fenetre, text="Entrez votre nom :", font=("Arial", 14)).pack(pady=10)
    nom_entry = tk.Entry(fenetre, font=("Arial", 14))
    nom_entry.pack()

    tk.Label(fenetre, text="Choisissez un niveau :", font=("Arial", 14)).pack(pady=10)
    niveau = tk.StringVar(value="facile")
    tk.Radiobutton(fenetre, text="Facile", variable=niveau, value="facile", font=("Arial", 12)).pack()
    tk.Radiobutton(fenetre, text="Intermédiaire", variable=niveau, value="moyen", font=("Arial", 12)).pack()
    tk.Radiobutton(fenetre, text="Forte", variable=niveau, value="fort", font=("Arial", 12)).pack()

    def valider():
        global joueur_nom, mode_ia
        joueur_nom = nom_entry.get().strip()
        mode_ia = niveau.get()
        if joueur_nom:
            lancer_jeu()

    tk.Button(fenetre, text="Jouer", font=("Arial", 14), command=valider).pack(pady=10)

def lancer_jeu():
    for widget in fenetre.winfo_children():
        widget.destroy()
    global score_label
    score_label = tk.Label(fenetre, text=f"{joueur_nom} (X) : {joueur_score}   |   IA (O) : {ia_score}", font=("Arial", 14))
    score_label.grid(row=0, column=0, columnspan=3, pady=5)

    for i in range(3):
        for j in range(3):
            bouton = tk.Button(fenetre, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda x=i, y=j: clic_utilisateur(x, y))
            bouton.grid(row=i + 1, column=j)
            boutons[i][j] = bouton
    reset_grille()

def reset_grille():
    global grille
    grille = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            boutons[i][j].config(text="", state="normal")

def victoire(sym):
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] == sym:
            return True
        if grille[0][i] == grille[1][i] == grille[2][i] == sym:
            return True
    if grille[0][0] == grille[1][1] == grille[2][2] == sym:
        return True
    if grille[0][2] == grille[1][1] == grille[2][0] == sym:
        return True
    return False

def egalite():
    return all(cell != "" for row in grille for cell in row)

def clic_utilisateur(x, y):
    global joueur_score
    if grille[x][y] == "":
        grille[x][y] = "X"
        boutons[x][y].config(text="X", state="disabled")
        if victoire("X"):
            joueur_score += 1
            messagebox.showinfo("Victoire", f"{joueur_nom} a gagné !")
            update_score()
            reset_grille()
            return
        elif egalite():
            messagebox.showinfo("Égalité", "Match nul !")
            reset_grille()
            return
        fenetre.after(500, tour_ia)

def tour_ia():
    global ia_score
    x, y = ia_facile() if mode_ia == "facile" else ia_moyen() if mode_ia == "moyen" else ia_forte()
    grille[x][y] = "O"
    boutons[x][y].config(text="O", state="disabled")
    if victoire("O"):
        ia_score += 1
        messagebox.showinfo("Défaite", "L'IA a gagné !")
        update_score()
        reset_grille()
    elif egalite():
        messagebox.showinfo("Égalité", "Match nul !")
        reset_grille()

def update_score():
    score_label.config(text=f"{joueur_nom} (X) : {joueur_score}   |   IA (O) : {ia_score}")

def ia_facile():
    cases_vides = [(i, j) for i in range(3) for j in range(3) if grille[i][j] == ""]
    return random.choice(cases_vides)
def ia_moyen():
    for i in range(3):
        for j in range(3):
            if grille[i][j] == "":
                grille[i][j] = "O"
                if victoire("O"):
                    grille[i][j] = ""
                    return i, j
                grille[i][j] = ""
    for i in range(3):
        for j in range(3):
            if grille[i][j] == "":
                grille[i][j] = "X"
                if victoire("X"):
                    grille[i][j] = ""
                    return i, j
                grille[i][j] = ""
    return ia_facile()

def ia_forte():
    return ia_moyen()  


page_accueil()
fenetre.mainloop()