from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

Talisman(app)

# Access token e ID de usuario de la cuenta de Instagram
ACCESS_TOKEN = 'IGQWRNbDQzZAXZApakJmX0xRcmVudU5idC1xZAmFrTXdJeXlSbUlWMm1jZAzRVMFJ6VkYzSnRuSmVPN3YtUWdpcGU1RkdiMzkzeUpSTGFoeTJ5MlZAHOURRYmNIalNmMEp0LUhFejNHLVJXaFBHUGtrTUx5eWhhT0V2OU0ZD'
USER_ID = '1249292085'

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API funcionando. Usa /api/reels para obtener reels."})

@app.route('/api/reels', methods=['GET'])
def get_latest_reels():
    """
    Este endpoint obtiene los últimos reels (imágenes/videos) de la cuenta de Instagram usando la Graph API.
    """
    try:
        # URL de la API para obtener medios
        url = f'https://graph.instagram.com/{USER_ID}/media'
        params = {
            'fields': 'id,media_type,media_url,thumbnail_url,permalink',
            'access_token': ACCESS_TOKEN
        }

        # Llama a la API de Instagram
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return jsonify({'error': response.json()}), response.status_code

        # Procesa la respuesta
        data = response.json().get('data', [])
        reels_data = [
            {
                "video_url": item.get('media_url') if item['media_type'] == 'VIDEO' else None,
                "thumbnail_url": item.get('thumbnail_url') or item.get('media_url'),
                "post_url": item.get('permalink'),
            }
            for item in data if item['media_type'] in ['VIDEO', 'IMAGE']
        ]

        # Devuelve solo los primeros 8 reels
        return jsonify(reels_data[:8])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
