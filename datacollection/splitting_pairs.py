# -*- coding: utf-8 -*-
import re
import pickle


def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    # creating a space between a word and the punctuation following it
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)

    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    sentence = re.sub(r"[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9?.!,]+", " ", sentence)
    sentence = sentence.strip()
    return sentence


def load_conversations(conversation_file_path):
    # dictionary of line id to text
    inputs, outputs = [], []
    with open(conversation_file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.replace("\n", "").split("|=|")
        query_parts = parts[1:]
        counter = len(query_parts)
        for i in range(counter - 1):
            inputs.append(preprocess_sentence(query_parts[i]))
            outputs.append(preprocess_sentence(query_parts[i + 1]))

    return inputs, outputs


srt_path = './datasets/srt/srt-conversations-new.txt'

questions, answers = load_conversations(srt_path)

save_data(questions, '../pairs/questions-new.pkl')
save_data(answers, '../pairs/answers-new.pkl')

print(len(questions))
print(len(answers))
