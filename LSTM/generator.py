#imports
import pickle
import numpy as np
from music21 import instrument, note, stream, chord
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.layers import Activation



def prepareSequences(notes, pitchnames, nVocab):
    # same prepareSequences function from LSTM.py
    noteToInt = dict((note, number) for number, note in enumerate(pitchnames))

    sequenceLength = 100
    networkInput = []
    output = []
    for i in range(0, len(notes) - sequenceLength, 1):
        sequenceIn = notes[i:i + sequenceLength]
        sequenceOut = notes[i + sequenceLength]
        networkInput.append([noteToInt[char] for char in sequenceIn])
        output.append(noteToInt[sequenceOut])

    nPatterns = len(networkInput)

    normalisedInput = np.reshape(networkInput, (nPatterns, sequenceLength, 1))
    normalisedInput = normalisedInput / float(nVocab)

    return (networkInput, normalisedInput)


def createNetork(networkInput, nVocab):
    # same network shape but weights are loaded after compiling
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(networkInput.shape[1],
                     networkInput.shape[2]),
        return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(nVocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop')
    model.load_weights('weights.hdf5')

    return model


def generateNotes(model, networkInput, pitchnames, nVocab):
    start = np.random.randint(0, len(networkInput)-1)

    intToNote = dict((number,note) for number, note in enumerate(pitchnames))

    pattern = networkInput[start]
    predictionOutput = []

    # generate 500 notes (~2 minutes of music)
    for noteIndex in range(500):
        predictionInput = np.reshape(pattern, (1, len(pattern), 1))
        predictionInput = predictionInput / float(nVocab)

        prediction = model.predict(predictionInput, verbose=0)

        index = np.argmax(prediction)
        result = intToNote[index]
        predictionOutput.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return predictionOutput


def createMidi(predictionOutput):
    # function to write the prediction output to a MIDI file
    offset = 0
    outputNotes = []

    for pattern in predictionOutput:
        if ('.' in pattern) or pattern.isdigit():
            notesInChord = pattern.split('.')
            notes = []
            for currentNote in notesInChord:
                newNote = note.Note(int(currentNote))
                newNote.storedInstrument = instrument.Piano()
                notes.append(newNote)
            newChord = chord.Chord(notes)
            newChord.offset = offset
            outputNotes.append(newChord)
        else:
            newNote = note.Note(pattern)
            newNote.offset = offset
            newNote.storedInstrument = instrument.Piano()
            outputNotes.append(newNote)

        offset += 0.5


    midiStream = stream.Stream(outputNotes)

    midiStream.write('midi', fp='test_output.mid')

def generate():
    with open('data/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    pitchnames = sorted(set(item for item in notes))

    nVocab = len(set(notes))
    

    networkInput, normalisedInput = prepareSequences(notes, pitchnames, nVocab)
    model = createNetwork(normalisedInput, nVocab)
    predictionOutput = generateNotes(model, networkInput, pitchnames, nVocab)
    createMidi(predictionOutput)

# generate on running of the program
if __name__ == '__main__':
    generate()







