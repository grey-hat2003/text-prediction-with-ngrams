import random 
from collections import Counter 
  
# This function calulates the freq of the (i+1)th 
# word in the whole corpus, where i is the index of 
# the sentence or the word. 
  
def next_word_freq(array, sentence): 
      
    sen_len, word_list = len(sentence.split()), [] 
      
    for i in range(len(array)):         
        if ' '.join(array[i : i + sen_len]).lower() == sentence.lower(): 
            if i + sen_len < len(array) - 1: 
                word_list.append(array[i + sen_len]) 

    return dict(Counter(word_list)) 
  
def CDF(d): 
      
    prob_sum, sum_vals = 0, sum(d.values()) 
      
    for k, v in d.items(): 
        pmf = v / sum_vals 
        prob_sum += pmf 
        d[k] = prob_sum

    return d 
  
def main(sent, x, n): 
    corpus = open('TheHindu_PerservanceReport copy.txt','r').read() 
      
    l = corpus.split() 
      
    temp_out = '' 
    out = sent + ' '
      
    for i in range(n - x):
          
        func_out = next_word_freq(l, sent) 
        cdf_dict = CDF(func_out) 
        rand = random.uniform(0, 1) 
          
        try: 
            key, val = zip(*cdf_dict.items()) 
        except: 
            break
          
        for j in range(len(val)): 
            if rand <= val[j]: 
                pos = j 
                break
                      
        temp_out = key[pos] 
        out = out + temp_out + ' '
        sent = temp_out 
          
    print(out, end = '\n\n') 
  
if __name__ == '__main__': 
    
    inp_sent = input("Enter a word: ")
    main(inp_sent, len(inp_sent), 5) 