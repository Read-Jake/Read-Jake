"""
this will take the generated fourpart and play it with piano sounds
"""

import pygame
import time
from testing import *

pygame.mixer.init()

# harmony = test_22
tempo = 90


def play(voices):
    """
    this will play the fourpart
    parameter is voices, a list of strings that include a combination of "soprano", "alto", "tenor", "bass", or "all"
    """
    voice_num = {'soprano': 0, 'alto': 1, 'tenor': 2, 'bass': 3}
    if len(voices) == 1 and voices[0] != 'all':
        for index in range(len(harmony.canto)):
            play_note = str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[0]]][index]][1]) + '-'
            play_note += str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[0]]][index]][0].lower())
            play_note = play_note.replace('#', 's')
            play_note = "C:\\Users\\Jake\\Documents\\Python Files\\Four Part Project\\samples\\" + play_note + '.wav'

            pygame.mixer.Channel(0).play(pygame.mixer.Sound(file=play_note))
            time.sleep(60/tempo)

    elif len(voices) == 2:

        for index in range(len(harmony.canto)):

            note_one, note_two = '', ''
            notes = [note_one, note_two]

            for voice in range(2):
                notes[voice] = str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][1]) + '-'
                notes[voice] += str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][0].lower())
                notes[voice] = notes[voice].replace('#', 's')
                notes[voice] = "C:\\Users\\Jake\\Documents\\Python Files\\Four Part Project\\samples\\" + notes[
                    voice] + '.wav'

            note_one, note_two = notes[0], notes[1]
            sound_one = pygame.mixer.Sound(file=note_one)
            sound_two = pygame.mixer.Sound(file=note_two)
            pygame.mixer.Channel(0).play(sound_one)
            pygame.mixer.Channel(1).play(sound_two)
            time.sleep(60/tempo)

    elif len(voices) == 3:
        for index in range(len(harmony.canto)):

            note_one, note_two, note_three = '', '', ''
            notes = [note_one, note_two, note_three]

            for voice in range(3):
                notes[voice] = str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][1]) + '-'
                notes[voice] += str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][0].lower())
                notes[voice] = notes[voice].replace('#', 's')
                notes[voice] = "C:\\Users\\Jake\\Documents\\Python Files\\Four Part Project\\samples\\" + notes[
                    voice] + '.wav'

            note_one, note_two, note_three = notes[0], notes[1], notes[2]
            sound_one = pygame.mixer.Sound(file=note_one)
            sound_two = pygame.mixer.Sound(file=note_two)
            sound_three = pygame.mixer.Sound(file=note_three)
            pygame.mixer.Channel(0).play(sound_one)
            pygame.mixer.Channel(1).play(sound_two)
            pygame.mixer.Channel(2).play(sound_three)
            time.sleep(60/tempo)

    elif len(voices) == 4 or voices[0] == 'all':
        voices = ['soprano', 'alto', 'tenor', 'bass']
        for index in range(len(harmony.canto)):

            note_one, note_two, note_three, note_four = '', '', '', ''
            notes = [note_one, note_two, note_three, note_four]

            for voice in range(4):
                notes[voice] = str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][1]) + '-'
                notes[voice] += str(number_note_sharp[harmony.fourpart_numbers[voice_num[voices[voice]]][index]][0].lower())
                notes[voice] = notes[voice].replace('#', 's')
                notes[voice] = "C:\\Users\\Jake\\Documents\\Python Files\\Four Part Project\\samples\\" + notes[
                    voice] + '.wav'

            note_one, note_two, note_three, note_four = notes[0], notes[1], notes[2], notes[3]
            sound_one = pygame.mixer.Sound(file=note_one)
            sound_two = pygame.mixer.Sound(file=note_two)
            sound_three = pygame.mixer.Sound(file=note_three)
            sound_four = pygame.mixer.Sound(file=note_four)
            pygame.mixer.Channel(0).play(sound_one)
            pygame.mixer.Channel(1).play(sound_two)
            pygame.mixer.Channel(2).play(sound_three)
            pygame.mixer.Channel(3).play(sound_four)
            time.sleep(60/tempo)


if __name__ == "__main__":
    while True:
        playback = input("Select a voice to play:").strip().split()
        playback.sort()
        if playback == ['end']:
            break
        elif playback == ['all']:
            play(playback)
        elif all(list(i in ['soprano', 'alto', 'tenor', 'bass'] for i in playback)):
            play(playback)
        elif playback == ['rerun']:
            harmony.__init__(harmony.canto, harmony.key)
        elif playback == ['tempo']:
            tempo = int(input("    New tempo:"))
        else:
            print('Not a valid voice')
