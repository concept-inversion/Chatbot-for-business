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
from .faq_db import set_all_keys
from .lemmatizer import lemmatize_word
from .lemmatizer import select_noun_verbs
from .lemmatizer import fuzzymatcher
from .optimizedsimilarity import similarity
from .faq_db import get_answer_from_database
import sqlite3
from .faq_db import conn, cur

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
    # User Input Spelling Correction Completed

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
        user_input = user_query
        # Processing Spell Corrected User Input
        result = test_response(user_input)
        if result is None:
            return uncorrected + "? I don't know any responses for that. May be you should email to info@merojob.com"
        return result

    def pos_similarity(user_input):
        user_input_corrected = ' '.join(correction(word) for word in user_input)
        user_input_to_list_after_pos_reduction = select_noun_verbs(user_input_corrected, list_only=True)
        user_input_to_lemma_after_pos_reduction = [lemmatize_word(word) for word in user_input_to_list_after_pos_reduction]
        user_input_to_statement = ' '.join(user_input_to_lemma_after_pos_reduction)
        all_database_questions_non_pos = set_all_keys()
        # the recieved format is [(question,),...]
        all_database_questions_after_pos = list((select_noun_verbs(line[0], list_only=True),line[1]) for line in all_database_questions_non_pos)
        all_database_questions_after_lemma = list()        
        for line in all_database_questions_after_pos:
            lemmatized = ' '.join([lemmatize_word(word) for word in line[0]])
            all_database_questions_after_lemma.append((lemmatized,line[1]))
        que_value = list()
        for each_question in all_database_questions_after_lemma:
            jquestion = each_question[0]
            fuzz_value = fuzzymatcher(user_input_to_statement,jquestion, partial=False)
            que_value.append((fuzz_value,jquestion,each_question[1]))
        # import ipdb; ipdb.set_trace()
        t_list = sorted(que_value, reverse=True)[:5]
        similarity_list = list()
        for each_question in t_list:
            _, quest, question_id = each_question
            similarity_value = similarity(quest, user_input_to_statement, True)
            data = (similarity_value, quest, question_id)
            similarity_list.append(data)
        similarity_value, _ , selected_id = max(similarity_list)
        print(similarity_list)
        answer_fetched = get_answer_from_database('',id=selected_id)
        if similarity_value < 0.65:
            print('Did not respond as {} for {} due to {} sim value'.format(answer_fetched, ' '.join(user_input), similarity_value))
            failed_query = ' '.join(user_input)
            # print(failed_query)
            cur.execute("INSERT INTO log(user_query) values('{}')".format(failed_query))
            conn.commit()
            return "I dont know about that. Our representatives will let you know."
        return answer_fetched
        # print('>>>{}\n>{}'.format(user_input, answer_fetched))
    
    import re
    word_selector = re.compile(r'\w+')
    result_message['text'] = pos_similarity(word_selector.findall(message['text']))
    # result_message['text'] = get_multiple_response(word_selector.findall(message['text']))
    # result_message['text'] = check_similarity(' '.join(word_selector.findall(uncorrected)))
    return result_message


def show_user_queries(request):
    context_data = dbLogger.fetch_data()
    return HttpResponse(json.dumps(context_data))


class LogView(ListView):
    model = UserQuery
    context_object_name = 'context_data'
    template_name = 'chatbot_tutorial/display.html'

def insert(id, response):
    que = cur.execute("SELECT distinct user_query from log where id={}".format(id)).fetchone()[0]
    stmt = "INSERT INTO que2(question, answer, category) values('{}','{}','{}')".format(que, response, 'userDefined')
    # print(stmt)
    cur.execute(stmt)
    conn.commit()

def editable_dashboard(request):
    if request.method == 'POST':
        id = request.POST['update_id']
        response = request.POST['update_query']
        insert(id, response)
    user_log = list()
    statement = "SELECT * FROM log"
    cur.execute(statement)
    headers = [desc[0] for desc in cur.description]
    for row in cur:
        user_log.append(dict(zip(headers, row)))
    # all_failed_responses = dbLogger.fetch_data()
    return render(request, 'chatbot_tutorial/editable_dashboard.html', {'lists': user_log})

