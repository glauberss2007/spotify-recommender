import requests
import json
import sys

def recommend_songs(songs_list, server_url):
    """Envia requisição para o servidor de recomendação"""
    payload = {
        'songs': songs_list
    }
    
    try:
        response = requests.post(
            f"{server_url}/api/recommend",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'HTTP {response.status_code}: {response.text}'}
    
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def main():
    if len(sys.argv) < 3:
        print("Uso: python test_client.py <server_url> <song1> [song2] ...")
        print("Exemplo: python test_client.py http://localhost:30502 'Yesterday' 'Bohemian Rhapsody'")
        return
    
    server_url = sys.argv[1]
    songs = sys.argv[2:]
    
    print(f"Enviando requisição para: {server_url}")
    print(f"Músicas de input: {songs}")
    
    result = recommend_songs(songs, server_url)
    
    print("\nResposta do servidor:")
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
