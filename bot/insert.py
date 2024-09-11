import json
import firebase_admin
from firebase_admin import credentials, db
import os
import re

# Caminho para o arquivo de credenciais e JSON
cred_path = './blockchain-games-brasil-firebase-adminsdk-23egt-18c921f9a4.json'
json_path = './table_data.json'

# Função para inicializar o Firebase
def initialize_firebase():
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://blockchain-games-brasil-default-rtdb.firebaseio.com/'
        })
        print("Firebase inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")

# Função para carregar dados do JSON
def load_json_data():
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Arquivo JSON não encontrado: {json_path}")
    
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar o JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o arquivo JSON: {e}")

# Função para escapar caracteres especiais
def escape_special_characters(text):
    return re.sub(r'[.#$[\]]', '_', text)

# Função para inserir ou atualizar dados no Firebase
def upsert_data_to_firebase(data):
    try:
        ref = db.reference('player')
        for item in data:
            if len(item) != 4:
                print(f"Formato de item inválido: {item}")
                continue
            
            chave, nome, vip, pts = item
            escaped_nome = escape_special_characters(nome)
            
            # Consultar os jogadores existentes pelo nome
            existing_players = ref.order_by_child('nome').equal_to(escaped_nome).get()
            
            if existing_players:
                # Atualizar os pontos do jogador existente
                for key in existing_players:
                    ref.child(key).update({'pts': pts})
                print(f"Jogador com nome {nome} atualizado com novos pontos.")
            else:
                # Inserir um novo jogador
                dados = {
                    'id': chave,
                    'nome': nome,
                    'vip': vip,
                    'pts': pts
                }
                ref.push(dados)
                print(f"Jogador com nome {nome} inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir ou atualizar dados no Firebase: {e}")

# Execução do script
if __name__ == "__main__":
    initialize_firebase()
    try:
        dados_json = load_json_data()
        upsert_data_to_firebase(dados_json)
    except Exception as e:
        print(f"Erro geral: {e}")
