from flask import Flask, request, jsonify
import pickle
import os
import hashlib
import time
from datetime import datetime

app = Flask(__name__)

class RecommendationModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.rules = None
        self.last_hash = None
        self.load_model()
    
    def get_file_hash(self):
        """Calcula hash do arquivo do modelo para detectar mudanças"""
        if not os.path.exists(self.model_path):
            return None
        with open(self.model_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def load_model(self):
        """Carrega o modelo se houve mudanças"""
        current_hash = self.get_file_hash()
        
        if current_hash and current_hash != self.last_hash:
            try:
                with open(self.model_path, 'rb') as f:
                    self.rules = pickle.load(f)
                self.last_hash = current_hash
                print(f"Modelo carregado/atualizado em {datetime.now()}")
                return True
            except Exception as e:
                print(f"Erro ao carregar modelo: {e}")
                return False
        return False
    
    def get_recommendations(self, input_songs, max_recommendations=10):
        """Gera recomendações baseadas nas regras"""
        if not self.rules:
            return []
        
        recommendations = {}
        input_set = set(input_songs)
        
        for rule in self.rules:
            antecedent = set(rule[0])
            consequent = set(rule[1])
            confidence = rule[2]
            
            # Se o antecedente está contido nas músicas de input
            if antecedent.issubset(input_set):
                for song in consequent:
                    if song not in input_set:  # Não recomendar músicas já conhecidas
                        if song not in recommendations:
                            recommendations[song] = 0
                        recommendations[song] += confidence
        
        # Ordenar por confiança e retornar top N
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [song for song, conf in sorted_recs[:max_recommendations]]

# Inicializar o modelo
model = RecommendationModel('/shared/model.pickle')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Endpoint para recomendações"""
    # Verificar e carregar atualizações do modelo
    model.load_model()
    
    # Processar request
    data = request.get_json(force=True)
    input_songs = data.get('songs', [])
    
    if not input_songs:
        return jsonify({'error': 'Lista de músicas vazia'}), 400
    
    # Gerar recomendações
    recommendations = model.get_recommendations(input_songs)
    
    # Preparar resposta
    response = {
        'songs': recommendations,
        'version': '1.0.0',
        'model_date': datetime.now().isoformat(),
        'input_songs_count': len(input_songs)
    }
    
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy', 'model_loaded': model.rules is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
