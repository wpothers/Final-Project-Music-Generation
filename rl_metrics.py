from music21 import converter, instrument, note, chord, key, interval
import glob
import numpy as np

inputFile = 'C:/Users/willb/Documents/Computer Science/Year3/Final Project/results/rl monophonic.mid'

def initStatDict():

    statDict = dict()

    statDict['key_of_piece'] = ''
    statDict['notes_in_key'] = 0
    statDict['notes_not_in_key'] = 0
    statDict['num_repeated_notes'] = 0
    statDict['num_octave_jumps'] = 0
    statDict['num_fifths'] = 0
    statDict['num_high_unique'] = 0
    statDict['num_low_unique'] = 0

    return statDict

def computeStats():
   

    #initialise stat dict
    statDict = initStatDict()
    
    midi = getStream(inputFile)

    notes, noteNums = getNotes(midi)


    #get key of piece
    statDict['key_of_piece'] = str(getKey())

    ks = key.Key(statDict['key_of_piece'][0:2])

    midi.keySignature = ks
    
    #need to set the key to be actual key using key function and then count the accidentals
    notesInKey = findNotesInKey(ks)

    numCorrect, numAccidentals = countAccidentals(notesInKey, notes)
    statDict['notes_in_key'] = numCorrect
    statDict['notes_not_in_key'] = numAccidentals

    numRepeated = detectRepeatingNotes(notes)
    statDict['num_repeated_notes'] = numRepeated

    highUniqueCount = detectHighUnique(noteNums)
    statDict['num_high_unique'] = highUniqueCount
    lowUniqueCount = detectLowUnique(noteNums)
    statDict['num_low_unique'] = lowUniqueCount

    intervals = getIntervals(midi)

    octaves = getOctaveJumps(intervals)
    statDict['num_octave_jumps'] = octaves
    fifths = getFifthJumps(intervals)
    statDict['num_fifths'] = fifths
    

    return statDict

def getOctaveJumps(intervals):
    octaveCount = 0
    for i in range(len(intervals)):
        if intervals[i] == 'P8':
            octaveCount += 1
    return octaveCount

def getFifthJumps(intervals):
    fifthCount = 0
    for i in range(len(intervals)):
        if intervals[i] == 'P5':
            fifthCount += 1
    return fifthCount
        

def getIntervals(stream):
    interval = []
    intervalS = stream.melodicIntervals()
    for i in intervalS:
        interval.append(i.simpleName)
    return interval

def detectHighUnique(noteNums):
    noChords = []
    for i in noteNums:
        if (isinstance(i, list)) == False:
            noChords.append(i)
    maxNote = max(noChords)
    return list(noChords).count(maxNote)

def detectLowUnique(noteNums):
    noChords = []
    for i in noteNums:
        if (isinstance(i, list)) == False:
            noChords.append(i)
    minNote = min(noChords)
    return list(noChords).count(minNote)

def detectRepeatingNotes(notesOfPiece):
    numRepeated = 0
    
    for i in range(len(notesOfPiece)):
        if((i+2)<len(notesOfPiece)):
            if notesOfPiece[i] == notesOfPiece[i+1]:
                repeatKernel += 1
            elif notesOfPiece[i] != notesOfPiece[i+1]:
                repeatKernel = 0

            if repeatKernel > 1:
                numRepeated += 1
    return numRepeated


def countAccidentals(notesInKey, notesOfPiece):
    numCorrect = 0
    numAccidentals = 0
    for notes in notesOfPiece:
        if (notes[:-1] in notesInKey):
            numCorrect += 1
        elif (notes[:-1] not in notesInKey):
            numAccidentals += 1
    return numCorrect, numAccidentals

def findNotesInKey(key):
    notesInKey = []
    for i in key.pitches:
        notesInKey.append(i.name)
    return notesInKey

def getStream(inputFile):
    for file in glob.glob(inputFile):
        midi = converter.parse(file)

    return midi

def getKey():
    midi = getStream(inputFile)

    key = midi.analyze('key')

    return key

def getNotes(stream):
    #stream = getStream()
    
    notes = []
    noteNums = []

    notesToParse = None
    
    try:
        s2 = instrument.partitionByInstrument(stream)
        notesToParse = s2.parts[0].recurse()
    except:
        notesToParse = stream.flat.notes

    for element in notesToParse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
            noteNums.append(element.pitch.midi)
        elif isinstance(element, chord.Chord):
            chorde = []
            chordeNums = []
            for elements in element:
                chorde.append(str(elements.pitch))
                chordeNums.append(elements.pitch.midi)
            notes.append(chorde)
            noteNums.append(chordeNums)
            
    return notes, noteNums


