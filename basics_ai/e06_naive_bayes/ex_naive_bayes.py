"""
Implement a naive Bayes classificator for spam emails.

We supply a database of spam/ham emails as well as a small library to read it.
The database is in the subfolder database. All spam mails are in
database/spam_mails, all ham emails in database/ham_emails.

To load the database write

    db = spamAssassinDatabase.SpamAssassinDatabase(data_path='./database',
                                                   training_test_ratio=.75)

The data_path parameter gives the path to the database, the training_test_ratio
defines which part of the database should be read as training data and which
part should be used as test data.

You can then access the data with:

    word_count_spam = {}
    word_count_ham = {}

    for mail in db.read_training_mails():
        for w in mail.words:
             if mail.label == 'spam':
                 word_count_spam[w] += 1
             elif mail.label == 'ham':
                 word_count_ham[w] += 1

You can use the word frequency to estimate the probabilities p(x|c).
"""
import spamAssassinDatabase
import random
from math import log,exp


class NaiveBayes(object):
    def __init__(self, database):
        ''' Train the classificator with the given database. '''

        self.P_c = {}
        self.P_c_w = {'spam':{}, 'ham':{}}
        
        #split trainings data by annotaion
        by_class = {'spam':[], 'ham':[]}
        for mail in database.read_training_mails():
            by_class[mail.label].append(mail)
        
        #calculate prior probs
        n_spams = len(by_class['spam'])
        n_hams = len(by_class['ham'])
        n_mails = n_hams+n_spams
        self.P_c['spam'] = n_spams/float(n_mails)
        self.P_c['ham'] = n_hams/float(n_mails)
        
        #calculate word probs
        for smail in by_class['spam']:
            for word in set(smail.words):  ##set evt unnoetig
                if word not in self.P_c_w['spam']:
                    self.P_c_w['spam'][word] = 0
                self.P_c_w['spam'][word] += 1

        for hmail in by_class['ham']:
            for word in hmail.words:  ##set evt unnoetig
                if word not in self.P_c_w['ham']:
                    self.P_c_w['ham'][word] = 0
                self.P_c_w['ham'][word] += 1
        #P_c_w[spam][word] haelt jetzt die Anzahl an Spammails die min. einmal 'wort' enthalten.
        for word in self.P_c_w['spam']:
            self.P_c_w['spam'][word] /= float(n_spams)
        for word in self.P_c_w['ham']:
            self.P_c_w['ham'][word] /= float(n_hams)
        #P_c_w[spam][word] haelt jetzt die wahrscheinlichkeit, dass 'wort' in einer Spammail vorkommt
        print "training ended"
        print self.P_c

    def spam_prob(self, email):
        ''' Compute the probability for the given email that it is spam. '''
        #calac prior prob
        prob_spam = self.P_c['spam']
        prob_ham = self.P_c['ham']
        
        #calc posterior
        for word in email.words:
            if (word in self.P_c_w['spam']) and (word in word in self.P_c_w['ham']):
                prob_spam *= self.P_c_w['spam'][word]
                prob_ham *= self.P_c_w['ham'][word]
                

        print prob_spam, prob_ham
        return prob_spam/(prob_spam+prob_ham+1e-321)


def main():
    db = spamAssassinDatabase.SpamAssassinDatabase(data_path='./database',
                                                   training_test_ratio=.75)

    nb = NaiveBayes(db)
    ##
    #tp = 0
    #tn = 0
    #fp = 0
    #fn = 0
    ##
    for n, mail in enumerate(db.read_test_mails()):
        prob = nb.spam_prob(mail)
        correct = ((prob > .5 and mail.label == 'spam')
                   or (prob <= .5 and mail.label == 'ham'))
        ##
        #if correct and mail.label == 'spam':
        #    tp += 1
        #elif correct and mail.label == 'ham':
        #    tn += 1
        #elif (not correct) and mail.label == 'spam':
        #    fn += 1
        #elif (not correct) and mail.label == 'ham':
        #    fp += 1
        ##
        print("Mail {} -- p(c|x) = {} -- is {} -- Labeling correct: {}"
              .format(n, prob, mail.label, correct))
    ##
    #print tp
    #print tn
    #print fp
    #print fn
    #p = tp/float(tp+fp) 
    #r = tp/float(tp+fn)
    #print "Precision=",p
    #print "Recall=",r
    #print "F1=",(2*p*r)/(p+r)
    ##

if __name__ == '__main__':
    main()
