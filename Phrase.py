"""
new phrase
"""
from Theory import *


class phrase:
    
    def __init__(self, canto, key):
        
        self.canto = canto
        self.key = key
        self.tonic = key[:-5].strip()
        self.modality = key[-5:]

        self.modulation_needed = {}
        self.modulation_dest = self.key
        self.transposition_needed = False
        self.transposition_degree = 0

        self.transposition_check()
        self.minor_degree_index = {}
        self.secondary_dominant_index = {}
        
        if self.tonic in sharp_keys[self.modality]:
            self.number_note = number_note_sharp
            self.note_number = note_sharp_number
        else:
            self.number_note = number_note_flat
            self.note_number = note_flat_number
            
        self.note_degree = self.scale_dict(self.key)
        self.degree_note = self.scale_dict_reverse()
        self.modulation_check()
        
        for index in range(len(self.canto)):
            self.minor_degree_index.update({index: False})
            self.secondary_dominant_index.update({index: False})
        
        if self.modality == 'major':
            self.chord_scale_degrees = major_chord
        else:
            self.chord_scale_degrees = minor_chord
            self.minor_scale_conversion()
            
        self.secondary_dominant_conversion()
        self.chord_name = chord_name[self.modality]
        self.name_chord = name_chord[self.modality]
        
        # ranges specified in the New Harvard Dictionary of Music
        self.bass_range = range(self.note_number[('E', 2)], self.note_number[('C', 4)]+1)
        self.canto_range = range(self.note_number[('C', 4)], self.note_number[('A', 5)]+1)
        self.alto_range = range(self.note_number[('F', 3)], self.note_number[('D', 5)]+1)
        self.tenor_range = range(self.note_number[('B', 2)], self.note_number[('G', 4)]+1)
        
        self.attempts = 0
        self.max_attempts = len(self.canto)*10000
        self.possibilities = []
        self.inversion_possibilities = {}
        self.secondary_inversions = secondary_inversion_options[self.modality]
        
        self.chords = []
        self.inversions = {}
        self.bass = []
        self.alto = []
        self.tenor = []

        self.fourpart_numbers = []
        self.voice_ref = {'alto': self.alto, 'tenor': self.tenor, 'canto': self.canto, 'bass': self.bass}

    def modulation_check(self):  # todo
        if self.canto[-2][0] not in self.note_degree.keys():
            pass


    def note_conversion(self, note):  # this might be redundant
        """
        returns the note number if tuple is passed.
        returns the number note if int is passed
        """
        if type(note) == int:
            return self.number_note[note]
        elif type(note) == tuple:
            if note[0] in notes_sharp:
                return note_sharp_number[note]
            elif note[0] in notes_flat:
                return note_flat_number[note]
            elif note[0][-1] == '#':
                diff = 0
                while note[0] not in self.note_degree.keys():
                    note = diminish(note)[0]
                    diff += 1
                return self.note_number[note] + diff
            elif note[0][-1] == 'b':
                diff = 0
                while note[0] not in self.note_degree.keys():
                    note = augment(note)[0]
                    diff += 1
                return self.note_number[note] - diff
        else:
            raise 'Invalid note_index parameter'

    def scale_dict(self, key):
        """
        returns a dictionary that links each note to a specific scale degree
        """
        number = 1
        increment = 0
        major_mode = [0, 2, 2, 1, 2, 2, 2]
        minor_mode = [0, 2, 1, 2, 2, 1, 2]
        degree = {}
        mode = {'major': [0, 2, 2, 1, 2, 2, 2], 'minor': [0, 2, 1, 2, 2, 1, 2]}
        
        for num in mode[key[-5:]]:
            increment += num
            degree.update({self.number_note[self.note_number[key[:-6], 1] + increment][0]: number})
            number += 1
        
        return degree

    def scale_dict_reverse(self):
        reverse_dict = {}
        for key, value in self.note_degree.items():
            reverse_dict.update({value:key})
        return reverse_dict

    def transposition_check(self):
        '''
        Checks to see if the key of the CF has too many sharps or flats in it for the code to recognise.
        If it does, this function uses the augment or diminish functions to remove the flats/sharps
        into something more readable
        '''


        while self.tonic not in {'major': [*sharp_majors, *flat_majors],
                                 'minor': [*sharp_minors, *flat_minors]}[self.modality]:

            if self.tonic[-1] == '#':
                self.tonic = diminish((self.tonic, 3))[0][0]
                for note in range(len(self.canto)):
                    self.canto[note] = diminish(self.canto[note])[0]
                self.transposition_degree += 1
                
            elif self.tonic[-1] == 'b':
                self.tonic = augment((self.tonic, 3))[0][0]
                for note in range(len(self.canto)):
                    self.canto[note] = augment(self.canto[note])[0]
                self.transposition_degree -= 1
                
        if self.transposition_degree != 0:
            self.transposition_needed = True
        
        self.key = self.tonic + ' ' + self.modality
        
    def minor_scale_conversion(self):  # still need to include
                
        for index in range(len(self.canto)):
            if self.canto[index][0] not in list(self.note_degree.keys()):
                if self.note_degree.get(diminish(self.canto[index])[0][0]) in [6, 7]:
                    index_degree = self.note_degree[diminish(self.canto[index])[0][0]]
                    self.canto[index] = diminish(self.canto[index])[0]
                    self.minor_degree_index.update({index:True})
        
    def check_voices(self, index):
                
        all_checks = []
        canto1 = self.canto[index-1]
        canto2 = self.canto[index]
        bass1 = self.bass[index-1]
        bass2 = self.bass[index]
        
        try:
            alto1 = self.alto[index-1]
            alto2 = self.alto[index]
            check1 = Mistake(canto1, canto2, alto1, alto2)
            check2 = Mistake(alto1, alto2, bass1, bass2)
            all_checks.append(check1.parallels())
            all_checks.append(check1.voice_crossing())
            all_checks.append(check2.parallels())
            all_checks.append(check2.voice_crossing())
        except:
            pass
        try:
            tenor1 = self.tenor[index-1]
            tenor2 = self.tenor[index]
            check3 = Mistake(canto1, canto2, tenor1, tenor2)
            check4 = Mistake(tenor1, tenor2, bass1, bass2)
            all_checks.append(check3.parallels())
            all_checks.append(check3.voice_crossing())
            all_checks.append(check4.parallels())
            all_checks.append(check4.voice_crossing())
        except:
            pass
        try:
            check5 = Mistake(alto1, alto2, tenor1, tenor2)
            all_checks.append(check5.parallels())
            all_checks.append(check5.voice_crossing())
        except:
            pass

        if any(all_checks):
            return True
        else:
            return False
        
    def closest(self, voice, scale_degree):
        try:
            starting_note = self.note_number[self.voice_ref[voice][-1]]
        except:
            starting_note = {'alto': 36+pos(self.note_number[self.canto[len(self.alto)]]-8-36),
                             'tenor': 29+pos(self.note_number[self.canto[len(self.alto)]]-12-29)
                             }[voice]
        fixed_note = starting_note
        closest_notes = {}
        increment = 1
        while len(closest_notes) != 2:
            try:
                if self.note_degree[self.number_note[starting_note][0]] == scale_degree:
                    closest_notes.update({abs(fixed_note-starting_note):self.number_note[starting_note]})
            except:
                pass
            starting_note += increment
            increment = -increment
            if increment < 0:
                increment -= 1
            else:
                increment += 1
        return closest_notes[min(closest_notes)]

    def closest_note (self, voice, note):
        """
        does the same as self.closest, but this takes a note name as a parameter
        instead of a scale degree
        """
        if len(self.voice_ref[voice]) > 0:
            starting_note = self.note_number[self.voice_ref[voice][-1]]
        else:
            starting_note = {'alto': 36 + pos(self.note_number[self.canto[len(self.alto)]] - 8 - 36),
                             'tenor': 29 + pos(self.note_number[self.canto[len(self.alto)]] - 12 - 29)
                             }[voice]

        oct = self.number_note[starting_note][1]
        targets = [note_index_conv((note, oct)), note_index_conv((note, oct+1)), note_index_conv((note, oct-1))]
        targets = {abs(interval-starting_note):interval for interval in targets}

        return targets[min(targets)]

    
    def double(self, voice, note_index):
        achieved = False
        major_minor_options = {
            'major': {
                'I': [1, 5, 3], 'ii': [4, 2, 6], 'iii': [3], 'IV': [4, 1, 6],
                'V': [5, 2], 'vi': [6], 'vii0': [2, 4]},
            'minor': {
                'i': [1, 5, 3], 'ii0': [4, 6], 'III': [3], 'iv': [4, 1, 6],
                'v': [5, 2], 'VI': [6], 'VII': [2, 4]}
                                }
        double_options = major_minor_options[self.modality][self.chords[note_index]]
        for note in double_options:
            self.voice_ref[voice].append(self.closest(voice,note))
            if self.check_voices(note_index):
                self.voice_ref[voice].pop()
            else:
                achieved = True
                break
        return achieved
    
    def secondary_dominant_conversion (self):
        
        for index in range(len(self.canto)):
            if self.canto[index][0] not in self.note_degree.keys():
                self.secondary_dominant_index.update({index: 'dominant'})
                self.secondary_dominant_index.update({index+1: 'tonic'})
                
