import tensorflow as tf
import tensorflow_datasets as tfds
from datacollection.splitting_pairs import load_data

#print(len(questions))
#print(len(answers))

#print(questions[32122])
#print(answers[32122])

def tokenize_and_filter(hparams, tokenizer, questions, answers):
    tokenized_questions, tokenized_answers = [], []

    for (question, answer) in zip(questions, answers):
        # tokenize sentence
        sentence1 = hparams.start_token + tokenizer.encode(question) + hparams.end_token
        sentence2 = hparams.start_token + tokenizer.encode(answer) + hparams.end_token

        # check tokenize sentence length
        if (
            len(sentence1) <= hparams.max_length
            and len(sentence2) <= hparams.max_length
        ):
            tokenized_questions.append(sentence1)
            tokenized_answers.append(sentence2)

    # pad tokenized sentences
    tokenized_questions = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_questions, maxlen=hparams.max_length, padding="post"
    )
    tokenized_answers = tf.keras.preprocessing.sequence.pad_sequences(
        tokenized_answers, maxlen=hparams.max_length, padding="post"
    )

    return tokenized_questions, tokenized_answers


def get_dataset(hparams):
    questions = load_data('pairs/questions.pkl')
    answers = load_data('pairs/answers.pkl')

    tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
        questions + answers, target_vocab_size=2**13
    )

    hparams.start_token = [tokenizer.vocab_size]
    hparams.end_token = [tokenizer.vocab_size + 1]
    hparams.vocab_size = tokenizer.vocab_size + 2

    questions, answers = tokenize_and_filter(hparams, tokenizer, questions, answers)

    dataset = tf.data.Dataset.from_tensor_slices(
        ({"inputs": questions, "dec_inputs": answers[:, :-1]}, answers[:, 1:])
    )
    dataset = dataset.cache()
    dataset = dataset.shuffle(len(questions))
    dataset = dataset.batch(hparams.batch_size)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)

    return dataset, tokenizer