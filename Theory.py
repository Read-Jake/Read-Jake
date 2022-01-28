__note_number__ = 1
notes_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", ]
notes_flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", ]
notes_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
octaves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

note_sharp_number = {}
for no in octaves:
    for note in notes_sharp:
        note_sharp_number.update({(note, no): __note_number__})
        __note_number__ += 1

__note_number__ = 1

note_flat_number = {}
for no in octaves:
    for note in notes_flat:
        note_flat_number.update({(note, no): __note_number__})
        __note_number__ += 1

__note_number__ = 1
number_note_flat = {}
for no in octaves:
    for note in notes_flat:
        number_note_flat.update({__note_number__: (note, no)})
        __note_number__ += 1

__note_number__ = 1
number_note_sharp = {}
for no in octaves:
    for note in notes_sharp:
        number_note_sharp.update({__note_number__: (note, no)})
        __note_number__ += 1


note_number = note_sharp_number.copy()
for dict_key, value in note_flat_number.items():
    note_number.update({dict_key: value})
for dict_key, value in note_sharp_number.items():
    note_number.update({dict_key: value})


def get_note_sharp(num):
    """
    gives the number associated to each note in each octave
    """
    for note_key, note_value in note_sharp_number.items():
        if num == note_value:
            return note_key
        else:
            pass


def get_note_flat(num):
    for note_key, note_value in note_flat_number.items():
        if num == note_value:
            return note_key


sharp_keys = {'major': ["C", "D", "E", "G", "A", "B"], 'minor': ['A', 'E', 'B', 'F#', 'C#', 'G#']}
flat_keys = {'major': ["Db", "Eb", "F", "Ab", "Bb"], 'minor': ['D', 'G', 'C', 'F', 'Bb']}

sharp_majors = ["C", "D", "E", "G", "A", "B"]
flat_majors = ["Db", "Eb", "F", "Ab", "Bb"]
sharp_minors = ['A', 'E', 'B', 'F#', 'C#', 'G#']
flat_minors = ['D', 'G', 'C', 'F', 'Bb']

# the following is a dictionary associating chords with specific scale degrees in different modes

major_chord = {'I': (1, 3, 5), 'ii': (2, 4, 6), 'iii': (3, 5, 7), 'IV': (4, 6, 1),
               'V': (5, 7,  2), 'vi': (6, 1, 3), 'vii0': (7, 2, 4), 'V7': (5, 7, 2, 4),
               'ii7': (2, 4, 6, 1)
               }

minor_chord = {'i': (1, 3, 5), 'ii0': (2, 4, 6), 'III': (3, 5, 7),
               'iv': (4, 6, 1), 'v': (5, 7, 2), 'v7': (5, 7, 2, 4),
               'VI': (6, 1, 3), 'VII': (7, 2, 4), 'ii*7': (2, 4, 6, 1)
               }

chord_name = {'major': {'tonic': 'I', 'dominant': ['V7', 'V'], 'subdominant': 'IV',
                        'mediant': 'iii', 'submediant': 'vi', 'supertonic': ['ii', 'ii7'], 'subtonic': 'vii0'},
              'minor': {'tonic': 'i', 'dominant': ['v7', 'v'], 'subdominant': 'iv', 'mediant':
                        'III', 'submediant': 'VI', 'supertonic': ['ii0', 'ii*7'], 'subtonic': 'VII'}
              }

name_chord = {'major': {'I': 'tonic', 'V': 'dominant', 'V7': 'dominant', 'IV': 'subdominant',
                        'iii': 'mediant', 'vi': 'submediant', 'ii': 'supertonic',
                        'ii7': 'supertonic', 'vii0': 'subtonic'},
              'minor': {'i': 'tonic', 'v': 'dominant', 'v7': 'dominant', 'iv': 'subdominant',
                        'III': 'mediant', 'VI': 'submediant', 'ii0': 'supertonic',
                        'ii*7': 'supertonic', 'VII': 'subtonic'}
              }

