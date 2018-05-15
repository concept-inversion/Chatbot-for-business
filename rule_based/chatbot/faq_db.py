import shelve
import sqlite3
import nltk
from fuzzywuzzy import fuzz
from nltk.stem.snowball import SnowballStemmer
from similarity import *

conn = sqlite3.connect('db.faq')
stemmer = SnowballStemmer('english')

cur = conn.cursor()

key_result = cur.execute("select id, question from question").fetchall()
keys_only = [row[1] for row in key_result]


def generate_stem_statement(stmt):
    corpora = nltk.word_tokenize(stmt)
    return ' '.join([stemmer.stem(word) for word in corpora])


def get_highest_matching_key(user_query):
    true_score = [(similarity(generate_stem_statement(user_query), generate_stem_statement(key), True), key) for key in keys_only]
    return sorted(list(filter(lambda d: d[0] > 0.7, true_score)),reverse=True)


while True:
    ui = input('> ')
    ts = get_highest_matching_key(ui)
    print(ts)


# create_faq = "create table if not exists question(id integer primary key, question varchar(255),answer varchar(255), category varchar(100))"
# conn.execute(create_faq)
# js = shelve.open('jobseeker.shelve')
# em = shelve.open('employer.shelve')
#
# for q, s in js.items():
#     stmt = r"INSERT into question(question, answer, category) values ('"+q.replace("'","''")+"','"+s.replace("'","''")+"','jobseeker')"
#     print(stmt)
#     cur.execute(stmt)
#     conn.commit()
#
# for q, s in em.items():
#     stmt = r"INSERT into question(question, answer, category) values ('"+q.replace("'","''")+"','"+s.replace("'","''")+"','employer')"
#     print(stmt)
#     cur.execute(stmt)
#     conn.commit()

