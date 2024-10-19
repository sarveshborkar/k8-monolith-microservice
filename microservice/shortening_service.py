from flask import Flask, request, jsonify
import redis
import string
import random
import os

app = Flask(__name__)
redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_code = generate_short_code()
    while redis_client.exists(f"url:{short_code}"):
        short_code = generate_short_code()

    redis_client.set(f"url:{short_code}", original_url)
    redis_client.set(f"count:{short_code}", 0)

    # Assuming "analytics-service" is the Kubernetes service name for the analytics service
    short_url = f"http://analytics-service/redirect/{short_code}"
    return jsonify({'short_url': short_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)