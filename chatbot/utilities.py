# This data will be handled from scrapped inputs
registration = "Registration is easy. Just sign up for a new account by filling in the form completely with your full name, a valid email id, mobile number, preferred job category and password. Click “Create my Account” and look for an email from us confirming your registration. Click the link in the email and you are now registered with merojob. You can also sign up with Facebook and twitter."
u_password = "Username is a valid email id and Password is the set of characters which provides access to an account. The username and password are your login credential to your meroJob.com resume account. With the username/ password, you can login to your profile/ Account for managing your resume as well as to apply any job circulation."
# compile documents
doc_complete = [u_password]

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)

jumbled_list = ldamodel.print_topics(num_topics=3, num_words=5)

import re


def filter_weights(pre_result, confidence, key_only=False):
    selected_data = list()
    # Received Data Format
    # [topic]: topic=> {word:value}: word=>keyword as topics, value=>relevancy of keyword as topic
    for topic in pre_result:
        dix = dict()
        for word, its_value in topic.items():
            if its_value >= confidence:
                dix[word] = its_value
        if dix:
            selected_data.append(dix)
    return [topic.keys() for topic in selected_data] if key_only else selected_data


def get_weights(stub_data):
    all_data = list()
    word_value_finder = re.compile(r'(\d\.\d+)\*\"(\w+)')
    for row_data in stub_data:
        dic = dict()
        values = re.findall(word_value_finder, row_data[1])
        for value, key in values:
            dic[key] = float(value)
        all_data.append(dic)
    return all_data

unstructured = get_weights(jumbled_list)
list_to_synonym = filter_weights(unstructured, 0.065, key_only=True)
# print(structured[0])

from nltk.corpus import wordnet as wn
import itertools
# list_to_synonym = [['email', 'click', 'registration']]
collect = []
for each in list_to_synonym[0]:
    a=[]
    for synset in wn.synsets(each):
        for lemma in synset.lemmas():
            a.append(lemma.name())
    new_li = []
    for i in range(len(a)):
        new_li.append(a[i])
    collect.append(new_li)
list(itertools.chain.from_iterable([[1,2,3], [2,5,8]]))
no_filter_list = list(itertools.chain.from_iterable(collect))
filter_list = list(set(no_filter_list))
dict_key_tuple = tuple(filter_list)
