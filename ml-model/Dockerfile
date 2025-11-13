FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train_model.py .

# Variáveis de ambiente com valores padrão
ENV DATASET_PATH=/datasets/2023_spotify_ds1.csv
ENV MODEL_PATH=/shared/model.pickle
ENV MIN_SUPPORT=0.01
ENV MIN_CONFIDENCE=0.5

CMD ["python", "train_model.py"]
