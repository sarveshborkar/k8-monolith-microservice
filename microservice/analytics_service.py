from flask import Flask, redirect, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

@app.route('/redirect/<short_code>')
def redirect_url(short_code):
    original_url = redis_client.get(f"url:{short_code}")
    if original_url:
        redis_client.incr(f"count:{short_code}")
        return redirect(original_url)
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
