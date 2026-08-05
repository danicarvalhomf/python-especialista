# Python Especialista

Repositório central dos experimentos e projetos práticos desenvolvidos por Daniela Carvalho, reunindo tanto o blog **Engenharia dos Fluxos** quanto laboratórios técnicos (`labs/`) de engenharia de dados, MLOps, APIs e containers.

- **Repositório principal**: https://github.com/danicarvalhomf/python-especialista/tree/main
- **Blog (Engenharia dos Fluxos)**: https://danicarvalhomf.github.io/python-especialista
- **Laboratórios (labs)**: https://github.com/danicarvalhomf/python-especialista/tree/main/labs

## Estrutura do repositório

```
.
├── blog/       # Fontes Quarto (.qmd) do blog "Engenharia dos Fluxos"
├── docs/       # Site publicado (GitHub Pages) gerado a partir do blog
└── labs/       # Laboratórios práticos de Python (um projeto por pasta)
```

## Blog — Engenharia dos Fluxos

O blog é construído com [Quarto](https://quarto.org/) e publicado via GitHub Pages em https://danicarvalhomf.github.io/python-especialista.

Ele reúne artigos sobre Python, engenharia de software, dados, DevOps, IA e a relação entre comunicação e sistemas complexos. Os artigos publicados até o momento:

| Post | Tema |
| --- | --- |
| [001 — Projeto Python: Explorando sistemas complexos](blog/posts/001-projeto-python/index.qmd) | Introdução ao projeto e à motivação por trás do blog |
| [002 — A metamorfose do desenvolvimento de aplicações em Python: Docker e Containers](blog/posts/002-docker-python/index.qmd) | Primeiros passos com Docker aplicados a Python |
| [003 — Controlando a metamorfose do desenvolvimento e da disponibilização de conteúdo com uso de container](blog/posts/003-docker-container/index.qmd) | Uso de containers para disponibilizar aplicações Python, com referência ao laboratório `lab-dashboard-cycling` |

O código-fonte do site está em [blog/](blog/) (arquivos `.qmd`, configuração em [blog/_quarto.yml](blog/_quarto.yml)) e o site renderizado é publicado em [docs/](docs/).

## Laboratórios (`labs/`)

Cada laboratório é um projeto Python independente, com seu próprio `pyproject.toml` e gerenciado via [uv](https://docs.astral.sh/uv/). Veja em https://github.com/danicarvalhomf/python-especialista/tree/main/labs.

| Laboratório | Descrição | Principais tecnologias |
| --- | --- | --- |
| [lab-ambiente-python](labs/lab-ambiente-python/) | Laboratório introdutório sobre configuração de um ambiente Python moderno (gerenciamento de dependências e ambientes virtuais com `uv`) | Python, uv, pandas, psutil, rich |
| [lab-docker-python](labs/lab-docker-python/) | API FastAPI simples empacotada em container, primeiros passos com Docker aplicado a aplicações Python | Python, FastAPI, uvicorn, Docker |
| [lab-dashboard-cycling](labs/lab-dashboard-cycling/) | Dashboard interativo de condições climáticas para ciclismo, com dados da API Open-Meteo e fallback local | Python, Vizro, Plotly, Docker, Open-Meteo API |
| [lab-bike-demand-mlops](labs/lab-bike-demand-mlops/) | Pipeline completo de MLOps para previsão de demanda de bicicletas (ingestão, feature engineering, treinamento, API de predição e dashboard de monitoramento) | Python, FastAPI, PostgreSQL, SQLAlchemy, scikit-learn, Vizro, Docker Compose, pytest |

### Detalhes por laboratório

- **lab-ambiente-python**: script de exemplo (`main.py`) que valida a instalação do ambiente, exibindo versão do Python, sistema operacional, memória disponível e um resumo das ferramentas usadas (`uv`, `venv`, `pyproject.toml`).
- **lab-docker-python**: expõe uma API FastAPI (`GET /`, `GET /health`) e um `Dockerfile` baseado em `python:3.12-slim` + `uv`, demonstrando o empacotamento de uma aplicação Python em container.
- **lab-dashboard-cycling**: dashboard Vizro que consome a API [Open-Meteo](https://open-meteo.com/) para exibir previsões do tempo relevantes para ciclismo, com filtros de cidade e data, retry automático e fallback via snapshot local (`weather_snapshot.csv`). Deploy de demonstração em https://cycling-weather-dashboard.onrender.com.
- **lab-bike-demand-mlops**: projeto mais completo do repositório, cobrindo todo o ciclo de MLOps sobre o [dataset de demanda de bicicletas](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) — ingestão para PostgreSQL, engenharia de features (codificações cíclicas de tempo), treinamento e avaliação de modelo (`HistGradientBoostingRegressor`), API de predição em FastAPI e dashboard de monitoramento em Vizro, tudo orquestrado com Docker Compose e testado com pytest.

## Como executar um laboratório

Cada laboratório é autocontido. De forma geral:

```bash
cd labs/<nome-do-lab>
uv sync
uv run python main.py   # ou o comando específico descrito no README do laboratório
```

Consulte o `README.md` de cada pasta em `labs/` para instruções detalhadas (variáveis de ambiente, Docker Compose, testes, etc.).

## Sobre a autora

Daniela Carvalho atua na área de dados e tecnologia, com graduação em Comunicação Social (Publicidade e Propaganda) e em Análise e Desenvolvimento de Sistemas, mestrado em Multimeios, doutorado em Artes e pós-doutorado em Inteligência Artificial. Mais detalhes na página [Sobre](blog/about.qmd) do blog e no [Currículo Lattes](http://lattes.cnpq.br/6174708363093351).
