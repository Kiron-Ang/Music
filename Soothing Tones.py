import math
import wave
import os

# List of piano note frequencies (C4, C4#, D4, D4#, etc.)
piano_notes = [
    261.63,  # C4
    277.18,  # C4#
    293.66,  # D4
    311.13,  # D4#
    329.63,  # E4
    349.23,  # F4
    369.99,  # F4#
    392.00,  # G4
    415.30,  # G4#
    440.00,  # A4
    466.16,  # A4#
    493.88,  # B4
    523.25   # C5
]

# Mapping of note names to their indices in the piano_notes list
note_indices = {
    'C4': 0,
    'C4#': 1,
    'D4': 2,
    'D4#': 3,
    'E4': 4,
    'F4': 5,
    'F4#': 6,
    'G4': 7,
    'G4#': 8,
    'A4': 9,
    'A4#': 10,
    'B4': 11,
    'C5': 12
}

# Create a calm and soothing chord progression (e.g., C, G, Am, F)
# These chords are often used in soothing music.
song = [
    ('C4', 2),  # Whole note C4
    ('E4', 2),  # Whole note E4
    ('G4', 2),  # Whole note G4
    ('C5', 2),  # Whole note C5
    ('A4', 2),  # Whole note A4
    ('C5', 2),  # Whole note C5
    ('E4', 2),  # Whole note E4
    ('G4', 2),  # Whole note G4
    ('F4', 2),  # Whole note F4
    ('A4', 2),  # Whole note A4
    ('C5', 2),  # Whole note C5
]

# Parameters
sample_rate = 44100  # Samples per second (standard for audio)
amplitude = 16000  # Volume of the sound
channels = 1  # Mono Audio
sampwidth = 2  # Number of bytes per sample

# Get the script name without extension and use it for the output filename
script_name = os.path.splitext(os.path.basename(__file__))[0]
output_filename = f"{script_name}.wav"

# Function to generate a sine wave for a given frequency and duration with crossfade
def generate_note(frequency, duration):
    num_samples = int(sample_rate * duration)
    fade_duration = 0.05  # Fade duration in seconds (50ms for smooth transition)
    fade_samples = int(sample_rate * fade_duration)
    samples = bytearray()  # Using bytearray for efficient byte manipulation
    
    for i in range(num_samples):
        # Apply fade-in and fade-out
        fade_in = min(i / fade_samples, 1.0) if i < fade_samples else 1.0
        fade_out = min((num_samples - i) / fade_samples, 1.0) if i > num_samples - fade_samples else 1.0
        amplitude_adjusted = amplitude * fade_in * fade_out
        
        sample_value = int(amplitude_adjusted * math.sin(2 * math.pi * frequency * (i / sample_rate)))
        # Convert sample_value to bytes in little-endian (16-bit signed integer)
        samples.extend(sample_value.to_bytes(sampwidth, byteorder='little', signed=True))
    
    return bytes(samples)

# Create the wave file
with wave.open(output_filename, 'w') as wave_file:
    # Set the parameters for the WAV file
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(sampwidth)
    wave_file.setframerate(sample_rate)
    
    # Repeat the song to make it last for 3 minutes (180 seconds)
    total_duration = 180  # Target song length in seconds
    song_duration = sum(note_duration for _, note_duration in song)
    repeat_count = int(total_duration / song_duration)
    
    # Generate and write the song notes to the file for the required duration
    for _ in range(repeat_count):
        for note, note_duration in song:
            # Get the frequency for the note using the note_indices to map note to its index
            frequency = piano_notes[note_indices[note]]
            wave_file.writeframes(generate_note(frequency, note_duration))

print(f"Song saved to {output_filename}")