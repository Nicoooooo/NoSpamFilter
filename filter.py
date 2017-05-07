dico = []
baseapp = []

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

def charger_base_app():
    for i in range (2500):
        baseapp.append(lire_message('baseapp/ham/'+str(i)+'.txt'))
    # Bug pour le spam 115, qui n'est pas en utf-8
    #for i in range (500):
    #   baseapp.append(lire_message('baseapp/spam/'+str(i)+'.txt'))

charger_dictionnaire()
charger_base_app()
msg = lire_message("baseapp/ham/0.txt")
print(dico)
print(msg)
print(len(baseapp))
print(baseapp[0])