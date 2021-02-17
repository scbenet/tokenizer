import sys
import io
import tokenizer

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
    file_out = 'tokenized.txt'

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

    # Output tokenized text to file_out
    output_file = open(file_out, 'w')
    for line in tokenized_text:
        output_file.write(line)


if __name__ == '__main__':
    main()
    
    