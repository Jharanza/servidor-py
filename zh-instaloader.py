from flask import Flask, jsonify
from flask_cors import CORS
from instaloader import Instaloader, Profile
import json
import os
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

JSON_FILE_PATH = '/reels_data_json'

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API funcionando. Usa /api/reels/<username> para obtener reels."})


@app.route('/favicon.ico')
def favicon():
    return '', 204 

@app.route('/api/reels', methods=['GET'])
def get_latest_reels():
    try:
        if os.path.exists(JSON_FILE_PATH):
            os.remove(JSON_FILE_PATH)
            
        profile = getProfileInstagram('hotelzamora')

        reels_data = []
        
        for post in profile.get_posts():
            if post.is_video:
                reel_info = {
                    "video_url": post.video_url,  # URL del video
                    "thumbnail_url": f"https://instagram.com/p/{post.shortcode}/media/?size=t",  # Generar la URL del thumbnail
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",  # URL del reel
                }
                reels_data.append(reel_info)

            if len(reels_data) >= 8:
                break
            
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(reels_data, file)
        print(f"Archivo JSON creado: {os.path.exists(JSON_FILE_PATH)}")
        return jsonify(reels_data)

    except Exception as e:
        print(f"Error al procesar los reels: {e}")
        return jsonify({ 'error': str(e) })
    
@app.route('/api/proxy', methods=['GET'])
def proxy():
    """
    This endpoint act as a proxy 
    """
    target_url = requests.args.get('url')
    
    if not target_url:
        return jsonify({ 'error': 'Missing a the url param'}), 400
    
    try:
        # Realiza la solicitud al servidor externo
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
        }
        response = requests.get(target_url, headers=headers)
        
        return jsonify({
            'status': response.status_code,
            'headers': dict(response.headers),
            'body': response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def getProfileInstagram(username):
    try:
        L = Instaloader()
        return Profile.from_username(L.context, username)
    except Exception as e:
        print(f"Error al obtener el perfil: {e}")
        raise e

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
