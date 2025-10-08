import os

class values:
    dire = ""
    listn = []

def ochis():
    values.listn = []
    
def vybkat(foled):
    os.chdir(foled)

def vybfay(name):
    values.listn.append(name)

def pre(sche):
    for item in values.listn:
        os.rename(item, f"{sche}. {item}")
        sche += 1