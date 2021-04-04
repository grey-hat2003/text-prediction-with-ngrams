import os

data_base = 'abc.txt'

first_possible_words = {}
second_possible_words = {}
transitions = {}

def add_to_dict(dict, key, value):
    if key not in dict:
        dict[key] = []

    dict[key].append(value)

def get_next_probability(given_list):   #returns dictionary
    probability_dict = {}
    given_list_length = len(given_list)

    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1

    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length

    return probability_dict

def trainMarkovModel():
    for line in open(data_base):   #iterating through every line
        tokens = line.rstrip().lower().split()   #made a list of all the words in the line
        tokens_length = len(tokens)    #took the length of this list (no. of words in that line)

        for i in range(tokens_length):
            token = tokens[i]   #taking a single word

            if i == 0:
                first_possible_words[token] = first_possible_words.get(token, 0) + 1 
                #calculating the frequencies of all the first words, eg. {'i': 5, 'how': 4, 'this': 3}
                #get function returns the value zero if the key doesn't exists, otherwise increments it by one
                print(first_possible_words)


            else:
                prev_token = tokens[i - 1]

                if i == tokens_length - 1:
                    add_to_dict(transitions, (prev_token, token), 'END')

                if i == 1:
                    add_to_dict(second_possible_words, prev_token, token)

                else:
                    prev_prev_token = tokens[i - 2]
                    add_to_dict(transitions, (prev_prev_token, prev_token), token)

    first_possible_words_total = sum(first_possible_words.values())

'''
    for key, value in first_possible_words.items():
        first_possible_words[key] = value / first_possible_words_total

    for prev_word, next_word_list in second_possible_words.items():
        second_possible_words[prev_word] = get_next_probability(next_word_list)

    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = get_next_probability(next_word_list)

def next_word(tpl):
    #print(transitions)
    if(type(tpl) == str):   #it is first word of string.. return from second word
        d = second_possible_words.get(tpl)

        if (d is not None):
            return list(d.keys())

    elif(type(tpl) == tuple): #incoming words are combination of two words.. find next word now based on transitions
        d = transitions.get(tpl)

        if(d == None):
            return []
        return list(d.keys())

    return None #wrong input.. return nothing
'''

trainMarkovModel()  #generate first, second words list and transitions

########## demo code below ################

print("This is a n-gram text predictor. Type in anything and you'll get suggestions on which words to use next. \nPress TAB to use the first word (the word with highest probablity), or type in your own word :)\n")