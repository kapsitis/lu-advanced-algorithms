from midiutil import MIDIFile
from midi2audio import FluidSynth
from pydub import AudioSegment
import opuslib

# Step 1: Create a MIDI File
def create_midi_file(filename):
    track = 0
    time = 0
    tempo = 120
    volume = 100

    midi_file = MIDIFile(1)
    midi_file.addTempo(track, time, tempo)

    scale = [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60]  # C major scale
    duration = [0.5] * 14 + [1.0]  # durations for each note

    for i, pitch in enumerate(scale):
        midi_file.addNote(track, 0, pitch, time, duration[i], volume)
        time += duration[i]

    with open(filename, "wb") as output_file:
        midi_file.writeFile(output_file)

# Step 2: Convert MIDI to WAV using FluidSynth
def midi_to_wav(midi_filename, wav_filename):
    fs = FluidSynth()
    fs.midi_to_audio(midi_filename, wav_filename)

# Step 3: Convert WAV to Opus
def wav_to_opus(wav_filename, opus_filename):
    # Load WAV file using pydub
    audio = AudioSegment.from_wav(wav_filename)

    # Export to Opus
    audio.export(opus_filename, format="opus")

# Main Execution
midi_filename = "c_major_scale.mid"
wav_filename = "c_major_scale.wav"
opus_filename = "c_major_scale.opus"

create_midi_file(midi_filename)
midi_to_wav(midi_filename, wav_filename)
wav_to_opus(wav_filename, opus_filename)

print(f"Opus file saved as: {opus_filename}")




# Koda piemērs
# ~~~~~~~~~~~~~~~


# - `midiutil`: `pip install midiutil`
# - `midi2audio`: `pip install midi2audio`
# - `pydub`: `pip install pydub`
# - `opuslib`: Requires additional setup and might not support direct file handling.

