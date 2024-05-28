# -*- coding: utf-8 -*-
import os
import re


def process_sub_file(sub_file, skip_lines=5):
    # Whole .srt file preprocessing to conversation pairs
    with open(sub_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove first and last lines to avoid unnecessary information (e.g. about author)
    lines = [line.strip() for line in lines[skip_lines:-5] if line.strip()]

    # Remove tags <i>, <b>, <u>, <font>, <color> etc.
    lines = [re.sub(r'<[^>]+>', '', line) for line in lines]
    lines = [re.sub(r'|', '', line) for line in lines]

    # Remove numbers in {} brackets at the beginning of lines
    lines = [re.sub('{[0-9]*}', '', line) for line in lines]

    movie_conversations = []

    for index, line in enumerate(lines, start=skip_lines):
        # Checking every line in file
        current_conversation = line
        print(index)
        movie_conversations.append(current_conversation)

    return movie_conversations


def save_conversations_to_file(conversation_pairs, output_file):
    # Save conversations to one file
    with open(output_file, 'a', encoding='utf-8') as file:
        for conversation in conversation_pairs:
            file.write(conversation + '\n')


if __name__ == "__main__":
    folder_path = "./datasets/sub/files/"
    final_file = "./datasets/sub/sub-conversations.txt"

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt" or ".sub"):
            sub_file_path = os.path.join(folder_path, filename)
            print("Przetwarzanie pliku:", sub_file_path)

            conversations = process_sub_file(sub_file_path)

            save_conversations_to_file(conversations, final_file)

    print("Wszystkie konwersacje zostały zapisane do pliku:", final_file)
