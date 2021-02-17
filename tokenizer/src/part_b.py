import sys
import io
import tokenizer
import re
# import matplotlib.pyplot as plt


"""
@author Sam Benet, 2021

Main method controlling tokenizer

@params - filepath of text file to tokenize (strings)
@return - No return but writes tokenized input text to specified file
"""
def main():

    # Take command line arguments and check for 2 args
    args = sys.argv[1:]

    if(len(args) == 1):
        file_in = args[0]
    else:
        print("Invalid arguments")
        exit(-1)

    stopwords_fp = "../text/stopwords.txt"
    file_in = args[0]
    file_out = 'terms.txt'

    # Read text from input file to string
    input_file = open(file_in, 'r')
    stopwords_file = open(stopwords_fp, 'r')
    text = ''
    stopwords = ''

    for line in input_file:
        text = text + line

    for line in stopwords_file:
        stopwords = stopwords + line

    # Tokenize string
    tokenized_text = tokenizer.tokenizer(text, stopwords)

    # Generate and write list of top 200 most frequent terms
    top_200(tokenized_text, file_out)
    vocabulary_growth(tokenized_text)




"""
Generates a list of the 200 most frequent token in the input text
Token space padded by 20, longest token in moby dick list determined
to be 18. Can be changed for use in other texts

@params - text, filepath to output to (both string)
@return - no return, prints list to file specified
"""
def top_200(text, fp):

    text_list = re.split(r"\s", text)
    freq_dic = {}
    
    # Generate frequency dictionary
    for token in text_list:
      if(freq_dic.get(token) == None):
        freq_dic[token] = 1
      else:
        freq_dic[token] = freq_dic.get(token)+1

    values = freq_dic.items()
    sorted_list = sorted(values, key=lambda freq: freq[1], reverse=True)

    top_200 = sorted_list[:200]
    # Convert unsorted dictionary to 
    terms_file = open(fp, 'w')
    for key in top_200:
        terms_file.write(f"{key[0]:<20}{key[1]:>4}\n")
        pass
        
"""
Generates a graph of vocabulary growth throughout the supplied text
Uses matplotlib pyplot

@params - text to graph vocab growth of
@return - nonne but generates graph

def vocabulary_growth(tokenized_text):

    text_list = re.split(r"\s", tokenized_text)

    # Arrays containing data to be graphed
    word_count = []
    unique_count = []

    # Set of unique words
    word_set = set(())

    #Compute data
    for i in range(len(text_list)):
        word_count.append(i)
        word_set.add(text_list[i])
        unique_count.append(len(word_set))

    # Plot data on graph
    plt.plot(word_count, unique_count)
    plt.xlabel('Words in collection')
    plt.ylabel('Words in vocabulary')
    plt.title('Moby Dick Vocabulary Growth')
    plt.show()
"""


if __name__ == '__main__':
    main()
    
    