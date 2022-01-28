"""
New four part - optimised
"""
from Phrase import *
from random import sample, choice


class FourPart(phrase):
    
    def __init__(self, canto, key):
        phrase.__init__(self, canto, key)
        self.cadence_assign()
        self.chord_assign()
        self.inversion_assign()
        self.bassline_assign()
        self.alto_tenor_assign()
        # todo self.conversions
        self.formating()
    
    def cadence_assign(self):
        """
        Assigns a Cadence to the Phrase given
        """
        self.chords.clear()
        self.inversions.clear()
        ultima = self.note_degree[self.canto[-1][0]]
        penultima = self.note_degree[self.canto[-2][0]]
        if ultima in self.chord_scale_degrees[self.chord_name['tonic']] and \
           penultima in self.chord_scale_degrees[self.chord_name['dominant'][1]]:

            self.chords.append(choice(self.chord_name['dominant']))
            self.chords.append(self.chord_name['tonic'])

        elif ultima == 3 and penultima == 4:

            self.chords.append(self.chord_name['dominant'][0])
            self.chords.append(self.chord_name['tonic'])

        elif ultima in self.chord_scale_degrees[self.chord_name['dominant'][1]]:

            self.chords.append(choice(self.chord_name['dominant']))
                    
        for chord in range(len(self.chords)):
            self.inversions.update({len(self.canto)-(chord+1): 0})
            
    def chord_assign(self):
        """
        returns a suggestion of functional chords
        """
        chord_options = four_part_major_minor_chord_options[self.modality]

        while len(self.canto) != len(self.chords):
        
            index = len(self.canto)-(len(self.chords)+1)
            canto_note = self.canto[index]
            next_chord = self.chords[0]

            if self.secondary_dominant_index[index] == 'dominant':
                self.chords.insert(0, next_chord)
                continue

            canto_degree = self.note_degree[canto_note[0]]
            options = [chord for chord in chord_options[next_chord] if canto_degree in self.chord_scale_degrees[chord]]
            
            if self.secondary_dominant_index[index] == 'tonic':
                secondary_note = self.canto[index-1]
                removed_options = []
                for option in options:

                    chord_root = self.degree_note[self.chord_scale_degrees[option][0]]
                    secondary_chord = self.find_dominant(chord_root)
                    if secondary_note[0] not in secondary_chord or option[-1] in ['0', '7']:
                        removed_options.append(option)

                for option in removed_options:
                    options.remove(option)

            try:
                self.chords.insert(0, choice(options))
            except:
                self.cadence_assign()
                self.attempts += 1
                if self.attempts == self.max_attempts:
                    raise Exception('Max Attempts Reached at Chord Assign')
                
        if self.note_degree[self.canto[0][0]] in [1, 3] and self.chords[0] != self.chord_name['tonic']:  # this assures the first chord is 'I' if possible
            self.chords[0] = self.chord_name['tonic']
            
        elif self.note_degree[self.canto[0][0]] == 5:
            if self.note_degree[self.canto[1][0]] in [4, 6]:
                self.chords[0] = self.chord_name['tonic']
            else:
                options = [self.chord_name['tonic'], *self.chord_name['dominant']]
                self.chords[0] = choice(options)
                
        elif self.note_degree[self.canto[0][0]] in [7, 2]:
            self.chords[0] = choice(self.chord_name['dominant'])
            
    def inversion_assign(self):
        """
        takes the chord suggestion and provides a selection of inversions
        """
        
        index_reference = len(self.chords)-len(self.inversions.keys())
        
        while len(self.inversions.keys()) != len(self.chords):
            
            index = index_reference - (len(self.chords) - len(self.inversions))
            current_chord = self.chords[index]
            next_chord = self.chords[index+1]
            previous_chord = self.chords[index-1]

            if index == 0:  # if the chord position is 0. This is included to avoid Syntax Errors in later elif clauses
                
                if current_chord == self.chord_name['dominant'][0]:  # if the first chord is V7

                    options = [root, first, third]
                    if self.note_degree[self.canto[index][0]] in [7, 4]:
                        options.remove({7: first, 4: third}[self.note_degree[self.canto[index][0]]])
                    self.inversions.update({index: choice(options)})

                elif current_chord == self.chord_name['dominant'][1]:  # if the first chord is V

                    options = [root, first]
                    if (self.note_degree[self.canto[index][0]] == 7) or \
                       (next_chord == self.chord_name['submediant']):
                        options.remove(first)
                    self.inversions.update({index: choice(options)})

                elif current_chord == self.chord_name['subtonic']:

                    self.inversions.update({index: first})  # if the first chord is vii0

                else:  # if the first chord is anything else

                    self.inversions.update({index: root})
                    
            elif self.secondary_dominant_index[index] == 'tonic':

                if self.inversions[index-1] == third:

                    self.inversions.update({index: first})

                else:

                    self.inversions.update({index: root})
            
            elif self.secondary_dominant_index[index] == 'dominant':  # if the current chord is a secondary dominant

                current_chord = self.find_dominant(self.degree_note[self.chord_scale_degrees[next_chord][0]])
                options = self.secondary_inversions[self.name_chord[next_chord]]

                if current_chord.index(self.canto[index][0]) in [1, 2, 3] and current_chord.index(self.canto[index][0]) in options:
                    options.remove({1: first, 2: second, 3: third}[current_chord.index(self.canto[index][0])])
                self.inversions.update({index: choice(options)})

            elif current_chord == self.chord_name['tonic']:  # if the current chord is I or i
                if (index == 0) or \
                   (next_chord == self.chord_name['mediant']) or \
                   (previous_chord in self.chord_name['dominant'] and self.inversions[index-1] == first) or \
                   (previous_chord == self.chord_name['tonic'] and self.inversions[index-1] == first) or \
                   (previous_chord in self.chord_name['dominant'] and self.chords[index-2] in self.chord_name['dominant'] and
                    self.inversions.get(index-1) == root and self.inversions.get(index-2) == first) or \
                   (previous_chord == self.chord_name['dominant'][0] and self.inversions[index-1] == root) or \
                   (self.note_degree.get(self.canto[index]) == 3):

                    self.inversions.update({index: root})

                elif (previous_chord == self.chord_name['dominant'][0] and self.inversions[index-1] == third) or \
                     (previous_chord == self.chord_name['tonic'] and self.inversions[index-1] == root) or \
                     (index == len(self.canto)-3 and next_chord in self.chord_name['dominant']):

                    self.inversions.update({index: first})

                else:

                    self.inversions.update({index: choice([root, first])})

            elif current_chord == self.chord_name['dominant'][1]:  # if the current chord is V
                
                if (next_chord == self.chord_name['submediant']) or \
                   (previous_chord in self.chord_name['dominant'] and self.inversions[index-1] == first) or \
                   (previous_chord == self.chord_name['tonic'] and self.modality == 'minor' and self.inversions[index-1] == first):

                    self.inversions.update({index: root})
                    
                elif (previous_chord in self.chord_name['dominant'] and self.inversions[index-1] == root) or \
                     (index == len(self.canto)-3 and next_chord in self.chord_name['dominant']):

                    self.inversions.update({index: first})

                else:

                    self.inversions.update({index: choice([root, first])})
                
            elif current_chord == self.chord_name['dominant'][0]:  # if the current chord is V7
                
                options = [first, second, third]
                
                if (next_chord == self.chord_name['submediant']) or \
                   (previous_chord in self.chord_name['dominant'] and self.inversions[index-1] == first) or \
                   (previous_chord in self.chord_name['supertonic'] and self.inversions[index-1] == first):

                    self.inversions.update({index: root})

                elif previous_chord in self.chord_name['supertonic'] and self.inversions[index-1] == first:

                    self.inversions.update({index: choice([second, root])})

                elif (next_chord in self.chord_name['dominant']):

                    self.inversions.update({index: first})

                elif self.note_degree[self.canto[index][0]] == 5:

                    self.inversions.update({index: choice(options)})

                else:

                    options.remove({2: second, 4: third, 7: first}[self.note_degree[self.canto[index][0]]])
                    self.inversions.update({index: choice(options)})
                
            elif current_chord == self.chord_name['subdominant']:  # if the current chord is iv or IV

                if (self.minor_degree_index[index]) or \
                   (previous_chord == self.chord_name['mediant']):

                    self.inversions.update({index: root})

                else:

                    self.inversions.update({index: choice([root, first])})
                    
            elif current_chord == self.chord_name['mediant']:  # if current chord is iii or III

                self.inversions.update({index: root})
            
            elif current_chord == self.chord_name['submediant']:  # if current chord is vi or VI

                self.inversions.update({index: root})
                
            elif current_chord == self.chord_name['subtonic']:  # if current chord is vii0 or VII

                self.inversions.update({index: first})
            
            elif current_chord == self.chord_name['supertonic'][0]:  # if current chord is ii or ii0

                if self.minor_degree_index[index]:

                    self.inversions.update({index: root})  # todo: check this

                elif self.modality == 'minor' and not self.minor_degree_index[index]:

                    self.inversions.update({index: first})

                else:

                    self.inversions.update({index: choice([root, first])})
                    
            elif current_chord == self.chord_name['supertonic'][1]:
                self.inversions.update({index: first})
                    
    def bassline_assign(self):
        
        self.bass.clear()
        while len(self.bass) != len(self.canto):
            index = len(self.bass)
            bass_octaves = sample([2, 3], k=2)

            if index == 0:

                self.bass.append(self.degree_note[self.chord_scale_degrees[self.chords[index]][self.inversions[index]]])
                for first_octave in bass_octaves:
                    if self.note_number[(self.bass[0], first_octave)] in self.bass_range:
                        self.bass[0] = (self.bass[0], first_octave)
                        break
            
            else:
                
                if self.secondary_dominant_index[index] == 'dominant':
                    current_chord = self.find_dominant(self.degree_note[self.chord_scale_degrees[self.chords[index+1]][0]])
                    self.bass.append(current_chord[self.inversions[index]])
                else:
                    self.bass.append(self.degree_note[self.chord_scale_degrees[self.chords[index]][self.inversions[index]]])
                options = [self.note_number[(self.bass[index], octave)] for octave in bass_octaves]
                for option in options:
                    if option not in self.bass_range:
                        options.remove(option)
                
                if (abs(self.note_number[self.bass[index-1]] - options[0])) in [5, 7]:
                    self.bass[index] = self.number_note[choice(options)]
                else:
                    intervals = {abs(self.note_number[self.bass[index-1]]-note): note for note in options}
                    
                    self.bass[index] = self.number_note[intervals[min(intervals)]]
                mistake_check = Mistake(self.canto[index - 1], self.canto[index], self.bass[index - 1], self.bass[index])
                interval_diff = abs(self.note_number[self.bass[index]] - self.note_number[self.bass[index-1]])
                                    
                if mistake_check.parallels() or mistake_check.voice_crossing() or (interval_diff in [6, 10, 11, 0, 9]):
                    self.bass.clear()
                    self.cadence_assign()
                    self.chord_assign()
                    self.inversion_assign()
                    if self.attempts == self.max_attempts:
                        raise Exception('Max Attempts Reached at Bassline Assign')
                    self.attempts += 1
                    
