import pickle
import random
import csv


def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

questions = load_data('questions-new.pkl')
answers = load_data('answers-new.pkl')

# determining the number of pairs to be drawn
num_pairs = 500

# 500 unique indices
random_indices = random.sample(range(len(questions)), num_pairs)

# pairs drawn
wylosowane_pary = [(questions[i], answers[i]) for i in random_indices]

# saving pairs to a CSV file
with open('pairs_quality.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Zapytanie', 'Odpowiedź'])  
    for zapytanie, odpowiedź in wylosowane_pary:
        csvwriter.writerow([zapytanie, odpowiedź])