root, first, second, third = 0, 1, 2, 3
secondary_inversion_options = {'major': {'dominant': [root, first, third, second],
                                         'subdominant': [root, first, third, second],
                                         'submediant': [first, root],
                                         'supertonic': [first, third, root]},
                               'minor': {'dominant': [first, third, root, second],
                                         'subdominant': [first, third, root, second],
                                         'mediant': [root, first],
                                         'submediant': [first, root, second],
                                         'subtonic': [first, root]}
                               }

four_part_major_minor_chord_options = {'major': {'V': ['I', 'ii', 'IV', 'vii0', 'ii7', 'V', 'vi'],
                                                 'IV': ['I', 'IV', 'vi', 'iii'],
                                                 'I': ['I', 'V', 'IV', 'vii0', 'V7'],
                                                 'iii': ['I'], 'ii': ['I', 'IV', 'vi', 'ii'],
                                                 'vi': ['I', 'V'], 'vii0': ['I', 'IV', 'ii'],
                                                 'ii7': ['IV', 'vi', 'I'],
                                                 'V7': ['I', 'ii', 'ii7', 'IV', 'vii0', 'vi', 'V']},
                                       'minor': {'iv': ['i', 'iv', 'VI', 'III'], 'III': ['i'],
                                                 'i': ['i', 'v', 'iv', 'VII', 'v7'],
                                                 'ii*7': ['i', 'iv', 'VI'], 'ii0': ['i', 'iv', 'VI'],
                                                 'VI': ['i', 'v', 'v7'], 'VII': ['i', 'iv', 'ii0'],
                                                 'v7': ['i', 'ii0', 'iv', 'VII', 'ii*7', 'v', 'v7'],
                                                 'v': ['i', 'ii0', 'iv', 'VII', 'ii*7', 'v']}
                                       }

modulation_keys = {'major': ['dominant', 'subdominant', 'submediant', 'supertonic', 'submediant'],
                   'minor': ['dominant', 'subdominant', 'subtonic', 'mediant', 'submediant']
                   }


def augment(note):
    """
    returns a list of a note that has either added a sharp or removed a flat
    + the new number of the note. eg: input = ('e',4), outpute = [('e#',4),42]
    """

    if '#' in note[0][1:]:

        note_name = note[0]+'#'
        sharp_number = note_name.count('#')
        octave = note[1]
        repeated_twelves = sharp_number//12
        remainder = sharp_number - repeated_twelves*12

        remainders = {'B': 1, 'A': 3, 'G': 5, 'F': 7, 'E': 8, 'D': 10, 'C': 0}

        if remainder == remainders[note_name[0]]:
            octave += 1

        temporary_octave = octave - repeated_twelves

        if remainder >= remainders[note_name[0]]:
            temporary_octave -= 1

        note_value = note_number[(note_name[0], temporary_octave)] + sharp_number

    elif 'b' in note[0][1:]:

        note_name = note[0][:-1]
        flat_number = note_name.count('b')
        octave = note[1]
        repeated_twelves = flat_number//12
        remainder = flat_number - repeated_twelves*12

        remainders = {'B': 11, 'A': 9, 'G': 7, 'F': 5, 'E': 4, 'D': 2, 'C': 0}

        if remainder == remainders[note_name[0]]:
            octave += 1

        temporary_octave = octave + repeated_twelves

        if remainder > remainders[note_name[0]]:
            temporary_octave += 1

        note_value = note_number[(note_name[0], temporary_octave)] - flat_number

    else:
        note_name = note[0]+'#'
        note_value = note_number[note] + 1
        octave = get_note_sharp(note_value)[1]

    return [(note_name, octave), note_value]


