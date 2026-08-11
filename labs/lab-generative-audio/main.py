from pathlib import Path

from src.lab_generative_audio.earcons.completion import (
    generate_cloud_completion_earcon,
    generate_completion_earcon,
)
from src.lab_generative_audio.earcons.interaction import (
    generate_button_press,
)
from src.lab_generative_audio.synthesis import save_wav


OUTPUT_DIR = Path("outputs/earcons")


sun_completion = generate_completion_earcon()

save_wav(
    sun_completion,
    OUTPUT_DIR / "sun" / "completion_v01.wav",
)


cloud_completion = generate_cloud_completion_earcon()

save_wav(
    cloud_completion,
    OUTPUT_DIR / "cloud" / "completion_v01.wav",
)


button_press = generate_button_press()

save_wav(
    button_press,
    OUTPUT_DIR / "ui" / "button_press_v01.wav",
)