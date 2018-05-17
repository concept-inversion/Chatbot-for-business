import json
from django.http import HttpResponse
import nltk
import datetime
import logging
from django.shortcuts import render
from .faq_data import user_input
from .spelling import correction
from .pylog import LogQuery
from django.views .generic import ListView
from .models import UserQuery
from .faq_db import test_response

# FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(filename='logs/response.log', level=logging.ERROR, format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')

dbLogger = LogQuery()


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
    user_query = ' '.join(a)

    def get_multiple_response(key_list):
        user_keys = set(key_list)
        available_keys = set(user_input.keys())
        selected_keys = user_keys & available_keys
        response_output = list()
        for selected_key in selected_keys:
            retrieved_response = user_input.get(selected_key, '')
            if not retrieved_response:
                continue
            response_output.append(retrieved_response[0])
        if response_output:
            return '\n Also, \n'.join(response_output)
        else:
            #
            # logging.error(uncorrected)
            # md = UserQuery()
            # md.username = 'Anonymous'
            # md.query = uncorrected
            # md.timestamp = str(datetime.datetime.now())
            # md.save()
            # dbLogger.insert_data(uncorrected)
            return uncorrected + "? I don't know any responses for that. May be you should email to info@merojob.com"

    def check_similarity(user_input):
        token_word = nltk.word_tokenize(user_input)
        user_input = " ".join([correction(word) for word in token_word])
        print(user_input)
        result = test_response(user_input)
        if result is None:
            return uncorrected + "? I don't know any responses for that. May be you should email to info@merojob.com"
        return result

    import re
    word_selector = re.compile(r'\w+')
    # result_message['text'] = get_multiple_response(word_selector.findall(message['text']))
    result_message['text'] = check_similarity(' '.join(word_selector.findall(uncorrected)))
    return result_message


def show_user_queries(request):
    context_data = dbLogger.fetch_data()
    return HttpResponse(json.dumps(context_data))


class LogView(ListView):
    model = UserQuery
    context_object_name = 'context_data'
    template_name = 'chatbot_tutorial/display.html'


def editable_dashboard(request):
    all_failed_responses = dbLogger.fetch_data()
    return render(request, 'chatbot_tutorial/editable_dashboard.html', {'lists': all_failed_responses})

