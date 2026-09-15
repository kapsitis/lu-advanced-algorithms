import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# Define the note frequencies for one octave (C major scale)
note_frequencies = {
    'c4': 261.63,  # Middle C
    'd': 293.66,
    'e': 329.63,
    'f': 349.23,
    'g': 392.00,
    'a': 440.00,
    'b': 493.88,
    'c5': 523.25  # C an octave above Middle C
}

# Define the order of the notes to play
note_sequence = ['c4', 'd', 'e', 'f', 'g', 'a', 'b', 'c5', 'b', 'a', 'g', 'f', 'e', 'd', 'c4']

# Create an empty audio segment to append notes
scale_audio = AudioSegment.silent(duration=0)

# Generate each note and append it to the scale_audio
duration = 250  # duration of each note in milliseconds (eighth note)
for note in note_sequence:
    sine_wave = Sine(note_frequencies[note])
    note_audio = sine_wave.to_audio_segment(duration=duration)
    scale_audio += note_audio

# Save the audio to a WAV file
wav_file = "C_major_scale.wav"
scale_audio.export(wav_file, format="wav")

# Now, convert the WAV file to an Opus file using pydub
opus_file = "C_major_scale.opus"
scale_audio.export(opus_file, format="opus")

print(f"Opus-encoded audio file created: {opus_file}")