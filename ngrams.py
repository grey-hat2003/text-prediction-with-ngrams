import os
import re

corpus = 'corpora/testing.txt'

first_words = {}
second_words = {}
transitions = {}

def add_to_dict(dictionary, key, val):
    if key not in dictionary:
        diction[key] = []
        #making an empty list as a value for the new key
    
    dictionary[key].append(val)

# def update_dict(diction, key, val):
#     if key not in diction:
#         diction[key] = {}

#     diction[key] = diction.get(val, 0) + 1
#     # no need of [value]


def calculate_probab(listy):
    probab_dict = {}
    listy_length = len(listy)

    for element in listy:
        probab_dict[element] = probab_dict.get(element, 0) + 1
    
    # for key, value in probab_dict.items():
    #     probab_dict[key] = value/listy_length

    return probab_dict
    
def train_markov():
#this function is the real logic part. We are implementing markov chains here.
    data_base = open(corpus, 'r')
    #opening our corpus in read mode

    for sentence in data_base:       #scanning through every line in our corpus
        sentence = re.sub(r"[,.\"\\!@#$%^&*(){}?/;:<>+=-]", " ", sentence)   #clearing the sentence from any punctuation marks
        words = sentence.strip().lower().split()    #extracting words and make a list of the same
        no_of_words = len(words)    #the size of this list gives us the number of words in that sentence

        for x in range(no_of_words):
            #we iterate through every word of a sentence
            #word variable is an individual word and x is the index or word number
            word = words[x]

            if x == 0:
                first_words[word] = first_words.get(word, 0) + 1
                #we make a dict of all the possible first words as the key and calculate its frequency as the value

            else:
                prev_word = words[x-1] #we extract the previous word 


                if x == 1:
                    add_to_dict(second_words, prev_word, word)

                else:
                    second_prev_word = words[x-2]
                    add_to_dict(transitions, (second_prev_word, prev_word), word)

    #total_first_words = sum(first_words.values())

    #probability 

    # for key, value in first_words.items():
    #     first_words[key] = value / total_first_words  
        #doing this gives us the relative probability after processing every first word and its possible subsequent words

    for prev_word, next_words in second_words.items(): 
        #prev_word is the key and next_words is a list type value 
        second_words[prev_word] = calculate_probab(next_words)

    for word_group, next_words in transitions.items():
        #word_group is the key and next_words is a list type value
        transitions[word_group] = calculate_probab(next_words)

def first_words_sort():
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

# print(first_words)
# print()
# print(second_words)
# print()
# print(transitions)
