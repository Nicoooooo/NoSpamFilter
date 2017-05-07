dico = []

def charger_dictionnaire():
    file = open("dictionnaire1000en.txt", "r")
    for line in file:
        for word in line.split():
            dico.append(word)


def lire_message(chemin):
    file = open(chemin, "r")
    msg = {}
    for word in dico:
        msg[word] = 0
    for line in file:
        for word in line.split():
            if word.upper() in msg:
                msg[word.upper()] += 1
    return msg

charger_dictionnaire()
msg = lire_message("baseapp/ham/0.txt")
print(dico)
print(msg)