#!/usr/bin/env python

# NOTICE - this is a derivative work of the TF tutorial
# https://www.tensorflow.org/tutorials/sequences/text_generation

# Copyright 2019 tgandor
# (modifications under same license)

# Copyright 2018 The TensorFlow Authors.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# will this be ever run under 2.0?
from __future__ import absolute_import, division, print_function
# luckily, generator_stop and annotations can just be ignored

import argparse
import datetime
import json
import os
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs='?', help='input corpus (txt file) or trained model metadata (.json)')
parser.add_argument('start', nargs='?', help='string to start generating from (context)')
parser.add_argument('--cpu', action='store_true', help='force using CPU even if GPU available')
parser.add_argument('--epochs', '-e', type=int, default=10, help='epochs to train (# corpus sizes)')
parser.add_argument('--length', '-l', type=int, default=1000, help='nubmer of characters to generate')
parser.add_argument('--save', '-o', default='model.json', help='model metadata saving path (only training)')
parser.add_argument('--temperature', '-t', type=float, default=1.0, help='randomness of generated text')
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

# Not pep8 compliant, but you don't want to wait for argparse's --help until TF finishes importing..."

import numpy as np
import tensorflow as tf
tf.enable_eager_execution()

def main():
    """Main program.

    This way I can use functions defined below, unlike raw script."""

    if args.input and args.input.endswith('.json'):
        model, char2idx, idx2char = load_model()
    else:
        model, char2idx, idx2char = train_model()

    if args.start:
        print(generate_text(model, args.start, char2idx, idx2char, args.length))
    else:
        while True:
            start = prompt('Enter initial sequence: ')

            if not start:
                print('bye')
                break

            print(generate_text(model, start, char2idx, idx2char, args.length))


# functions


def prompt(msg=''):
    try:
        import readline
    except ImportError:
        pass

    try:
        import six
        return six.moves.input(msg)
    except ImportError:
        return input(msg)


def load_model():
    with open(args.input) as js:
        metadata = json.load(js)

    char2idx = metadata['char2idx']
    embedding_dim = metadata['embedding_dim']
    last_checkpoint = metadata['last_checkpoint']
    rnn_units = metadata['rnn_units']

    vocab = sorted(set(char2idx.keys()))
    vocab_size = len(vocab)
    idx2char = np.array(vocab)

    model = _model_for_prediction(last_checkpoint, vocab_size, embedding_dim, rnn_units)

    print('Model loaded from:', last_checkpoint)

    return model, char2idx, idx2char

