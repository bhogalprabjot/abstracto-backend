from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.cluster import KMeans
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.mixture import GaussianMixture
import pickle
import numpy as np
import math
"""
Split into sentences
Remove stop words and lemmatize and to lower
"""


def preprocessing(article):
    processedSentences = []
    sentences = []
    # nlp = spacy.load('en_core_web_lg')  # ~700mb
    nlp = spacy.load('en_core_web_sm')  # ~40+ mb
    doc = nlp(article)
    sen = [sent.text.strip() for sent in doc.sents]
    sentences = []

    # TODO: improve this code to clean sentences
    for line in sen:
        if line != '':
            sentences.append(line)

    # print(type(sentences))
    stopwords = nlp.Defaults.stop_words

    for sentence in sentences:
        # print(type(sentence))
        doc = nlp(sentence)
        reqtokens = []

        for token in doc:
            if token.text not in stopwords:
                # print(token.text,token.lemma_)          
                if token.lemma_ != '-PRON-':
                    reqtokens.append(token.lemma_)
            else:
                reqtokens.append(token.lower_)
        processedSentences.append(' '.join(reqtokens))
    # print(processedSentences)
    return processedSentences, sentences


"""
TF-IDF 

OUTPUT: 
Sparse matrix of (n_samples, n_features) 
Tf-idf-weighted document-term matrix.

Assume general form: (A,B) C
A: Document index B: Specific word-vector index in its vocab C: TFIDF score for word B in document A
This is a sparse matrix. It indicates the tfidf score for all non-zero values in the word vector for each document.
"""


def tfIdf(processedSentences):
    # create tfidf matrix from the processed sentences
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processedSentences)
    # print(tfidf_matrix)
    return tfidf_matrix


"""
Apply K Means Clustering
"""


def GMM(tfidf_matrix, cluster_count):
    Cluster = GaussianMixture(n_components = cluster_count)
    Cluster.fit(tfidf_matrix.toarray())
    clusters = Cluster.predict(tfidf_matrix.toarray())
    # kMeansCluster = KMeans(n_clusters=cluster_count)
    # kMeansCluster.fit(tfidf_matrix)
    # clusters = kMeansCluster.labels_.tolist()
    # print(clusters)
    return clusters


""" 
Create new dictionary that tracks which cluster each sentence belongs to keeps copy of original sentences and stemmed sentences 
sentenceDictionary { idx: { text: String, lemmetized: String, cluster: Number } }
"""


def sentenceDict(sentences, clusters, processedSentences):
    sentenceDictionary = {}
    for idx, sentence in enumerate(sentences):
        sentenceDictionary[idx] = {}
        sentenceDictionary[idx]['text'] = sentence
        sentenceDictionary[idx]['cluster'] = clusters[idx]
        sentenceDictionary[idx]['lemmetized'] = processedSentences[idx]
    # print(sentenceDictionary)
    return sentenceDictionary


"""
Create new dictionary that contains 1 entry for each cluster each key in dictionary will point to array of sentences, all of which belong to that cluster, 
we attach the index to the sentenceDictionary object so we can recall the original sentence
"""


def clusterDict(sentenceDictionary):
    clusterDictionary = {}
    for key, sentence in sentenceDictionary.items():
        if sentence['cluster'] not in clusterDictionary:
            clusterDictionary[sentence['cluster']] = []
        clusterDictionary[sentence['cluster']].append(sentence['lemmetized'])
        sentence['idx'] = len(clusterDictionary[sentence['cluster']]) - 1
    # print(clusterDictionary)
    return clusterDictionary


"""
####################################
# Calculate Cosine Similarity Scores
####################################		

# For each cluster of sentences,
# Find the sentence with highet cosine similarity over all sentences in cluster
"""


def calCosineSim(clusterDictionary):
    vectorizer = TfidfVectorizer()
    maxCosineScores = {}
    for key, clusterSentences in clusterDictionary.items():
        maxCosineScores[key] = {}
        maxCosineScores[key]['score'] = 0
        tfidf_matrix = vectorizer.fit_transform(clusterSentences)
        cos_sim_matrix = cosine_similarity(tfidf_matrix)
        # print(cos_sim_matrix)
        for idx, row in enumerate(cos_sim_matrix):
            sum = 0
            for col in row:
                sum += col
            if sum > maxCosineScores[key]['score']:
                maxCosineScores[key]['score'] = sum
                maxCosineScores[key]['idx'] = idx
    # print("Max Cosine Score {}".format(maxCosineScores))
    return maxCosineScores


"""
Construct Document Summary

for every cluster's max cosine score,
find the corresponding original sentence

"""


def constructResult(maxCosineScores, clusterDictionary, sentenceDictionary, sentences):
    resultIndices = []
    i = 0

    for key, value in maxCosineScores.items():
        cluster = key
        idx = value['idx']
        stemmedSentence = clusterDictionary[cluster][idx]
        # key corresponds to the sentences index of the original document
        # we will use this key to sort our results in order of original document
        for key, value in sentenceDictionary.items():
            if value['cluster'] == cluster and value['idx'] == idx:
                resultIndices.append(key)

    resultIndices.sort()
    # print(resultIndices)
    # Iterate over sentences and construct summary output
    result = ''
    for idx in resultIndices:
        result += sentences[idx] + ' '
    return result


# def main():
def summarizer(article):
    # f = open("001.txt", "r")
    # article = f.read()

    processedSentences, sentences = preprocessing(article)
    # print("\n", processedSentences) 
    # print("\n", sentences) 

    tfidf_matrix = tfIdf(processedSentences)

    model = pickle.load(open('Summarizer/model.pkl', 'rb'))
    arr = np.array([len(sentences)])
    arr_2d = np.reshape(arr, (-1,1))
    k = model.predict(arr_2d)
    k1= math.floor(k[0])
    clusters = GMM(tfidf_matrix, k1)

    sentenceDictionary = sentenceDict(sentences, clusters, processedSentences)
    # print("\nsentence dictionary \n{}".format(sentenceDictionary))

    clusterDictionary = clusterDict(sentenceDictionary)
    # print("\nCluster dictionary \n{}".format(clusterDictionary))
    maxCosineScores = calCosineSim(clusterDictionary)

    result = constructResult(maxCosineScores, clusterDictionary, sentenceDictionary, sentences)
    # print("\n\nThe resulting summary is: \n")
    # print(result)
    return result

# if __name__ == '__main__':
#     main()