#                 elif abs(self.note_number[self.bass[note_index]] - self.note_number[self.bass[note_index]])

    def alto_tenor_assign(self):
        
        self.alto.clear()
        self.tenor.clear()
        
        if len(self.bass) == 0:
            return
        
        while len(self.alto) != len(self.canto):
            
            if len(self.bass) == 0:
                return
            
            index = len(self.alto)
            missing_voices = ['alto', 'tenor']
            
            if self.secondary_dominant_index[index] == 'dominant':
                missing_notes = self.find_dominant(self.degree_note[self.chord_scale_degrees[self.chords[index+1]][0]])
                missing_notes.remove(self.canto[index][0])
                missing_notes.remove(self.bass[index][0])
                combinations = {1: {'alto': missing_notes[0], 'tenor': missing_notes[1]},
                                2: {'alto': missing_notes[1], 'tenor': missing_notes[0]}}

                for attempt in sample([1, 2],k=2):
                    choice = combinations[attempt]

                    self.alto.append(self.closest_note('alto', choice['alto']))
                    self.tenor.append(self.closest_note('tenor', choice['tenor']))
                    if self.check_voices(index):
                        self.alto.pop()
                        self.tenor.pop()
                    else:
                        self.alto[index] = self.number_note[self.alto[index]]
                        self.tenor[index] = self.number_note[self.tenor[index]]
                        break

            else:  # if the chord is not a secondary dominant
                missing_notes = list(self.chord_scale_degrees[self.chords[index]])
                missing_notes.remove(self.note_degree[self.canto[index][0]])

                if self.note_degree[self.bass[index][0]] in missing_notes:
                    missing_notes.remove(self.note_degree[self.bass[index][0]])

                if len(missing_notes) == 1:
                    missing_options = {voice: self.closest(voice, missing_notes[0]) for voice in missing_voices}
                    for voice in missing_voices:
                        self.voice_ref[voice].append(missing_options[voice])
                        other_voice = missing_voices.copy()
                        other_voice.remove(voice)
                        if self.double(other_voice[0], index):
                            break
                        else:
                            self.voice_ref[voice].pop()

                elif len(missing_notes) == 2:
                    combinations = {1: {'alto': missing_notes[0], 'tenor': missing_notes[1]},
                                    2: {'alto': missing_notes[1], 'tenor': missing_notes[0]}}

                    for attempt in sample([1, 2], k=2):

                        selection = combinations[attempt]
                        self.voice_ref['alto'].append(self.closest('alto', selection['alto']))
                        self.voice_ref['tenor'].append(self.closest('tenor', selection['tenor']))
                        if self.check_voices(index):
                            self.alto.pop()
                            self.tenor.pop()
                        else:
                            break
                        
            if index == len(self.alto):  # trying again
                self.alto.clear()
                self.tenor.clear()
                self.cadence_assign()
                self.chord_assign()
                self.inversion_assign()
                self.bassline_assign()
                if self.attempts == self.max_attempts:
                    raise Exception('Max Attempts Reached at Alto Tenor Assign')
                self.attempts += 1

    def conversions(self):
        self.fourpart_numbers = [self.canto.copy(), self.alto.copy(), self.tenor.copy(), self.bass.copy()]
        for voice in self.fourpart_numbers:
            for index in range(len(voice)):
                voice[index] = note_index_conv(voice[index])

        fourpart = [self.canto, self.alto, self.tenor, self.bass]

        if self.modality == 'minor':

            for note_index in range(len(self.chords)):
                if (not self.minor_degree_index[note_index]) and \
                        self.note_degree.get(self.canto[note_index][0]) not in [6, 7] and \
                        self.chords[note_index] in ['v', 'v7', 'VII']:
                    self.minor_degree_index.update({note_index: True})

            augmented_chords = {'III': 'III+', 'iv': 'IV', 'v': 'V', 'v7': 'V7',
                                'VII': 'vii0', 'ii0': 'ii', 'ii*7': 'ii7'}
            for note_index in range(len(self.canto)):
                for voice in range(4):
                    if self.note_degree.get(fourpart[voice][note_index][0]) in [6, 7] and self.minor_degree_index[
                        note_index]:
                        fourpart[voice][note_index] = augment(fourpart[voice][note_index])[0]
                        self.fourpart_numbers[voice][note_index] += 1
                        try:
                            self.chords[note_index] = augmented_chords[self.chords[note_index]]
                        except:
                            pass

        for chord in range(len(self.chords)):
            if self.secondary_dominant_index[chord] == 'dominant':
                self.chords[chord] = 'V7/'

    def formating(self):

        self.fourpart_numbers = [self.canto.copy(), self.alto.copy(), self.tenor.copy(), self.bass.copy()]
        for voice in self.fourpart_numbers:
            for index in range(len(voice)):
                voice[index] = note_index_conv(voice[index])

        fourpart = [self.canto.copy(), self.alto.copy(), self.tenor.copy(), self.bass.copy()]
        phrase_format = ('{:'+str(len(self.tonic)+9+abs(self.transposition_degree))+'}')*len(self.alto)

        if self.modality == 'minor':
            
            for note_index in range(len(self.chords)):
                if (not self.minor_degree_index[note_index]) and \
                        self.note_degree.get(self.canto[note_index][0]) not in [6, 7] and \
                        self.chords[note_index] in ['v', 'v7', 'VII']:

                    self.minor_degree_index.update({note_index: True})
            
            augmented_chords = {'III': 'III+', 'iv': 'IV', 'v': 'V', 'v7': 'V7',
                                'VII': 'vii0', 'ii0': 'ii', 'ii*7': 'ii7'}

            for note_index in range(len(self.canto)):
                for voice in range(4):
                    if self.note_degree.get(fourpart[voice][note_index][0]) in [6, 7] and self.minor_degree_index.get(note_index):
                        fourpart[voice][note_index] = augment(fourpart[voice][note_index])[0]
                        self.fourpart_numbers[voice][note_index] += 1
                        try:
                            self.chords[note_index] = augmented_chords[self.chords[note_index]]
                        except:
                            pass
                        
        for chord in range(len(self.chords)):
            if self.secondary_dominant_index[chord] == 'dominant':
                self.chords[chord] = 'V7/'
        
        while self.transposition_needed and self.transposition_degree != 0:
            if self.transposition_degree > 0:
                for voice in fourpart:
                    for note in range(len(voice)):
                        voice[note] = augment(voice[note])[0]
                self.transposition_degree -= 1
            elif self.transposition_degree < 0:
                for voice in fourpart:
                    for note in range(len(voice)):
                        voice[note] = diminish(voice[note])[0]
                self.transposition_degree += 1

        for index in self.inversions:

            if self.chords[index][-1] == '7':
                self.chords[index] = self.chords[index][:-1]
                self.chords[index] += {0: '7', 1: '65', 2: '43', 3: '42'}[self.inversions[index]]
            elif self.chords[index][-1] == '/':
                self.chords[index] = self.chords[index][:-2]
                self.chords[index] += {0: '7/', 1: '65/', 2: '43/', 3: '42/'}[self.inversions[index]]
                self.chords[index] += self.chords[index+1]
            else:
                self.chords[index] += {0: '', 1: '6', 2: '64'}[self.inversions[index]]

        for voice in fourpart:
            for note in range(len(voice)):
                voice[note] = str(voice[note])
        print('Canto:', phrase_format.format(*fourpart[0]))
        print('Alto: ', phrase_format.format(*fourpart[1]))
        print('Tenor:', phrase_format.format(*fourpart[2]))
        print('Bass: ', phrase_format.format(*fourpart[3]))
        print('Chords: ', phrase_format.format(*self.chords))
        print('-'*(len(self.canto)*(len(fourpart[0][0])+4)))
