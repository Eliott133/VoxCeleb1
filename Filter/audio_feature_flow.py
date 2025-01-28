import pyworld as pw
import librosa
import numpy as np
import os
import pickle
import tgt
from multiprocessing import Pool
import time

# Paths
PATH_AUDIO = '/lium/home/fsaget/2425-PROJETM1/resources/data/VoxCeleb1/wav/wav'
PATH_ALIGNMENTS = '/lium/home/fsaget/2425-PROJETM1/resources/data/VoxCeleb1/alignments/en'

# Utility Functions
def get_audio_files(path_audio):
    """Retrieve all .wav files in the given directory."""
    wav_files = []
    for root, _, files in os.walk(path_audio):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

def get_alignment_file(audio_file):
    """Get the corresponding TextGrid alignment file for a given audio file."""
    parts = audio_file.split(os.sep)
    id_person, identifiant, numero_audio = parts[-3], parts[-2], os.path.splitext(parts[-1])[0]
    alignment_file = os.path.join(PATH_ALIGNMENTS, f"{id_person}_{identifiant}_{numero_audio}.TextGrid")
    return alignment_file

# Feature Extraction Functions
def extract_f0_and_energy(file_path):
    """Extract F0, energy, and duration features from an audio file."""
    try:
        y, sr = librosa.load(file_path, sr=None)
        y = y.astype(np.float64)
        duration = len(y) / sr

        # Energy features
        energy = librosa.feature.rms(y=y)[0]
        mean_energy = np.mean(energy)
        std_energy = np.std(energy)

        # F0 features
        _f0, _time = pw.dio(y, sr)
        f0 = pw.stonemask(y, _f0, _time, sr)
        f0_valid = f0[f0 > 0]

        mean_f0 = np.mean(f0_valid) if len(f0_valid) > 0 else 0
        mean_log10_f0 = np.mean(np.log10(f0_valid)) if len(f0_valid) > 0 else 0
        std_f0 = np.std(np.log10(f0_valid)) if len(f0_valid) > 0 else 0

        return duration, mean_f0, mean_log10_f0, std_f0, mean_energy, std_energy

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, 0, 0, 0, 0, 0

def calculate_flows(alignment_file):
    """Calculate both phonemic and word flows from a TextGrid alignment file."""
    try:
        tg = tgt.io.read_textgrid(alignment_file)
        
        # Phonemes
        phones_tier = tg.get_tier_by_name("phones")
        phoneme_count = len(phones_tier)
        phoneme_duration = sum(interval.end_time - interval.start_time for interval in phones_tier)

        flow_phonemic = phoneme_count / phoneme_duration if phoneme_duration > 0 else 0

        # Words
        words_tier = tg.get_tier_by_name("words")
        word_count = len(words_tier)
        word_duration = sum(interval.end_time - interval.start_time for interval in words_tier)

        flow_word = word_count / word_duration if word_duration > 0 else 0

        return flow_phonemic, flow_word

    except Exception as e:
        print(f"Error processing {alignment_file}: {e}")
        return 0, 0


def process_audio_file(audio_file):
    """Process a single audio file to extract all features including phonemic flow."""
    alignment_file = get_alignment_file(audio_file)
    
    # Extract features
    duration, mean_f0, mean_log10_f0, std_f0, mean_energy, std_energy = extract_f0_and_energy(audio_file)
    flow_phonemic, flow_word = calculate_flows(alignment_file)

    return {
        "file_path": audio_file,
        "duration": duration,
        "mean_f0": mean_f0,
        "mean_log10_f0": mean_log10_f0,
        "std_f0": std_f0,
        "mean_energy": mean_energy,
        "std_energy": std_energy,
        "flow_phonemic": flow_phonemic,
        "flow_word": flow_word
    }

# Parallel Processing
def process_files_in_parallel(audio_files, num_processes=4):
    """Process multiple audio files in parallel."""
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_audio_file, audio_files)
    return results

# Main Function
def main():
    audio_files = get_audio_files(PATH_AUDIO)

    # Measure time for processing
    start_time = time.time()
    results = process_files_in_parallel(audio_files, num_processes=4)
    end_time = time.time()

    print(f"Processing completed in {(end_time - start_time) / 60:.2f} minutes")


    # Save results to a pickle file
    output_file = "audio_features_with_flow.pkl"
    with open(output_file, "wb") as f:
        pickle.dump(results, f)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
