import numpy as np

from src.lab_generative_audio.synthesis import (
    SAMPLE_RATE,
    apply_envelope,
    sine_tone,
)


def generate_completion_earcon() -> np.ndarray:
    first_note = sine_tone(
        frequency=523.25,  # C5
        duration=0.25,
        amplitude=0.3,
    )

    second_note = sine_tone(
        frequency=659.25,  # E5
        duration=0.35,
        amplitude=0.3,
    )

    first_note = apply_envelope(
        first_note,
        attack=0.02,
        release=0.08,
    )

    second_note = apply_envelope(
        second_note,
        attack=0.02,
        release=0.10,
    )

    silence = np.zeros(
        int(SAMPLE_RATE * 0.04)
    )

    return np.concatenate(
        [
            first_note,
            silence,
            second_note,
        ]
    )

def generate_cloud_completion_earcon() -> np.ndarray:
    first_note = sine_tone(
        frequency=392.00,  # G4
        duration=0.30,
        amplitude=0.24,
    )

    second_note = sine_tone(
        frequency=523.25,  # C5
        duration=0.42,
        amplitude=0.22,
    )

    first_note = apply_envelope(
        first_note,
        attack=0.04,
        release=0.10,
    )

    second_note = apply_envelope(
        second_note,
        attack=0.05,
        release=0.16,
    )

    silence = np.zeros(
        int(SAMPLE_RATE * 0.06)
    )

    return np.concatenate(
        [
            first_note,
            silence,
            second_note,
        ]
    )