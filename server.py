from flask import Flask, request, jsonify, send_file
from rembg import remove
import io
import base64
from PIL import Image

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    try:
        # Получаем изображение из запроса
        file = request.files['image']
        
        # Читаем изображение
        input_image = Image.open(file.stream)
        
        # Удаляем фон с помощью rembg
        output_image = remove(input_image)
        
        # Конвертируем результат в bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Кодируем в base64 для отправки на клиент
        encoded = base64.b64encode(img_byte_arr).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{encoded}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)