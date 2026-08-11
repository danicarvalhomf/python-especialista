import numpy as np
from pathlib import Path
from scipy.io.wavfile import write
from scipy.signal import butter, sosfilt

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


def save_wav(
    signal: np.ndarray,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    normalized = np.clip(signal, -1.0, 1.0)

    audio = (normalized * 32767).astype(np.int16)

    write(
        output_path,
        SAMPLE_RATE,
        audio,
    )


def soft_tone(
    frequency: float,
    duration: float,
    amplitude: float = 0.18,
) -> np.ndarray:
    samples = int(SAMPLE_RATE * duration)
    time = np.arange(samples) / SAMPLE_RATE

    fundamental = np.sin(
        2 * np.pi * frequency * time
    )

    harmonic = 0.20 * np.sin(
        2 * np.pi * frequency * 2 * time
    )

    signal = fundamental + harmonic

    signal = signal / np.max(
        np.abs(signal)
    )

    return amplitude * signal


def soft_pluck(
    frequency: float = 330.0,
    duration: float = 0.14,
    amplitude: float = 0.10,
) -> np.ndarray:
    samples = int(SAMPLE_RATE * duration)
    time = np.arange(samples) / SAMPLE_RATE

    fundamental = np.sin(
        2 * np.pi * frequency * time
    )

    warm_component = 0.25 * np.sin(
        2 * np.pi * frequency * 1.5 * time
    )

    signal = fundamental + warm_component

    decay = np.exp(
        -18 * time
    )

    signal = signal * decay

    signal = signal / np.max(
        np.abs(signal)
    )

    return amplitude * signal

def soft_plack(
    frequency: float = 260.0,
    duration: float = 0.24,
    amplitude: float = 0.07,
) -> np.ndarray:
    samples = int(SAMPLE_RATE * duration)
    time = np.arange(samples) / SAMPLE_RATE

    fundamental = np.sin(
        2 * np.pi * frequency * time
    )

    fifth = 0.18 * np.sin(
        2 * np.pi * frequency * 1.5 * time
    )

    signal = fundamental + fifth

    attack_samples = int(SAMPLE_RATE * 0.025)

    attack = np.linspace(
        0.0,
        1.0,
        attack_samples,
    )

    decay_samples = samples - attack_samples

    decay = np.linspace(
        1.0,
        0.0,
        decay_samples,
    ) ** 1.8

    envelope = np.concatenate(
        [
            attack,
            decay,
        ]
    )

    signal *= envelope

    signal = signal / np.max(
        np.abs(signal)
    )

    return amplitude * signal


from scipy.signal import butter, sosfilt


def baby_rattle(
    duration: float = 0.16,
    amplitude: float = 0.045,
) -> np.ndarray:
    samples = int(SAMPLE_RATE * duration)

    rng = np.random.default_rng(seed=42)

    noise = rng.normal(
        0.0,
        1.0,
        samples,
    )

    # Remove graves excessivos e agudos ásperos.
    sos = butter(
        2,
        [700, 2200],
        btype="bandpass",
        fs=SAMPLE_RATE,
        output="sos",
    )

    filtered_noise = sosfilt(
        sos,
        noise,
    )

    filtered_noise /= np.max(
        np.abs(filtered_noise)
    )

    time = np.linspace(
        0.0,
        duration,
        samples,
        endpoint=False,
    )

    # Pequenas pulsações simulam o movimento dos grânulos.
    movement = (
        0.55
        + 0.25 * np.sin(2 * np.pi * 18 * time)
        + 0.15 * np.sin(2 * np.pi * 27 * time)
    )

    # Envelope macio: entra rápido, mas não "estala".
    envelope = np.sin(
        np.linspace(
            0,
            np.pi,
            samples,
        )
    ) ** 1.2

    signal = (
        filtered_noise
        * movement
        * envelope
    )

    signal /= np.max(
        np.abs(signal)
    )

    return amplitude * signal