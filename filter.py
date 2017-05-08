import math

range_spam = 499 #500 Bug pour le spam 115, qui n'est pas en utf-8
range_ham = 2499

nbtests_spam = 20
nbtests_ham = 20

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
    # Bug pour le spam 115, qui n'est pas en utf-8
    for i in range (range_spam):
      baseapp_spam.append(lire_message('baseapp/spam/'+str(i)+'.txt'))

#methode 0
def calculer_bj(baseapp):
    bjs = {}

    for word in dico:
        bjs[word] = 0

    for msg in baseapp:
        for word in dico:
            bjs[word] += msg[word]

    if len(baseapp) > 0:
        for word in dico:
            bjs[word] = (bjs[word] + epsilon) / float(2 * epsilon + len(baseapp))
    
    return bjs

def calculer_probabilite(message, bjs, pyy):
    #proba = (1 / P(X = x)) * P(Y = y) * mult ( bjs)^xi * (1 - bjs)^(1-xi)
    proba = 1 * pyy
    for word in dico:
        proba *= math.pow(bjs[word], message[word]) * math.pow(1 - bjs[word], 1 - message[word])

    return abs(proba)

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

    # print(type.upper() + ' numero ' + str(no) + ' identifie comme un ' + prediction.upper() + erreur)

    print(type.upper() + ' numero ' + str(no) + ' : P(Y=SPAM | X=x) = ' + str(pspam) +', P(Y=HAM | X=x) = ' + str(pham))
    print('\t\t\t\t\t => identifie comme un ' + prediction.upper() + erreur + '\n')

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


print('Apprentissage realise sur ' + str(range_spam) + ' SPAMs et ' + str(range_ham) + ' HAMs')

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

print('Resultats : ')
print('Erreur de test sur les ' + str(nbtests_spam) + ' SPAM       :  ' + str(int( 100 * count_erreurs_spam / float(nbtests_spam) )) + ' %')
print('Erreur de test sur les ' + str(nbtests_ham)  + ' HAM        :  ' + str(int( 100 * count_erreurs_ham / float(nbtests_spam) )) + ' %')
print('Erreur de test globale sur ' + str(nbtests_ham)  + ' mails  :  ' + str(int( 100 * (count_erreurs_ham + count_erreurs_spam) / float(nbtests_spam + nbtests_ham) )) + ' %')
