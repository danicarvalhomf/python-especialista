from src.lab_generative_audio.synthesis import baby_rattle


def generate_button_press():
    return baby_rattle(
        duration=0.16,
        amplitude=0.045,
    )