def diminish(note):
    """
    returns a list of note that has either added a flat or removed a sharp
    + the new number of the note. eg: [('fb',4),41]
    """
    if '#' in note[0][1:]:

        note_name = note[0][:-1]
        sharp_number = note_name.count('#')
        octave = note[1]
        repeated_twelves = sharp_number//12
        remainder = sharp_number - repeated_twelves*12

        remainders = {'C': 11, 'D': 9, 'E': 7, 'F': 6, 'G': 4, 'A': 2, 'B': 0}

        if remainder == remainders[note_name[0]]:
            octave -= 1

        temporary_octave = octave - repeated_twelves

        if remainder > remainders[note_name[0]]:
            temporary_octave -= 1

        note_value = note_number[(note_name[0], temporary_octave)] + sharp_number

    elif 'b' in note[0][1:]:

        note_name = note[0]+'b'
        flat_number = note_name.count('b')
        octave = note[1]
        repeated_twelves = flat_number//12
        remainder = flat_number - repeated_twelves*12

        remainders = {'C': 1, 'D': 3, 'E': 5, 'F': 6, 'G': 8, 'A': 10, 'B': 0}

        if remainder == remainders[note_name[0]]:
            octave -= 1

        temporary_octave = octave + repeated_twelves

        if remainder >= remainders[note_name[0]]:
            temporary_octave += 1

        note_value = note_number[(note_name[0], temporary_octave)] - flat_number

    else:
        note_name = note[0]+'b'
        note_value = note_number[note] - 1
        octave = get_note_flat(note_value)[1]

    return [(note_name, octave), note_value]


def note_index_conv(note):
    """
    put in a note, get a number, regardless of if the note is in the key or not
    """
    if note[0] in [*notes_sharp, *notes_flat]:
        return note_number[note]
    else:
        if note[0][-1] == '#':
            diff = 0
            while note[0] not in notes_sharp:
                note = diminish(note)[0]
                diff += 1
            return note_number[note] + diff
        elif note[0][-1] == 'b':
            diff = 0
            while note[0] not in notes_sharp:
                note = augment(note)[0]
                diff += 1
            return note_number[note] - diff


class Mistake:
    """
    this class will look for voice leading mistakes between four notes across two voices
    """
    def __init__(self, upper_voice_1, upper_voice_2, lower_voice_1, lower_voice_2):

        if type(upper_voice_1) == tuple:  # converts all input into integers of note values
            self.upper_1 = note_index_conv(upper_voice_1)
        else:
            self.upper_1 = upper_voice_1
        if type(upper_voice_2) == tuple:
            self.upper_2 = note_index_conv(upper_voice_2)
        else:
            self.upper_2 = upper_voice_2
        if type(lower_voice_1) == tuple:
            self.lower_1 = note_index_conv(lower_voice_1)
        else:
            self.lower_1 = lower_voice_1
        if type(lower_voice_2) == tuple:
            self.lower_2 = note_index_conv(lower_voice_2)
        else:
            self.lower_2 = lower_voice_2

    def parallels(self):
        """
        Checks if there are either parallel octaves or parallel fifths between two voices.
        Returns True if there are. Returns False if there aren't.
        """
        if type(self.upper_1) == tuple:  # converts all input into integers of note values
            self.upper_1 = note_number[self.upper_1]
        if type(self.upper_2) == tuple:
            self.upper_2 = note_number[self.upper_2]
        if type(self.lower_1) == tuple:
            self.lower_1 = note_number[self.lower_1]
        if type(self.lower_2) == tuple:
            self.lower_2 = note_number[self.lower_2]

        if self.upper_1 == self.upper_2:
            # paralles don't count if they're stationary
            return False
        elif (self.upper_1 - self.upper_2) * (self.lower_1 - self.lower_2) < 0:
            # checks if they move in contrary motion
            return False
        elif (self.upper_1 - self.lower_1) % 12 == 0 and (self.upper_2 - self.lower_2) % 12 == 0:
            # checks for parallel octaves
            return True

        elif ((self.upper_1 - 7) - self.lower_1) % 12 == 0 and ((self.upper_2 - 7) - self.lower_2) % 12 == 0:
            # checks for parallel fifths
            return True

        else:
            return False

    def voice_crossing(self):
        if type(self.upper_1) == tuple:  # converts all input into integers of note values
            self.upper_1 = note_number[self.upper_1]
        if type(self.upper_2) == tuple:
            self.upper_2 = note_number[self.upper_2]
        if type(self.lower_1) == tuple:
            self.lower_1 = note_number[self.lower_1]
        if type(self.lower_2) == tuple:
            self.lower_2 = note_number[self.lower_2]

        if self.lower_2 > self.upper_2 or self.lower_2 > self.upper_1:
            return True
        elif self.upper_2 < self.lower_2 or self.upper_2 < self.lower_1:
            return True
        else:
            return False


def pos(number):
    if number > 0:
        return number
    else:
        return 0
