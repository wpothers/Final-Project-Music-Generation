#imports
from music21 import converter, instrument, note, chord
import numpy as np

import glob
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras import backend as K
from keras.utils import np_utils
from tensorflow.keras.callbacks import ModelCheckpoint



def getNotes():
    # function to load the note data into a list
    notes = []

    for file in glob.glob("midi_songs/*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)
        
        notesToParse = None

        # if midi file has more than one instrument
        try:
            s2 = instrument.partitionByInstrument(midi)
            notesToParse = s2.parts[0].recurse()
        # if midi file has notes in a flat structure
        except:
            notesToParse = midi.flat.notes

        for element in notesToParse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    # save note list to use later for generation
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes,filepath)
    
    return notes

def prepareSequences(notes, nVocab):
    # function to prepare the sequences of notes
    # arguments:
    #   notes  - a list of all note and chord objects taken from the training data
    #   nVocab - a set of every unique note and chord used in the training data
    # outputs:
    #   networkInput - input sequences for the network
    #   networkOutput - respective outputs for the input sequence

    sequenceLength = 100

    pitchnames = sorted(set(item for item in notes))
    
    # map pitches to integars 
    notesToInt = dict((note, number) for number, note in enumerate(pitchnames))

    networkInput = []
    networkOutput = []

    for i in range(0, len(notes) - sequenceLength, 1):
        sequenceIn = notes[i:i + sequenceLength]
        sequenceOut = notes[i + sequenceLength]
        networkInput.append([notesToInt[char] for char in sequenceIn])
        networkOutput.append(notesToInt[sequenceOut])

    nPatterns = len(networkInput)

    networkInput = np.reshape(networkInput, (nPatterns, sequenceLength, 1))

    # normalise the input
    networkInput = networkInput / float(nVocab)

    networkOutput = np_utils.to_categorical(networkOutput)

    return (networkInput, networkOutput)


def createNetwork(networkInput, nVocab):
    # function to create the network
    # arguments:
    #   networkInput - the prepared sequences of notes in one hot encoding
    #   nVocab       - a set of every unique note or chord used in the training data
    # outputs:
    #   model        - a three layer LSTM
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(networkInput.shape[1], networkInput.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(nVocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model

def train(model, networkInput, networkOutput):

    # save the weights using a model checkpoint file
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
        )
    callbacksList = [checkpoint]

    # function to train the network in Keras
    model.fit(networkInput, networkOutput, epochs=400, batch_size=64, callbacks=callbacksList)


def trainNetwork():
    # function to train the network
    notes = getNotes()

    nVocab = len(set(notes))

    networkInput, networkOutput = prepareSequences(notes, nVocab)

    model = createNetwork(networkInput, nVocab)

    train(model, networkInput, networkOutput)


# train network on running of program
if __name__ == '__main__':
    trainNetwork()















                         
