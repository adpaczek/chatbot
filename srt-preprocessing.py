import os
import re


def process_srt_file(srt_file, skip_lines=10, max_time_gap=6.4):
    # Whole .srt file preprocessing to conversation pairs
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove first and last lines to avoid unnecessary information (e.g. about author)
    lines = [line.strip() for line in lines[skip_lines:-7] if line.strip()]

    # Remove lines that are not conversation lines or time frames
    lines = [line for line in lines if not re.match(r'^\d+\s*$', line)]

    # Remove tags <i>, <b>, <u>, <font>, <color> etc.
    lines = [re.sub(r'<[^>]+>', '', line) for line in lines]

    # Remove lines that are stage directions
    lines = [re.sub(r'\[.*\]', '', line) for line in lines]

    # Remove lines that are not conversation lines or time frames
    lines = [line for line in lines if not re.match(r'^\d+\s*$', line)]

    movie_conversations = []
    current_conversation = ""
    last_end_time = ""

    for index, line in enumerate(lines, start=skip_lines):
        # Checking every line in file
        if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
            times = re.findall(r'\d+:\d+:\d+,\d+', line)
            start_time = times[0]
            if last_end_time:
                time_gap = convert_time_to_seconds(start_time) - convert_time_to_seconds(last_end_time)
                if time_gap >= max_time_gap:
                    movie_conversations.append(current_conversation.strip())
                    movie_conversations.append('+++')
                    current_conversation = ""
            last_end_time = times[1]
        else:
            if line.strip() and not (line.strip() == "-" or line.strip() == " " or line.strip() == " -"):
                if line.startswith(tuple('.abcćdefghijklłmnopqrsśtuvwxyzżź')):
                    current_conversation += " " + line
                else:
                    current_conversation += "|=|" + line

    if current_conversation:
        movie_conversations.append(current_conversation.strip())

    return movie_conversations


def convert_time_to_seconds(time_str):
    # Check milliseconds
    if ',' in time_str:
        time_str, milliseconds = time_str.split(',')
    else:
        milliseconds = '000'

    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds + int(milliseconds) / 1000
    return total_seconds


def save_conversations_to_file(conversation_pairs, output_file):
    # Save conversations to one file
    with open(output_file, 'a', encoding='utf-8') as file:
        for conversation in conversation_pairs:
            file.write(conversation + '\n')


if __name__ == "__main__":
    folder_path = "./datasets/srt/files/"
    final_file = "datasets/srt/srt-conversations.txt"

    for filename in os.listdir(folder_path):
        if filename.endswith(".srt"):
            srt_file_path = os.path.join(folder_path, filename)
            print("Przetwarzanie pliku:", srt_file_path)

            conversations = process_srt_file(srt_file_path)

            save_conversations_to_file(conversations, final_file)

    print("Wszystkie konwersacje zostały zapisane do pliku:", final_file)

