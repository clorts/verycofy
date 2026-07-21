from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configura o banco de dados SQLite com tabela de mensagens e de usuários
def init_db():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    # Tabela de mensagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    # Tabela de contas (usuários)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, message FROM messages')
    messages = cursor.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if username:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        # Salva a conta no banco de dados se ela já não existir
        try:
            cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
            conn.commit()
        except Exception as e:
            print(e)
        conn.close()
    return redirect(url_for('index'))

@app.route('/send', methods=['POST'])
def send():
    username = request.form.get('username', '').strip()
    message = request.form.get('message', '').strip()
    if username and message:
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        # Garante que o usuário está registrado na tabela de usuários também
        cursor.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
        # Salva a mensagem
        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
