import os
import re

corpus = 'corpus\\a.txt'

first_words = {}
second_words = {}
transitions = {}

#adds new words(values) to the dictionary based on the key
def add_to_dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

#returns dictionary of words and their corresponding probabilities from the given list
def calculate_probab(listy):
    probab_dict = {}
    total_words = len(listy)
    #loop to count words
    for word in listy:
        probab_dict[word] = probab_dict.get(word,0) + 1
    """
    #loop to calculate probability of the words
    for word,word_count in probab_dict.items():
        probab_dict[word] = word_count/total_words
    """
    return probab_dict

def train_markov():
    #MAIN LOGIC - MARKOV CHAIN MODEL
    data_base = open(corpus,'r')

    #loop to iterate through every line in corpus
    for sentence in data_base:
        #remove any special characters  if ppresent and replace with whitespace
        sentence = re.sub(r"[,.\"\'\\!@#$%^&*(){}?/;:<>+=-]"," ",sentence)
        #r -> string to be treated raw;ignore escape sequences
        words  = sentence.strip().lower().split()
        #strip white spaces before/after sentences, convert to lowercase and split into a list
        no_of_words = len(words)

        for i in range(no_of_words):
            word = words[i]
            #store the 1st word in first_words
            if(i==0):
                #if word not present: add the word and initialize its counter to 0
                first_words[word] = first_words.get(word,0) + 1
            else:
                #get the previous word
                prev_word = words[i-1]
                # if it is the last word add it to transitions dictionary with suggestion with end of sentence
                #if(i==(no_of_words-1)):
                #    add_to_dict(transitions,(prev_word,word),".")
                #if it is a second word add to second_words dictionary
                if(i==1):
                    add_to_dict(second_words,prev_word,word)
                #else add second_prev_wordand prev_word as key and word as value
                else:
                    second_prev_word = words[i-2]
                    #print(second_prev_word,prev_word,word)
                    add_to_dict(transitions, (second_prev_word,prev_word),word)
    #probability dictionary of second possible words based on first word
    for prev_word,next_words in second_words.items():
        second_words[prev_word] = calculate_probab(next_words)
    #probability of words based on previous two words
    for prev_two_words,next_words in transitions.items():
        transitions[prev_two_words] = calculate_probab(next_words)
    #calculating probability of each word in the list
    """
    #calculating probabilites of first occuring words
    total_first_words = sum(first_words.values())
    for word,count in first_words.items():
    first_words[word] = count/total_first_words
    """


#sorted list of first occuring words based on their probabilites in descending order
#display suggestion when input is ""
def suggest_first_words():
    return sorted(first_words, key = first_words.get, reverse = True)


def update_corpus(sentence):
    sentence = re.sub(r"[,.\"\'\\!@#$%^&*(){}?/;:<>+=-]"," ",sentence)
    f = open(corpus,"a")
    f.write("\n"+sentence)
    f.close()

def suggestions(in_put):
    #if input is a single word refer second_words
    if(type(in_put)==str):
        #sorted list of second occuring words based on their probabilites in descending order
        suggestion_dict = second_words.get(in_put)
        if(suggestion_dict is not None):
            return sorted(suggestion_dict,key=suggestion_dict.get,reverse=True)
    #if input are two words refer transitions dictionary
    if(type(in_put)==tuple):
        #sorted list of words, occuring after two words, based on their probabilites in descending order
        suggestion_dict = transitions.get(in_put)
        if(suggestion_dict is not None):
            return sorted(suggestion_dict,key=suggestion_dict.get,reverse=True)
    return []

#train_markov()
#print("----------------Markov Data Model----------------")
#print(first_words)
#print()
#print(second_words)
#print()
#print(transitions)
