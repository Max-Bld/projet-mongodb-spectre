# Trier les listes alpha 
def sort_listes(liste_alpha, liste_valeur):
    
    sorted_pairs = sorted(enumerate(liste_alpha), key=lambda x: x[1])
    sorted_indices, sorted_liste_alpha = zip(*sorted_pairs)
    sorted_liste_valeur = [liste_valeur[i] for i in sorted_indices]
    
    return list(sorted_liste_alpha), list(sorted_liste_valeur) 
