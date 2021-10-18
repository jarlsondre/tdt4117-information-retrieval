from nltk.stem.porter import PorterStemmer
import random; random.seed(123)
import codecs
import string
import gensim


def print_five_first_paragraphs(paragraphs): 
    print("\n--------------------")
    print("Printing the five first paragraphs")
    print("--------------------\n")
    for i in range(5):
        print(paragraphs[i])
    print("--------------------\n")

def main(): 
    # 1.1 Open file
    f = codecs.open("pg3300.txt", "r", "utf-8")

    # 1.2 Partition file into paragraphs
    paragraphs = f.read().split("\n\n")

    print(f"length is {len(paragraphs)}")
    
    # 1.3 Filter out paragraphs containing "Gutenberg"
    for p in paragraphs:
        if "Gutenberg" in p:
            paragraphs.remove(p)

    print(f"length is {len(paragraphs)}") # Seeing that the length changes after removal

    # Copying the paragraphs so we have them for later
    original_paragraphs = []
    for p in paragraphs:
        original_paragraphs.append(p)
    
    print_five_first_paragraphs(paragraphs)

    # 1.4 Tokenizing paragraphs (splitting them into words)
    for i in range(len(paragraphs)):
        paragraphs[i] = paragraphs[i].split()

    print_five_first_paragraphs(paragraphs)

    # 1.5 Removing punctuation
    print(string.punctuation+"\n\r\t")
    table = str.maketrans("", "", string.punctuation+"\n\r\t")
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            paragraphs[i][j] = paragraphs[i][j].translate(table).lower() # Removing all the punctuation and making the strings lowercase
    
    print_five_first_paragraphs(paragraphs)

    # 1.6 Stemming the words
    stemmer = PorterStemmer()
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            paragraphs[i][j] = stemmer.stem(paragraphs[i][j])

    print_five_first_paragraphs(paragraphs)

    # 1.7 Frequency of words ??

    # 2 Dictionary Building

    # 2.1 Building a dictionary
    dictionary = gensim.corpora.Dictionary(paragraphs)
    print(dictionary)




if __name__ == "__main__":
    main()