#         for index in self.secondary_dominant_index:
#             if self.secondary_dominant_index[index] != False:
#                 self.canto.remove(self.canto[index])

    def interval(self, note_1, note_2):  # todo update this function
        return abs(self.note_number[note_1]-self.note_number[note_2])
    
    def find_dominant(self, note):
    
        chord = {1: [5, 7, 2, 4], 2: [6, 1, 3, 5], 3: [7, 2, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 6, 1],
                 6: [3, 5, 7, 2], 7: [4, 6, 1, 3]}[self.note_degree[note]]
        augment_diminish_index = {'major': {1: {}, 2: {1: 'augment'}, 3: {2: 'augment', 4: 'augment'},
                                            4: {7: 'diminish'}, 5: {4: 'augment'}, 6: {5:'augment'},
                                            7: {4: 'augment', 6: 'augment', 1: 'augment'}
                                            },
                                  'minor': {1: {7: 'augment'}, 2: {6: 'augment', 1: 'augment', 3: 'augment'},
                                            3: {}, 4: {3: 'augment'}, 5: {4: 'augment', 6: 'augment'},
                                            6: {2: 'diminish'}, 7: {6: 'augment'}
                                            }
                                   }
        
        dominant_chord = []

        for index in chord:
            
            if augment_diminish_index[self.modality][self.note_degree[note]].get(index) == 'augment':
                dominant_chord.append(augment((self.degree_note[index],4))[0][0])
            elif augment_diminish_index[self.modality][self.note_degree[note]].get(index) == 'diminish':
                dominant_chord.append(diminish((self.degree_note[index],4))[0][0])
            else:
                dominant_chord.append(self.degree_note[index])
        
        return dominant_chord


#                 index_degree = self.note_degree[diminish(self.canto[index])[0]]
#                 if index_degree in [6,7]:
#                     self.canto[index] = diminish(self.canto[index])[0]
#                     self.minor_degree_index.update({index:index_degree})
                    
# tests
if __name__ == '__main__':
    test_1 = phrase([('F#', 4), ('E', 4), ('F#', 4)], 'F# minor')
    print(test_1.note_degree.keys())
    for note in test_1.note_degree.keys():
        print(note, ':', test_1.find_dominant(note))
# print (test_1.canto)
# print (test_1.minor_degree_index)
