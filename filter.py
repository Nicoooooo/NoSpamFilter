import math

dico = []
baseapp_spam = []
baseapp_ham = []
variances_ham = {}
variances_spam = {}

def charger_dictionnaire():
    file = open("dictionnaire1000en.txt", "r")
    for line in file:
        for word in line.split():
            if len(word) >= 3:
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
        baseapp_ham.append(lire_message('baseapp/ham/'+str(i)+'.txt'))
    # Bug pour le spam 115, qui n'est pas en utf-8
    #for i in range (500):
    #   baseapp_spam.append(lire_message('baseapp/spam/'+str(i)+'.txt'))


def calculer_eperance(baseapp):
    esperance = {}

    for word in dico:
        esperance[word] = 0

    for msg in baseapp:
        for word in dico:
            esperance[word] += msg[word]

    if len(baseapp) > 0:
        for word in dico:
            esperance[word] /= float(len(baseapp))
    
    return esperance

def calculer_variance(baseapp):
    esperances = calculer_eperance(baseapp)
    variance = {}

    for word in dico:
        variance[word] = 0

    for msg in baseapp:
        for word in dico:
            variance[word] += pow(msg[word] - esperances[word], 2)

    if len(baseapp) > 0:
        for word in dico:
            variance[word] *= (1 / float(len(baseapp) - 1))
    
    return variance

# p(x|Y = y) 
def calculer_probabilite(x, esperance, variance2):
    return (1 / (math.sqrt(2 * math.pi * esperance))) * math.exp( - math.pow(x - esperance, 2) / (2 * variance2))


charger_dictionnaire()
charger_base_app()
msg = lire_message("baseapp/ham/0.txt")
variances_ham = calculer_variance(baseapp_ham)
variances_spam = calculer_variance(baseapp_spam)
#print(dico)
#print(msg)
#print(len(baseapp))
# print(baseapp_ham[0])

print(variances_ham)