"""
Script taken and modified from: https://keras.io/examples/lstm_text_generation/
Changes introduced a different prediciton methodology, text preprocessing, and
better code documentation
"""
# Built-in modules
from __future__ import print_function
import random
import json
import sys

# External modules
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import LambdaCallback
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import RMSprop

# Read in the training and prediction data
artist = "Taylor_Swift"
path = "./data/Taylor+Swift_preprocessed.txt"
text = []
with open(path) as f:
    text = f.read().lower()
print('corpus length:', len(text))
text_prediction = []
with open("./data/text_prediction.json", 'r') as json_f:
    text_prediction = json.load(json_f)

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# Cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# Build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars), activation='softmax'))

optimizer = RMSprop(learning_rate=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    """ 
    Helper function to sample an index from a probability array    
    
    Parameters
    ----------
    preds: 

    temperature: float
        Varies the randomness of choosing the index

    Returns
    -------
    int:
        Chosen index from the probability array
    """ 
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

class CustomSaver(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if epoch % 5 == 0:
            self.model.save(f"{artist}_{epoch}.hd5")

def on_epoch_end(epoch, _):
    """ 
    Function invoked at end of each epoch. Prints generated text.
    
    Parameters
    ----------
    epoch: int 
        No. the epoch

    Returns
    -------
    None    
    """ 
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    for diversity in [0.2, 0.5, 1.0]:
        print('----- diversity:', diversity)
        for text in text_prediction:
            generated = ''
            # Take the last maxlen characters from the sentence
            sentence = text[-maxlen:]
            generated += sentence
            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for i in range(50):
                x_pred = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, char_indices[char]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = indices_char[next_index]

                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                sys.stdout.flush()
            print()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
saver_callback = CustomSaver()

history = model.fit(x, y,
            batch_size=128,
            epochs=20,
            callbacks=[print_callback, saver_callback])


print(history.history)
def show_history(history, title):
    plt.title(title)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train_accuracy', 'validation_accuracy'], loc='best')
    plt.savefig(f"./results_{title}")

show_history(history, f"{artist}_accuracy")