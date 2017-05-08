import math

try:
    range_spam = int(input("Nombre de spam de la base d'apprentissage ? (max 500)"))
    range_ham = int(input("Nombre de ham de la base d'apprentissage ? (max 2500)"))

    nbtests_spam = int(input("Nombre de spam a tester ? (max 500)"))
    nbtests_ham = int(input("Nombre de ham a tester ? (max 500)"))
except ValueError:
    print("Not a number")

epsilon = 1
dico = []
baseapp_spam = []
baseapp_ham = []
variances_ham = {}
variances_spam = {}

count_testes = [0]
count_erreurs = [0]

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
    for i in range (range_ham):
        baseapp_ham.append(lire_message('baseapp/ham/'+str(i)+'.txt'))
    for i in range (range_spam):
        if i != 115 and i != 262 and i != 319 and i != 322 and i != 323 and i != 499: # spams non utf-8
            baseapp_spam.append(lire_message('baseapp/spam/'+str(i)+'.txt'))

#methode 0
def calculer_bj(baseapp):
    bjs = {}

    for word in dico:
        bjs[word] = 0

    for msg in baseapp:
        for word in dico:
            if msg[word] > 0:
                bjs[word] += 1

    if len(baseapp) > 0:
        for word in dico:
            bjs[word] = (bjs[word] + epsilon) / (2 * epsilon + len(baseapp))

    return bjs

def calculer_probabilite(message, bjs, pyy):
    #proba = (1 / P(X = x)) * P(Y = y) * mult ( bjs)^xi * (1 - bjs)^(1-xi)
    #optimise en appliquant ln() sur toute la formule et en considerant que xi est soit 0 soit 1
    proba = math.log(pyy)
    for word in dico:
        if message[word] == 0:
            proba += math.log(1 - bjs[word])
        else:
            proba += math.log(bjs[word])

    return proba

def predire(message, bjham, bjspam, pyham, pyspam):
    proba_spam = calculer_probabilite(message, bjspam, pyspam)
    proba_ham = calculer_probabilite(message, bjham, pyham)
    type = 'ham'

    if proba_spam > proba_ham:
        type = 'spam'

    return proba_spam, proba_ham, type

def tester_message(type, no, bjham, bjspam, pyham, pyspam):
    message = lire_message('basetest/' +  type + '/' + str(no) + '.txt')
    pspam, pham, prediction = predire(message, bjham, bjspam, pyham, pyspam)
    erreur = ''

    count_testes[0] += 1
    if type != prediction:
        erreur = ' *** erreur ***'
        count_erreurs[0] += 1

    print(type.upper() + ' numero ' + str(no) + ' : P(Y=SPAM | X=x) = ' + str(pspam) +', P(Y=HAM | X=x) = ' + str(pham) + '  => identifie comme un ' + prediction.upper() + erreur)
    
def tester_messages(norange, type, bjham, bjspam, pyham, pyspam):
    for no in range(norange):
        tester_message(type, no, bjham, bjspam, pyham, pyspam)

# methode 1
def calculer_variance(baseapp):
    esperances = calculer_bj(baseapp)
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


print('\nApprentissage realise sur ' + str(range_spam) + ' SPAMs et ' + str(range_ham) + ' HAMs\n')

charger_dictionnaire()
charger_base_app()

bjham = calculer_bj(baseapp_ham)
bjspam = calculer_bj(baseapp_spam)
variancesspam = calculer_variance(baseapp_spam)
variancesham = calculer_variance(baseapp_ham)
pyham = len(baseapp_ham) / float(len(baseapp_ham) + len(baseapp_spam))
pyspam = len(baseapp_spam) / float(len(baseapp_ham) + len(baseapp_spam))

tester_messages(nbtests_spam, 'spam', bjham, bjspam, pyham, pyspam)
count_erreurs_spam = count_erreurs[0]
count_erreurs[0] = 0
tester_messages(nbtests_ham, 'ham', bjham, bjspam, pyham, pyspam)
count_erreurs_ham = count_erreurs[0]

print('\nResultats : ')
print('Erreur de test sur les ' + str(nbtests_spam) + ' SPAM       :  ' + str(int( 100 * count_erreurs_spam / float(nbtests_spam) )) + ' %')
print('Erreur de test sur les ' + str(nbtests_ham)  + ' HAM        :  ' + str(int( 100 * count_erreurs_ham / float(nbtests_spam) )) + ' %')
print('Erreur de test globale sur ' + str(nbtests_ham + nbtests_spam) + ' mails  :  ' + str(int( 100 * (count_erreurs_ham + count_erreurs_spam) / float(nbtests_spam + nbtests_ham) )) + ' %')
