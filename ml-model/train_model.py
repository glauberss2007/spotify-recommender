import pandas as pd
import pickle
from fpgrowth_py import fpgrowth
import os

def load_dataset(dataset_path):
    """Carrega o dataset e prepara os dados para FIM"""
    print(f"Carregando dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Agrupar músicas por playlist (assumindo que cada linha é uma música em uma playlist)
    playlists = df.groupby('playlist_id')['track_name'].apply(list).tolist()
    
    return playlists

def generate_rules(playlists, min_support=0.01, min_confidence=0.5):
    """Gera regras de associação usando FP-Growth"""
    print("Gerando regras de associação...")
    
    # Converter para lista de listas (formato esperado pelo fpgrowth)
    transaction_list = [list(set(playlist)) for playlist in playlists if len(playlist) > 1]
    
    # Calcular suporte mínimo baseado no número de transações
    min_sup_count = int(len(transaction_list) * min_support)
    
    # Gerar itemsets frequentes e regras
    freqItemSet, rules = fpgrowth(transaction_list, minSupRatio=min_support, minConf=min_confidence)
    
    print(f"Generated {len(rules)} rules")
    return rules

def save_model(rules, model_path):
    """Salva o modelo gerado"""
    with open(model_path, 'wb') as f:
        pickle.dump(rules, f)
    print(f"Modelo salvo em: {model_path}")

def main():
    # Configurações
    DATASET_PATH = os.getenv('DATASET_PATH', '/home/datasets/spotify/2023_spotify_ds1.csv')
    MODEL_PATH = os.getenv('MODEL_PATH', '/shared/model.pickle')
    MIN_SUPPORT = float(os.getenv('MIN_SUPPORT', '0.01'))
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.5'))
    
    # Executar pipeline
    playlists = load_dataset(DATASET_PATH)
    rules = generate_rules(playlists, MIN_SUPPORT, MIN_CONFIDENCE)
    save_model(rules, MODEL_PATH)

if __name__ == "__main__":
    main()
