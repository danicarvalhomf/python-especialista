import numpy as np


SAMPLE_RATE = 44_100


def sine_tone(
    frequency: float,
    duration: float,
    amplitude: float = 0.3,
) -> np.ndarray:
    samples = int(SAMPLE_RATE * duration)
    time = np.arange(samples) / SAMPLE_RATE

    signal = amplitude * np.sin(
        2 * np.pi * frequency * time
    )

    return signal


def apply_envelope(
    signal: np.ndarray,
    attack: float = 0.02,
    release: float = 0.08,
) -> np.ndarray:
    envelope = np.ones(len(signal))

    attack_samples = min(
        int(SAMPLE_RATE * attack),
        len(signal),
    )

    release_samples = min(
        int(SAMPLE_RATE * release),
        len(signal),
    )

    envelope[:attack_samples] = np.linspace(
        0,
        1,
        attack_samples,
    )

    envelope[-release_samples:] = np.linspace(
        1,
        0,
        release_samples,
    )

    return signal * envelope