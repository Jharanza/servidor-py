from flask import Flask, jsonify
from flask_cors import CORS
from instaloader import Instaloader, Profile
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5173", "http://localhost:5173"]}})

JSON_FILE_PATH = 'reels_data_json'

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
            with open(JSON_FILE_PATH, 'r') as file:
                reels_data = json.load(file)
            return jsonify(reels_data)
            
        L = Instaloader()
        profile = Profile.from_username(L.context, 'hotelzamora')

        reels_data = []
        
        for post in profile.get_posts():
            if post.is_video:
                reel_info = {
                    "video_url": post.video_url,  # URL del video
                    "thumbnail_url": f"https://instagram.com/p/{post.shortcode}/media/?size=t",  # Generar la URL del thumbnail
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",  # URL del reel
                }
                reels_data.append(reel_info)

            if len(reels_data) >= 6:
                break
            
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(reels_data, file)
            
        return jsonify(reels_data, file)
 
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({ 'error': str(e) })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