def train_model():
    if not args.input:
        if args.verbose:
            print('Using default corpus - Shakespeare')
        path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
        if args.verbose:
            print('Corpus is here:', path_to_file)
    else:
        path_to_file = args.input

    # these mappings need to be saved, if model is to be used without corpus.
    char2idx, idx2char, text_as_int = vectorize_corpus(path_to_file)
    vocab = list(idx2char)

    # Dataset parameters
    # The maximum length sentence we want for a single input in characters
    seq_length = 100
    examples_per_epoch = len(text_as_int) // seq_length

    # Dataset - 100 chars + offset by 1:
    dataset = create_dataset(text_as_int, seq_length)

    if args.verbose:
        print('Dataset example:')
        for input_example, target_example in  dataset.take(1):
            print ('Input data: ', repr(''.join(idx2char[input_example.numpy()])))
            print ('Target data:', repr(''.join(idx2char[target_example.numpy()])))

    # model for training:
    BATCH_SIZE = 64
    steps_per_epoch = examples_per_epoch//BATCH_SIZE

    # Length of the vocabulary in chars
    vocab_size = len(vocab)

    # The embedding dimension
    embedding_dim = 256

    # Number of RNN units
    rnn_units = 1024

    # Buffer size to shuffle the dataset
    # (TF data is designed to work with possibly infinite sequences,
    # so it doesn't attempt to shuffle the entire sequence in memory. Instead,
    # it maintains a buffer in which it shuffles elements).
    BUFFER_SIZE = 10000

    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    model = build_model(
        vocab_size=len(vocab),
        embedding_dim=embedding_dim,
        rnn_units=rnn_units,
        batch_size=BATCH_SIZE
    )

    if args.verbose:
        print('Model performance before training:')
        for input_example_batch, target_example_batch in dataset.take(1):
            example_batch_predictions = model(input_example_batch)
            print('Return shape:', example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")
            # To get actual predictions from the model we need to sample from the output distribution,
            # to get actual character indices. This distribution is defined by the logits over the character vocabulary.
            # Note:
            # It is important to sample from this distribution as taking the argmax of the distribution can easily
            # get the model stuck in a loop.
            sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
            sampled_indices = tf.squeeze(sampled_indices,axis=-1).numpy()
            print("Input:", repr("".join(idx2char[input_example_batch[0]])))
            print("Next Char Predictions:", repr("".join(idx2char[sampled_indices])))

    def loss(labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    if args.verbose:
        example_batch_loss  = loss(target_example_batch, example_batch_predictions)
        print('Loss on initial example:', example_batch_loss.numpy().mean())

    model.compile(optimizer=tf.train.AdamOptimizer(), loss=loss)

    if args.verbose:
        model.summary()

    # Directory where the checkpoints will be saved
    checkpoint_dir = './training_checkpoints'

    # Name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True
    )

    start = datetime.datetime.now()
    EPOCHS = args.epochs if args.epochs > 0 else 3
    print(start, 'Starting training for', EPOCHS, 'epochs.')

    history = model.fit(dataset.repeat(), epochs=EPOCHS, steps_per_epoch=steps_per_epoch, callbacks=[checkpoint_callback])

    last_checkpoint = tf.train.latest_checkpoint(checkpoint_dir)
    print('Last checkpoint:', last_checkpoint)

    finish = datetime.datetime.now()
    print(finish, 'Finished training, Elapsed time:', finish - start)

    # save the model for re-use
    if args.save:
        metadata = {
            'char2idx': char2idx,
            # JSON has no int keys... we'll have to do without it, the information is there above.
            # 'idx2char': dict(enumerate(idx2char)),
            'embedding_dim': embedding_dim,
            'last_checkpoint': last_checkpoint,
            'rnn_units': rnn_units,
        }

        with open(args.save, 'w') as js:
            json.dump(metadata, js, indent=2)

        print('Metadata saved to:', args.save)

    # Prepare model for work - load last checkpoint etc.

    model = _model_for_prediction(last_checkpoint, vocab_size, embedding_dim, rnn_units)

    return model, char2idx, idx2char


def _model_for_prediction(last_checkpoint, vocab_size, embedding_dim, rnn_units):
    """Initialize model for 1-char batch with loaded weights."""
    model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)  # we'll use 1-char batches for prediction
    model.load_weights(last_checkpoint)
    model.build(tf.TensorShape([1, None]))
    return model


def vectorize_corpus(path_to_file):
    # Read, then decode for py2 compat.
    text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
    # length of text is the number of characters in it
    if args.verbose:
        print('Length of text: {} characters'.format(len(text)))
        print('Sample:', text[:250])

    vocab = sorted(set(text))
    if args.verbose:
        print ('{} unique characters: {!r}'.format(len(vocab), vocab))

    # Creating a mapping from unique characters to indices
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    text_as_int = np.array([char2idx[c] for c in text])

    return char2idx, idx2char, text_as_int


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    if tf.test.is_gpu_available() and not args.cpu:
        if args.verbose:
            print('using GPU')
        rnn = tf.keras.layers.CuDNNGRU
    else:
        if args.verbose:
            print('using CPU')
        import functools
        rnn = functools.partial(tf.keras.layers.GRU, recurrent_activation='sigmoid')

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        rnn(rnn_units, return_sequences=True, recurrent_initializer='glorot_uniform', stateful=True),
        tf.keras.layers.Dense(vocab_size)
    ])

    return model


def create_dataset(text_as_int, seq_length):
    # Create training examples / targets
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)

    def split_input_target(chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text

    dataset = sequences.map(split_input_target)

    return dataset


def generate_text(model, start_string, char2idx, idx2char, num_generate=1000):
  # Evaluation step (generating text using the learned model)

  # Converting our start string to numbers (vectorizing)
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # Empty string to store our results
  text_generated = []

  # Low temperatures results in more predictable text.
  # Higher temperatures results in more surprising text.
  # Experiment to find the best setting.
  temperature = args.temperature

  # Here batch size == 1
  model.reset_states()
  for i in range(num_generate):
      predictions = model(input_eval)
      # remove the batch dimension
      predictions = tf.squeeze(predictions, 0)

      # using a multinomial distribution to predict the word returned by the model
      predictions = predictions / temperature

      # predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      # We pass the predicted word as the next input to the model
      # along with the previous hidden state
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])

  return (start_string + ''.join(text_generated))


if __name__ == '__main__':
    main()
