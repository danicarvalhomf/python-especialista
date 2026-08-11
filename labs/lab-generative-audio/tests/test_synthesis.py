import numpy as np

from src.lab_generative_audio.synthesis import (
    SAMPLE_RATE,
    apply_envelope,
    sine_tone,
)


def test_sine_tone_has_expected_length():
    signal = sine_tone(
        frequency=440.0,
        duration=1.0,
    )

    assert len(signal) == SAMPLE_RATE


def test_sine_tone_is_bounded():
    signal = sine_tone(
        frequency=440.0,
        duration=1.0,
        amplitude=0.3,
    )

    assert np.max(np.abs(signal)) <= 0.3


def test_envelope_starts_and_ends_near_zero():
    signal = sine_tone(
        frequency=440.0,
        duration=1.0,
    )

    enveloped = apply_envelope(signal)

    assert np.isclose(enveloped[0], 0.0)
    assert np.isclose(enveloped[-1], 0.0)