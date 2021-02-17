import re
import string


"""
Controller method for tokenizer.py, called to tokenize raw text
Calls each of the other 3 methods in order

@params - text to tokenize as a string, list of stopwords (string)
@return - text tokenized and stemmed, one token per line (string)
"""
def tokenizer(text, stopwords):

    text_tokenized = tokenize(text)
    text_stopwords_removed = remove_stopwords(text_tokenized, stopwords)
    text_stemmed = stem(text_stopwords_removed)

    return text_stemmed


"""
Processes abbreviations in given text, removes other punctuation, and
formats text for further processing

@params - text to be tokenized (string)
@return - text in a tokenized form (string)
"""
def tokenize(text):

    # Handle abbreviations
    abbreviations = re.findall(r"(?:[A-Z]\.)(?:[A-Z]\.)+(?![A-Za-z])", text)

    for i in abbreviations:
        text = text.replace(i, i.replace('.', '').lower(), 1)

    # Replaces all punctuation with whitespace
    for i in string.punctuation:
        text = text.replace(i, " ")

    # Lowercase
    text = text.lower()

    # Gets rid of excess whitespace
    text = re.sub(r'\s+', " ", text)

    # Formats output (one token per line)
    text = text.replace(r"\s", "\n")

    return text


"""
Removes all stopwords from text consistent with provided stopwords

@params - text to parse and list of stopwords (both strings)
@return - text with stopwords removed (string)
"""
def remove_stopwords(text, stopwords):

    # Convert text and stopwords into iterable lists
    text_list = re.split(r"\s", text)
    stopwords_list = re.split(r"\s+", stopwords)

    # Find stopwords and remove from text list
    for i in stopwords_list:
        if i in text_list:
            text_list = list(filter(lambda x: x!=i, text_list))

    # Convert text list back to string form
    new_text = ""

    for i in text_list:
        new_text = new_text + i + '\n'

    return new_text


"""
Implements steps 1a and 1b of Porter stemming in accordance with
the algorithm described in SEIRiP

@params - text to stem (string)
@return - stemmed text (string)
"""
def stem(text):
    
    # Convert text into interable lists
    text_list = re.split(r"\s", text)
    new_list = []

    for token in text_list:

        # Part 1a
        if(token.endswith("sses")):
            token = token.removesuffix("es")
        elif(token.endswith("ied") or token.endswith("ies")):
            token = token[:-3]
            if(len(token) > 1):
                token = token + 'i'
            else:
                token = token + 'ie'

        elif(token.endswith("us") or token.endswith("ss")):
            pass
        elif(token.endswith("s") and contains_vowel(token)):
            token = token.removesuffix('s')

        # Part 1b
        if(token.endswith('eedly')):
            if(part1ba(token, 'eedly')):
                token = token.removesuffix('dly')
        elif(token.endswith('eed')):
            if(part1ba(token, 'eed')):
                token = token.removesuffix('d')
                
        elif(token.endswith('ingly')):
            token = part1bb(token, 'ingly')
        elif(token.endswith('edly')):
            token = part1bb(token, 'edly')
        elif(token.endswith('ing')):
            token = part1bb(token, 'ing')
        elif(token.endswith('ed')):
            token = part1bb(token, 'ed')
        


        new_list.append(token)

    # Convert text list back to string form
    new_text = ""

    for i in new_list:
        new_text = new_text + i + '\n'

    return new_text



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HERE BE HELPER METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
Checks for vowel in token before last 2 characters. Specifically, if token satisfies
requirements to remove 's' suffix in step 1a of Porter stemming

@params - token (string)
@return - bool
"""
def contains_vowel(token):

    for char in token[:-2]:
        if is_vowel(char):
            return True
    return False


"""
Pretty self explantory
"""
def is_vowel(char):
    vowels = ['a', 'e', 'i', 'o', 'u']
    return char in vowels


"""
Determines if a token matches the requirements for the first part of step 1b, 
aka if it is part of the word after the first non vowel following a vowel

@params - token to judge (string), suffix to ignore in search (string)
@return - bool
"""
def part1ba(token, suffix):
    word = token.removesuffix(suffix)
    if re.search("([aeiou][^aeiou])", word) is not None:
        token = token.removesuffix(suffix)
        return True
    else:
        return False


"""
Algorithm for the second half of porter stemming step 1b

@params - token to check, sufffix (both string)
@return - processed token
"""
def part1bb(token, suffix):
    if contains_vowel_true(token, suffix):
        token = token.removesuffix(suffix)
        if add_e_1(token):
            token = token + 'e'
        elif double_letter(token):
            if remove_letter(token):
                token = token[:-1]
        elif len(token) <= 4:
            token = token + 'e'
    return token


"""
Checks if word contains vowel to satisfy the first part of the second
part of Porter stemming step 1b 

@params - token to judge (string), suffix to ignore in search (string)
@return - bool
"""
def contains_vowel_true(token, suffix):
    word = token.removesuffix(suffix)

    for char in word:
        if is_vowel(char):
            return True
    return False


"""
Second check of second part of step 1b: add e for certain endings
"""
def add_e_1(token):
    matches = ['at', 'bl', 'iz']
    return token[-2:] in matches
    
    
"""
Helper method for part1bb, checks if the last 2 letters of string are equal
"""
def double_letter(token):
    return token[-1] == token[-2]


"""
Helper method for part1bb, removes double letters except in certain cases
"""
def remove_letter(token):
    acceptable_letter = ['l', 's', 'z']

    if token [-1] not in acceptable_letter:
        return True
    else:
        return False


"""
Originally used for removing stopwords to fix iterating problems,
removed because it was slow as molasses in winter
Kept in for historical purposes

def remove_all(word, list_in):
    while word in list_in:
        list_in.remove(word)
"""