import os
import re

corpus = 'corpora/training.txt'

first_words = {}
second_words = {}
transitions = {}

def add_to_dict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
        #making an empty list as a value for the new key

    dictionary[key].append(value)

#returns dictionary of words and their corresponding frequencies from the given list
def calculate_probab(listy):
    probab_dict = {}
    total_words = len(listy)

    for word in listy:
        probab_dict[word] = probab_dict.get(word, 0) + 1

    """
    #loop to calculate probability of the words
    for word,word_count in probab_dict.items():
        probab_dict[word] = word_count/total_words
    """
    return probab_dict

def train_markov():
    #this function is the real logic part. We are implementing markov chains here.
    data_base = open(corpus,'r')

    for sentence in data_base:  #scanning through every line in our corpus
        
        sentence = re.sub(r"[,.\"\'\\!@#$%^&*(){}?/;:<>+=-]", " ", sentence)    #clearing the sentence from any punctuation marks
        #r -> string to be treated raw; ignore escape sequences

        words  = sentence.strip().lower().split()   #extracting words and make a list of the same
        no_of_words = len(words)    #the size of this list gives us the number of words in that sentence

        for i in range(no_of_words):
            #we iterate through every word of a sentence
            #word variable is an individual word and 'i' is the index or word number

            word = words[i]
            
            if i == 0:
                first_words[word] = first_words.get(word, 0) + 1
                #we make a dict of all the possible first words as the key and calculate its frequency as the value

            else:
                prev_word = words[i-1]  #we extract the previous word

                # if it is the last word add it to transitions dictionary with suggestion with end of sentence
                #if(i==(no_of_words-1)):
                #    add_to_dict(transitions,(prev_word,word),".")
                #if it is a second word add to second_words dictionary

                if i == 1:
                    add_to_dict(second_words, prev_word, word)

                else:
                    second_prev_word = words[i-2]
                    add_to_dict(transitions, (second_prev_word, prev_word), word)

    for prev_word, next_words in second_words.items():
        #prev_word is the key and next_words is a list type value
        second_words[prev_word] = calculate_probab(next_words)

    for prev_two_words, next_words in transitions.items():
        #prev_two_words is the key and next_words is a list type value
        transitions[prev_two_words] = calculate_probab(next_words)

    """    
    #calculating probability of each word in the list
    #calculating probabilites of first occuring words
    total_first_words = sum(first_words.values())
    for word,count in first_words.items():
    first_words[word] = count/total_first_words
    """


#display suggestions when input is ""
def suggest_first_words():
    return sorted(first_words, key = first_words.get, reverse = True)


def update_corpus(sentence):
    sentence = re.sub(r"[,.\"\'\\!@#$%^&*(){}?/;:<>+=-]", " ", sentence)
    f = open(corpus, "a")
    f.write("\n" + sentence)
    f.close()

def suggestions(in_put):
    
    if(type(in_put) == str):
        #sorted list (descending) of second occuring words based on their frequencies
        suggestion_list = second_words.get(in_put)

        if(suggestion_list is not None):
            return sorted(suggestion_list, key = suggestion_list.get, reverse = True)

    if(type(in_put) == tuple):
        #sorted list (descending) of words occuring after two words, based on their frequencies
        suggestion_list = transitions.get(in_put)

        if(suggestion_list is not None):
            return sorted(suggestion_list, key = suggestion_list.get, reverse = True)

    return []

#train_markov()
#print("----------------Markov Data Model----------------")
#print(first_words)
#print()
#print(second_words)
#print()
#print(transitions)
