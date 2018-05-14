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
        a.append(corrected)
    message['text'] = ' '.join(a)

    def get_multiple_response(key_list):
        user_keys = set(key_list)
        available_keys = set(user_input.keys())
        selected_keys = user_keys & available_keys
        response_output = list()
        for selected_key in selected_keys:
            retrieved_response = user_input.get(selected_key,'')
            if not retrieved_response:
                continue
            response_output.append(retrieved_response[0])
        if response_output:
            return '\n Also, \n'.join(response_output)
        else:
            return uncorrected + "? I don't know any responses for that. May be you should try something else?"

    import re
    word_selector = re.compile(r'\w+')
    result_message['text'] = get_multiple_response(word_selector.findall(message['text']))
    return result_message
