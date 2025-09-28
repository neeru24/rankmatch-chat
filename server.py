from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import time
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
rooms = {}
users = {}
messages = {}

print("🚀 Starting Simple GameZone Chat Server...")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running',
        'message': 'Simple GameZone Server is online!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/create_invite', methods=['POST'])
def create_invite():
    try:
        data = request.get_json() or {}
        username = data.get('username', 'Player')
        room_id = str(uuid.uuid4())[:8].upper()
        
        rooms[room_id] = {
            'members': [username],
            'host': username,
            'created_at': time.time(),
            'host_name': username
        }
        
        messages[room_id] = []
        
        print(f"🎮 New room created: {room_id} by {username}")
        
        return jsonify({
            'success': True,
            'roomId': room_id,
            'message': 'Room created successfully!',
            'username': username
        })
        
    except Exception as e:
        print(f"❌ Error creating room: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/room/<room_id>/join', methods=['POST'])
def join_room(room_id):
    try:
        data = request.get_json() or {}
        username = data.get('username', 'Player')
        
        if room_id not in rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        
        if username not in rooms[room_id]['members']:
            rooms[room_id]['members'].append(username)
        
        # Add join message
        if room_id in messages:
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
        
        # Keep only last 100 messages
        if len(messages[room_id]) > 100:
            messages[room_id] = messages[room_id][-100:]
        
        print(f"💬 {username} in {room_id}: {message}")
        
        return jsonify({
            'success': True,
            'message': 'Message sent'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/room/<room_id>/messages')
def get_messages(room_id):
    try:
        if room_id not in messages:
            return jsonify({'success': True, 'messages': []})
        
        return jsonify({
            'success': True,
            'messages': messages[room_id][-50:]  # Last 50 messages
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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

if __name__ == '__main__':
    print("🎮 =========================================")
    print("🎮     Simple GameZone Server Ready!")
    print("🎮 =========================================")
    print("📍 Local: http://localhost:5000")
    print("🔧 No WebSockets - Simple HTTP API")
    print("🎮 =========================================")
    
    app.run(host='0.0.0.0', port=5000, debug=True)