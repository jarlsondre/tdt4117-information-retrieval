from nltk.stem.porter import PorterStemmer
import random; random.seed(123)
import codecs
import string
import gensim


def print_five_first_paragraphs(paragraphs): 
    """
    Function for printing paragraphs. This is used 
    in order to visualize what changes each transformation
    does :))  
    """
    print("\n--------------------")
    print("Printing the five first paragraphs")
    print("--------------------\n")
    for i in range(5):
        print(paragraphs[i])
    print("--------------------\n")


# TODO: Fill out this with the first part of the main()-function
def preprocessing(document):
    """
    Function for removing punctuation, tokenizing, stemming 
    """

    table = str.maketrans("", "", string.punctuation+"\n\r\t")
    for i in range(len(document)):
        document[i] = document[i].translate(table).lower() # Removing all the punctuation and making the strings lowercase
    
    stemmer = PorterStemmer()
    for i in range(len(document)):
        document[i] = stemmer.stem(document[i])

    return document

def main(): 
    # 1.1 Open file
    f = codecs.open("pg3300.txt", "r", "utf-8")

    # 1.2 Partition file into paragraphs
    paragraphs = f.read().split("\n\n")

    f.close() # Closing the file
    
    # 1.3 Filter out paragraphs containing "Gutenberg"
    for p in paragraphs:
        if "Gutenberg" in p:
            paragraphs.remove(p)


    # Copying the paragraphs so we have them for later
    original_paragraphs = []
    for p in paragraphs:
        original_paragraphs.append(p)
    

    # 1.4 Tokenizing paragraphs (splitting them into words)
    for i in range(len(paragraphs)):
        paragraphs[i] = paragraphs[i].split()


    # 1.5 Removing punctuation
    print(string.punctuation+"\n\r\t")
    table = str.maketrans("", "", string.punctuation+"\n\r\t")
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            paragraphs[i][j] = paragraphs[i][j].translate(table).lower() # Removing all the punctuation and making the strings lowercase
    

    # 1.6 Stemming the words
    stemmer = PorterStemmer()
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            paragraphs[i][j] = stemmer.stem(paragraphs[i][j])


    # 1.7 Frequency of words ??

    # 2 Dictionary Building

    # 2.1 Building a dictionary
    dictionary = gensim.corpora.Dictionary(paragraphs)


    with open("stopwords.txt", "r") as file:
        stopwords = file.read().split(",")
    
    stopword_ids = []
    for word in stopwords:
        if word in dictionary.values():
            stopword_ids.append(dictionary.token2id[word])
    
    dictionary.filter_tokens(stopword_ids)


    # 2.2 Bags of words

    bow_paragraphs = []
    for p in paragraphs:
        bag_of_words = dictionary.doc2bow(p)
        bow_paragraphs.append(bag_of_words)


    # 3 Retrieval Models

    # 3.1 Build TF-IDF Model 
    tfidf_model = gensim.models.TfidfModel(corpus=bow_paragraphs, dictionary=dictionary)

    # 3.2 Map bow into TF-IDF weights

    tfidf_corpus = [tfidf_model[i] for i in bow_paragraphs]

    # 3.3 Construct MatrixSimilary object to calculate similarities

    tfidf_similarity = gensim.similarities.MatrixSimilarity(tfidf_corpus)

    # 3.4 LSI Model

    lsi_model = gensim.models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=100)

    lsi_corpus = [lsi_model[i] for i in bow_paragraphs]

    lsi_similarity = gensim.similarities.MatrixSimilarity(lsi_corpus)

    # 3.5 Report and interpret topics

    print("Showing topics: ")
    topics = lsi_model.show_topics(num_topics=3, formatted=True)
    print(topics)


    # 4 Querying

    # 4.1 Apply all necessary transformation to the query
    
    query = "What is the function of money?".lower()
    query_list = query.split(" ")
    query_transformed = preprocessing(query_list)

    query_bow = dictionary.doc2bow(query_transformed)

    # 4.2 From BOW to TF-IDF

    tfidf_query = tfidf_model[query_bow]

    # 4.3 Report top 3 most relevant paragraphs

    doc2similarity = enumerate(tfidf_similarity[tfidf_query])
    relevant_docs = sorted(doc2similarity, key=lambda kv: -kv[1])[:3] 
    print()
    for doc in relevant_docs:
        print(f"[Paragraph #{doc[0]}]")
        print("\n".join(original_paragraphs[doc[0]].split("\n")[:5]))
        print()
    print(sorted(doc2similarity, key=lambda kv: -kv[1])[:3] )

    # 4.4 Convert from TF-IDF to LSI-topics representation

    lsi_query = lsi_model[tfidf_query]
    print( sorted(lsi_query, key=lambda kv: -abs(kv[1]))[:3] )
    print( lsi_model.show_topics(3) )
    doc2similarity = enumerate(lsi_similarity[lsi_query])
    relevant_docs2 = sorted(doc2similarity, key=lambda kv: -kv[1])[:3]
    for doc in relevant_docs2:
        print(f"[Paragraph #{doc[0]}]")
        print("\n".join(original_paragraphs[doc[0]].split("\n")[:5]))
        print()

    # The different mdoels yield different results. They both retrieve
    # document 1022, but the order is different and the other two results
    # are also different :^)




if __name__ == "__main__":
    main()