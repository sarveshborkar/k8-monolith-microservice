from flask import Flask, request, redirect, render_template, jsonify
import string
import random
import redis

app = Flask(__name__)

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Generate random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Route to handle URL shortening
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate a unique short code
    short_code = generate_short_code()
    while redis_client.exists(f'url:{short_code}'):
        short_code = generate_short_code()

    # Save to Redis
    redis_client.set(f'url:{short_code}', original_url)
    redis_client.set(f'count:{short_code}', 0)

    # Return shortened URL
    short_url = request.host_url + short_code
    return jsonify({'short_url': short_url})

# Route to handle redirection and click tracking
@app.route('/<short_code>')
def redirect_url(short_code):
    original_url = redis_client.get(f'url:{short_code}')
    if original_url:
        # Increment click count
        redis_client.incr(f'count:{short_code}')
        return redirect(original_url)
    else:
        return jsonify({'error': 'URL not found'}), 404

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
