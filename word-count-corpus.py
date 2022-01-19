"""
    Description: This program reads in a text file, stores the word counts to a
    CSV file, and then integrates that data into a larger word count corpus.
    Author: Matthew Erdman
    Date: 1/9/21
"""
from string import punctuation
import csv

def binarySearch(x, L):
    """
    Purpose: Perform a binary search to find a specified value in a list.
    Parameters: x - the value to look for, and L - the list to look in.
    Return Value: Boolean indicating if x is in L and the integer index of x.
    """
    low = 0
    high = len(L) - 1

    while low <= high:
        mid = (low + high) // 2

        if x == L[mid]:       # found x in L
            return True, mid

        elif x > L[mid]:      # too low, adjust low bound
            low = mid + 1

        elif x < L[mid]:      # too high, adjust high bound
            high = mid - 1

    return False, -1              # x is not in L


def mergeSort(L):
    """
    Purpose: Use a merge sort algorithm to sort a list of lists.
    Parameters: The list to be sorted.
    Return Value: A sorted list of lists, ordered alphabetically from the first item.
    """
    if len(L) > 1:
        mid = len(L)//2
        l = L[:mid]
        r = L[mid:]
        mergeSort(l)
        mergeSort(r)

        b = 0
        c = 0
        d = 0
        while b < len(l) and c < len(r):
            if l[b] < r[c]:
                L[d] = l[b]
                b += 1
            else:
                L[d] = r[c]
                c += 1
            d += 1

        while b < len(l):
            L[d] = l[b]
            b += 1
            d += 1

        while c < len(r):
            L[d] = r[c]
            c += 1
            d += 1


def readDictionary(filename):
    """ open wordCounts dictionary, read words into a list, return list """
    words = []
    dictionary = open(filename, 'r')
    for line in dictionary:
        words.append(line.split(",")[0])
    dictionary.close()
    return words


def readFile(filename):
    """ open given filename, read in text, split into words, return list of words """
    words = []
    infile = open(filename, 'r')
    for line in infile:
        lineList = line.strip().split(" ")
        for word in lineList:
            word = word.strip(punctuation).lower()
            if word.isalpha():
                words.append(word)
    infile.close()
    return words


def writeFile(filename, wordCounts):
    """ open given filename, output word and count as CSV """
    outfile = open(filename, "w")
    for word in wordCounts:
        outfile.write(word[0] + ',' + str(word[1]) + "\n")
    outfile.close()


def wordCount(words, dictionary):
    """
    Purpose: Create a set of word count data from a list of words.
    Parameters: The list of words to be counted and a dictionary of acceptable words.
    Return Value: A list of lists containing words and their counts.
    """
    wordCounts = []
    for word in words:
        # print(str(len(wordCounts)) + "/16087: " + str(len(wordCounts)*100//16087) + "%", end="\r")
        if binarySearch(word[0], dictionary):
            FOUND = False
            for i in range(len(wordCounts)):
                if word == wordCounts[i][0]:
                    wordCounts[i][1] += 1
                    FOUND = True
            if not FOUND:
                wordCounts.append([word, 1])

    return wordCounts

def updateCorpus(fnameCorpus, fnameMobyWords, dictionary):
    """
    Purpose: Merge Moby Dick word counts with corpus and rewrite corpus file.
    Parameters: The filename of the corpus and the Moby Dick word counts.
    Return Value: None.
    """
    corpus = open(fnameCorpus, 'r')
    corpusWordCounts = []
    for line in corpus:
        corpusWordCounts.append([line.split(',')[0], int(line.split(',')[1].strip())])
    corpus.close()

    moby = open(fnameMobyWords, 'r')
    corpusIndex = 0
    for mobyWord in moby:
        FOUND, index = binarySearch(mobyWord.split(',')[0], dictionary)
        if FOUND:
            while mobyWord.split(',')[0] != corpusWordCounts[corpusIndex][0]:
                corpusIndex += 1
            corpusWordCounts[corpusIndex][1] += int(mobyWord.split(',')[1])
            corpusIndex += 1
    moby.close()

    writeFile(fnameCorpus, corpusWordCounts)


def main():
    dictionary = readDictionary("wordCounts.txt")
    words = readFile("moby-dick.txt")
    print("counting...")
    wordCounts = wordCount(words, dictionary)
    print("sorting...")
    mergeSort(wordCounts)
    writeFile("word-count-moby.txt", wordCounts)
    # with open("word-count-moby.txt", 'r') as i:
    #     wordCounts = []
    #     for row in csv.reader(i): wordCounts.append(row)
    print("updating...")
    updateCorpus("wordCounts.txt", "word-count-moby.txt", dictionary)


main()
