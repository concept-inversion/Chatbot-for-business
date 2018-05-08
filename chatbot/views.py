import nltk
from django.shortcuts import render

from .faq_data import user_input
from .spelling import correction, synonym_r, synonym_m, synonym_p


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):

    result_message = {
        'type': 'text'
    }

    # Applying spelling correction using Bayes Theorem
    uncorrected = message['text']
    tokens = nltk.word_tokenize(message['text'])
    a = []
    for each in tokens:
        corrected = correction(str(each))
        print(corrected)
        a.append(corrected)
    message['text'] = ' '.join(a)

    # Some "Hot keywords" based on user data

    # Test synonyms

    # from nltk.corpus import wordnet as wn
    # a = []
    # for synset in wn.synsets('register'):
    #     for lemma in synset.lemmas():
    #         a.append(lemma.name())
    # for i in range(len(a)):
    #     print(a[i])

    if synonym_r[0] in message['text'] or synonym_r[1] in message['text']:
        result_message['text'] = user_input['register']

    elif synonym_m[0] in message['text'] or synonym_m[1] in message['text']:
        result_message['text'] = user_input['merojob']

    elif synonym_p[0] in message['text']:
        result_message['text'] = user_input['password']

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! Ask stuff about Merojob."
    else:
        result_message['text'] = uncorrected + "? I don't know any responses for that. May be you should try " \
                                                   "something else?"

    return result_message
    