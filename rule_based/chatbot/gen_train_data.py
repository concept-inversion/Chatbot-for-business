from pylog import LogQuery


def gen_data():
    lg = LogQuery()
    result_set = lg.fetch_data()
    file = open('train.txt', 'w')
    for row in result_set:
        print(row)
        temp = '>' + row.get('query').replace('\n', '') + '\n'
        file.write(temp)
        temp = '>' + row.get('attempted_response').replace('\n', '') + '\n'
        file.write(temp)

    file.close()

gen_data()

