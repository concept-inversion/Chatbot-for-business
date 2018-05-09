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

