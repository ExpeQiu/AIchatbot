from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
from .models.conversation import DatabaseManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class WebServer:
    def __init__(self):
        self.db = DatabaseManager()
        
    def add_conversation(self, user_input: str, bot_response: str):
        """添加新的对话记录"""
        conversation = self.db.add_conversation(user_input, bot_response)
        # 通过WebSocket发送更新
        socketio.emit('new_conversation', conversation)

    def start(self, host='0.0.0.0', port=5000):
        """启动Web服务器"""
        def run_server():
            socketio.run(app, host=host, port=port)
            
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

# Flask路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/conversations')
def get_conversations():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    offset = (page - 1) * limit
    return jsonify(web_server.db.get_conversations(limit=limit, offset=offset))

@app.route('/api/search')
def search_conversations():
    query = request.args.get('q', '')
    return jsonify(web_server.db.search_conversations(query))

# 创建全局WebServer实例
web_server = WebServer() 