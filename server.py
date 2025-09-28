from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage
rooms = {}
messages = {}

print("🚀 Starting GameZone Chat Server...")

# Serve frontend
@app.route('/')
def serve_index():
    return render_template('index.html')

# Health check
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running',
        'message': 'GameZone Server online!',
        'timestamp': datetime.now().isoformat()
    })

# Create a new room
@app.route('/create_invite', methods=['POST'])
def create_invite():
    try:
        data = request.get_json() or {}
        username = data.get('username', 'Player')
        room_id = str(uuid.uuid4())[:8].upper()

        rooms[room_id] = {
            'members': [username],
            'host': username,
            'created_at': time.time()
        }
        messages[room_id] = []

        print(f"🎮 New room created: {room_id} by {username}")
        return jsonify({'success': True, 'roomId': room_id, 'username': username})

    except Exception as e:
        print(f"❌ Error creating room: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Join an existing room
@app.route('/room/<room_id>/join', methods=['POST'])
def join_room(room_id):
    try:
        data = request.get_json() or {}
        username = data.get('username', 'Player')

        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404

        if username not in rooms[room_id]['members']:
            rooms[room_id]['members'].append(username)

        # Add system message
        messages[room_id].append({
            'username': 'System',
            'message': f'{username} joined the room',
            'timestamp': time.time(),
            'type': 'system'
        })

        print(f"👤 {username} joined room {room_id}")
        return jsonify({
            'success': True,
            'message': f'Joined room {room_id}',
            'members': rooms[room_id]['members'],
            'member_count': len(rooms[room_id]['members'])
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Send message
@app.route('/room/<room_id>/message', methods=['POST'])
def send_message(room_id):
    try:
        data = request.get_json() or {}
        username = data.get('username', 'Player')
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400

        if room_id not in messages:
            messages[room_id] = []

        message_data = {
            'username': username,
            'message': message,
            'timestamp': time.time(),
            'type': 'text'
        }

        messages[room_id].append(message_data)
        if len(messages[room_id]) > 100:
            messages[room_id] = messages[room_id][-100:]

        print(f"💬 {username} in {room_id}: {message}")
        return jsonify({'success': True, 'message': 'Message sent'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get last 50 messages
@app.route('/room/<room_id>/messages')
def get_messages(room_id):
    try:
        if room_id not in messages:
            return jsonify({'success': True, 'messages': []})
        return jsonify({'success': True, 'messages': messages[room_id][-50:]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Get members
@app.route('/room/<room_id>/members')
def get_members(room_id):
    try:
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        return jsonify({
            'success': True,
            'members': rooms[room_id]['members'],
            'member_count': len(rooms[room_id]['members'])
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
