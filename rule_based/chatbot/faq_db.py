"""
    generate_stem_statement(stmt)
    get_highest_matching_key(user_query)

"""
import shelve
import sqlite3
import nltk
from nltk.stem.snowball import SnowballStemmer
from .similarity import similarity
from .pylog import LogQuery

# Database Connection
conn = sqlite3.connect('db.faq', check_same_thread=False)
cur = conn.cursor()

# Word Stemmer
stemmer = SnowballStemmer('english')


# Call if no data in db
def pre_populate():
    # Define shelve data as js=> Jobseeker em=> Employer
    js = shelve.open('chatbot/jobseeker.shelve')
    em = shelve.open('chatbot/employer.shelve')

    # Insert Jobseeker Data
    for q, s in js.items():
        insert_data(q, s, 'Jobseeker')

    # Insert Employer Data
    for q, s in em.items():
        insert_data(q, s, 'Employer')

# Interact with the database
cur.execute("CREATE TABLE IF NOT EXISTS question(question varchar(255), answer varchar (255), category varchar (100))")

lg = LogQuery()
key_result = None

def create_user_log(user_query, probable_question, attempted_response, semantic_similarity):
    lg.insert_data(user_query, probable_question, attempted_response, semantic_similarity)


def generate_stem_statement(stmt):
    corpora = nltk.word_tokenize(stmt)
    return ' '.join([stemmer.stem(word) for word in corpora])

def hybrid_matcher(user_query):
    pass

def test_response(user_query):
    true_score = get_highest_matching_key(user_query)
    if not true_score:
        return None
    semantic_similarity, probable_question = max(true_score)
    attempted_response = get_answer_from_database(probable_question)
    if semantic_similarity > 0.5:
        return attempted_response
    create_user_log(user_query, probable_question, attempted_response, semantic_similarity)
    return None


def set_all_keys():
    global key_result
    key_result = cur.execute("select DISTINCT question,id from que2").fetchall()
    return key_result


def get_highest_matching_key(user_query):
    set_all_keys()
    if not key_result:
        pre_populate()
        set_all_keys()
    keys_only = [row[0] for row in key_result]
    true_score = [(similarity(generate_stem_statement(user_query), generate_stem_statement(key), True), key)
                  for key in keys_only]
    return true_score


def get_answer_from_database(selected_question,id=None):
    if id:
        return cur.execute("SELECT DISTINCT answer from que2 where id='{}'".format(id)).fetchone()[0]
    stmt = "SELECT DISTINCT answer from question where question='{}'".format(selected_question)
    return cur.execute(stmt).fetchone()[0]


def insert_data(question, answer=None, category='Anonymous'):
    insert_stmt = r"""INSERT into question(question, answer, category) values ('{}','{}','{}')""".\
        format(question.replace("'", "''"),
               answer.replace("'", "''"),
               category)
    print(insert_stmt)
    cur.execute(insert_stmt)
    conn.commit()


#
#
# while True:
#     ui = input('> ')
#     if ui == 'quit':
#         exit(0)
#     bot_response = test_response(ui)
#     if not bot_response:
#         print('Response Failed. Log Added.')
#         continue
#     print(bot_response)
#
