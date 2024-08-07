from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import tensorflow_datasets as tfds
from model import PositionalEncoding, MultiHeadAttentionLayer, create_padding_mask
import re, pickle


app = Flask(__name__)

model = tf.keras.models.load_model(
    "./models/model-v3.h5",
    custom_objects={
        "PositionalEncoding": PositionalEncoding,
        "MultiHeadAttentionLayer": MultiHeadAttentionLayer,
    },
    compile=False,
)

tokenizer = tfds.deprecated.text.SubwordTextEncoder.load_from_file('tokenizer_v3')
START_TOKEN, END_TOKEN = [tokenizer.vocab_size], [tokenizer.vocab_size + 1]
VOCAB_SIZE = tokenizer.vocab_size + 2
MAX_LENGTH = 50

def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    # reating a space between a word and the punctuation following it
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r'[" "]+', " ", sentence)

    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    sentence = re.sub(r"[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9?.!,]+", " ", sentence)
    sentence = sentence.strip()
    return sentence


def postprocess_sentence(sentence):
    # capitalize the first letter
    sentence = sentence.capitalize()
    # remove spaces before punctuation
    sentence = re.sub(r'\s([?.!,])', r'\1', sentence)
    return sentence


def evaluate(sentence):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(
        START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0
    )

    output = tf.expand_dims(START_TOKEN, 0)

    for i in range(MAX_LENGTH):
        predictions = model(inputs=[sentence, output], training=False)

        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        if tf.equal(predicted_id, END_TOKEN[0]):
            break

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sentence = data.get('message')
    prediction = evaluate(sentence)
    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size]
    )
    predicted_sentence = postprocess_sentence(predicted_sentence)
    return jsonify({'reply': predicted_sentence})


if __name__ == '__main__':
    app.run(debug=True)
