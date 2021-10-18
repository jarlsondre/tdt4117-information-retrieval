
import random; random.seed(123)
import codecs
import string


def main(): 
    f = codecs.open("pg3300.txt", "r", "utf-8")

    # 1.2
    paragraphs = f.read().split("\n\n")

    print(f"length is {len(paragraphs)}")
    
    # 1.3
    for p in paragraphs:
        if "Gutenberg" in p:
            paragraphs.remove(p)

    print(f"length is {len(paragraphs)}") # Seeing that the length changes after removal


    # 1.4
    for i in range(len(paragraphs)):
        paragraphs[i] = paragraphs[i].split()

    print(f"first paragraph is {paragraphs[0]}")

    # 1.5
    print(string.punctuation+"\n\r\t")
    table = str.maketrans("", "", string.punctuation+"\n\r\t")
    for i in range(len(paragraphs)):
        for j in range(len(paragraphs[i])):
            paragraphs[i][j] = paragraphs[i][j].translate(table).lower() # Removing all the punctuation and making the strings lowercase
    
    print(f"first paragraph is {paragraphs[0]}")


if __name__ == "__main__":
    main()