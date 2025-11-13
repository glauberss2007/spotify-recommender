import requests
import time
import json
from datetime import datetime

def continuous_test(server_url, test_songs, duration=300):
    """Testa continuamente o serviço durante um período"""
    print(f"Iniciando teste contínuo por {duration} segundos")
    print(f"Servidor: {server_url}")
    print(f"Músicas de teste: {test_songs}")
    
    start_time = time.time()
    requests_count = 0
    successful_requests = 0
    downtime_start = None
    downtime_periods = []
    
    while time.time() - start_time < duration:
        try:
            request_start = time.time()
            response = requests.post(
                f"{server_url}/api/recommend",
                json={'songs': test_songs},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            request_time = time.time() - request_start
            
            if response.status_code == 200:
                successful_requests += 1
                data = response.json()
                print(f"✅ Request {requests_count}: {request_time:.2f}s - "
                      f"Version: {data.get('version')} - "
                      f"Recommendations: {len(data.get('songs', []))}")
                
                # Se estava em downtime, registrar período
                if downtime_start:
                    downtime_periods.append(time.time() - downtime_start)
                    downtime_start = None
                    
            else:
                print(f"❌ Request {requests_count}: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request {requests_count}: Erro - {e}")
            # Iniciar ou continuar período de downtime
            if not downtime_start:
                downtime_start = time.time()
                
        requests_count += 1
        time.sleep(5)  # Esperar 5 segundos entre requests
    
    # Calcular métricas
    total_time = time.time() - start_time
    success_rate = (successful_requests / requests_count) * 100
    total_downtime = sum(downtime_periods) if downtime_periods else 0
    
    print(f"\n--- RESULTADOS DO TESTE ---")
    print(f"Total de requests: {requests_count}")
    print(f"Requests bem-sucedidos: {successful_requests}")
    print(f"Taxa de sucesso: {success_rate:.2f}%")
    print(f"Tempo total de downtime: {total_downtime:.2f}s")
    print(f"Disponibilidade: {((total_time - total_downtime) / total_time) * 100:.2f}%")

if __name__ == '__main__':
    # Configurar conforme seu ambiente
    SERVER_URL = "http://seu-endereço:30502"
    TEST_SONGS = ["Yesterday", "Bohemian Rhapsody", "Imagine"]
    
    continuous_test(SERVER_URL, TEST_SONGS, duration=300)  # 5 minutos
