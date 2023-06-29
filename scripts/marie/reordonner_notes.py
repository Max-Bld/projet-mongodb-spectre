# Réordonner les notes de musique 
def reordonner_notes(liste_note, liste_valeur):
    new_liste_note = []
    new_liste_valeur = []

    for note, valeur in zip(liste_note, liste_valeur):
        num = ''
        letters = ''
        if '#' in note:
            parts = note.split('#')
            num = parts[1]
            letters = parts[0] + '#'
        else:
            for char in note:
                if char.isdigit():
                    num += char
                else:
                    letters += char

        if num and num in letters:
            letters = letters.replace(num, '')

        new_note = letters + num
        new_liste_note.append(new_note)
        new_liste_valeur.append(valeur)

    sorted_indices = sorted(range(len(new_liste_note)), key=lambda x: (int(new_liste_note[x][:-1]) if new_liste_note[x][:-1].isdigit() else float('inf'), new_liste_note[x][-1]))

    sorted_liste_note = [new_liste_note[i] for i in sorted_indices]
    sorted_liste_valeur = [new_liste_valeur[i] for i in sorted_indices]

    return sorted_liste_note, sorted_liste_valeur
