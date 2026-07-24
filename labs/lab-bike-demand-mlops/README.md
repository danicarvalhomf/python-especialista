# Bike Demand MLOps

## Objetivo
O objetivo do projeto é fazer todo o processo de MLOps para o dataset de demandas por bicicleta, com o dataset disponível em https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset. 

## Arquitetura
A arquitetura separa dados brutos, dos modelos, notebooks e relatórios. Os recursos utilizados na aplicação também separa responsabilidade de código para conexão e consulta ao banco de dados PostgreSQL, ingestão de dados, dashboard, ingestão de dados, relatório e treinamento do modelo de machine learning.

## Running the project

Start PostgreSQL

```bash
docker compose up -d
```

Run tests

```bash
uv run pytest
```

Load raw dataset

```bash
uv run python -m src.ingestion.load_raw_dataset
```

## Tecnologias

## Estrutura

## Roadmap

- [ ] Ingestão
- [ ] PostgreSQL
- [ ] Feature Engineering
- [ ] Treinamento
- [ ] API
- [ ] Dashboard
- [ ] Docker
- [ ] Docker Compose
- [ ] Monitoramento