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

    f.close() # Closing the file
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


    with open("stopwords.txt", "r") as file:
        stopwords = file.read().split(",")
    
    print(stopwords)
    stopword_ids = []
    for word in stopwords:
        if word in dictionary.values():
            stopword_ids.append(dictionary.token2id[word])
    
    print(stopword_ids)
    dictionary.filter_tokens(stopword_ids)

    print(dictionary)

    # 2.2 Bags of words

    bow_paragraphs = []
    for p in paragraphs:
        bag_of_words = dictionary.doc2bow(p)
        bow_paragraphs.append(bag_of_words)

    print(bow_paragraphs[0], bow_paragraphs[1])

    # 3 Retrieval Models

    # 3.1 Build TF-IDF Model 
    tfidf_model = gensim.models.TfidfModel(corpus=bow_paragraphs, dictionary=dictionary)
    print(tfidf_model)

    # 3.2 Map bow into TF-IDF weights

    tfidf_corpus = [tfidf_model[i] for i in bow_paragraphs]
    print(tfidf_corpus[0])
    print(tfidf_corpus[1])

    # 3.3 Construct MatrixSimilary object to calculate similarities

    similarity = gensim.similarities.MatrixSimilarity(tfidf_corpus)

    print(similarity)










if __name__ == "__main__":
    main()