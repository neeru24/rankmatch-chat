# Lobby Chat Test Project

## Backend (Flask + Socket.IO)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Runs on http://localhost:5000

## Frontend (React)
```bash
cd frontend
npx create-react-app .
npm install socket.io-client react-router-dom
npm start
```
Runs on http://localhost:3000

## Usage
1. Create invite: POST to http://localhost:5000/create_invite
   ```bash
   curl -X POST http://localhost:5000/create_invite -H "Content-Type: application/json" -d '{"username":"player1"}'
   ```
   Response: `{ "roomId": "xxxxxxx" }`

2. Open two browser tabs:
   - http://localhost:3000/invite/xxxxxxx
   - http://localhost:3000/invite/xxxxxxx

3. Type messages to chat in real time.
```
