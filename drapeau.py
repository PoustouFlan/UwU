import json
from random import choice
with open("drapeaux.json", "r") as file:
    drapeaux = json.load(file)
    
def drapeau_aleatoire():
    """
    Retourne un drapeau aléatoire sous la forme d'un tuple
    (Drapeau, Nom)
    """
    return choice(list(drapeaux.items()))