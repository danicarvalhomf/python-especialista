import platform
import sys

import pandas as pd
import psutil
from rich import print

def main():
    print("[bold cyan] Ambiente Python moderno funcionando! [/bold cyan]")
    print(f"Python: {sys.version}")
    print(f"Sistema: {platform.system()}")
    print(f"Memória RAM total: {psutil.virtual_memory().total / 1024 ** 3:.2f} GB")

    df = pd.DataFrame({
        "ferramenta": ["uv", "venv", "pyprojet.toml"],
        "papel": [
            "Gerenciar dependências e ambientes virtuais",
            "Isolar pacotes do projeto",
            "Declarar configuração moderna do projeto",
        ]
    })

    print(df)


if __name__ == "__main__":
    main()