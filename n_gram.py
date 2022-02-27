import json, os
import emoji

gender_emoji = ["♂","♀"] #Preparing predicate lists so we don't consider Dark Skin Person a bigram of Dark Skin and Person
skin_emoji = ["🏻",
             "🏼",
             "🏽",
             "🏾",
             "🏿"]

def emoji_n_gram(string:str):
    '''
    param: string
    returns: list of emoji n-grams of that string
    
    Checks each character in the string, if it is in the emoji hashmap check if it is a gender or skim tone modifier, if it's not add it to the n_gram string else skip it. If the character is not in the emoji hashmap, append the n_gram string to the list of n_grams, reset the string to blank. When all characters have been checked, return the n_gram list
    '''
    n_gram = ""
    used_emoji = []
    temp = []
    for character in string:
        if character in emoji.UNICODE_EMOJI['en']:
            if character not in gender_emoji and character not in skin_emoji:
                n_gram+=character
                temp.append(character)
        else:
            if len(n_gram) > 1:
                temp.sort()
                used_emoji.append(temp)
                temp = []
            n_gram=""

    if len(n_gram) > 1:
        temp.sort()
        used_emoji.append(temp)

    return used_emoji


#emoji_repeating_n_gram_counter("▶▶▶")
n_grams = {}
master_gram = {2:{},
               3:{},
               4:{},
               5:{},
               6:{}}

#List of files in given directory
files = []
for x in os.listdir(os.getcwd()+"\\Archive\\Emoji"):
    files.append(os.getcwd()+"\\Archive\\Emoji\\{0}".format(x))

'''
For each file, check each string, get the list of n_grams from the string, add it to the dictionary of n_grams based on it's length.
'''
for file in files:
    with open(file) as jsonf:
        data = json.load(jsonf)
        for x in data:
            n_gram_list = emoji_n_gram(x)
            for grams in n_gram_list:
                gram_key = "".join(grams)
                if len(gram_key) in master_gram:
                    gram_dict = master_gram[len(gram_key)]
                    if gram_key not in gram_dict:
                        gram_dict[gram_key]=1
                    else:
                        gram_dict[gram_key]+=1
                    master_gram[len(gram_key)] = gram_dict


#Sorting the n-gram lists by their occurences for each length
for under_gram in master_gram:
    sorted_n_grames = sorted(master_gram[under_gram].values())
    sorted_dict = {}
    sorted_keys = sorted(master_gram[under_gram], key=master_gram[under_gram].get,reverse=False)  # [1, 3, 2]
    for w in sorted_keys:
        if master_gram[under_gram][w]>40:
            sorted_dict[w] = master_gram[under_gram][w]
print(master_gram)
'''
Variation of the N gram for only repeating
def emoji_repeating_n_gram_counter(string:str):
    temp=""
    count=1
    for character in string:
        if character in emoji.UNICODE_EMOJI['en']:
            if temp==character:
                count+=1
            else:
                print(temp)
                print(count)
                count=1
                temp=character
    print(temp)
    print(count)'''