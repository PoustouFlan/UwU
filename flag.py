import json
from random import choice
with open("flags.json", "r") as file:
    flags = json.load(file)
    
def random_flag():
    """
    Retourne un drapeau aléatoire sous la forme d'un tuple
    (Drapeau, Nom)
    """
    return choice(list(flags.items()))