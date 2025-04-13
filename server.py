from flask import Flask, request, jsonify
import sqlite3
import time
import uuid
app = Flask(__name__)
Folder = '.'
Database = Folder + '/RSC.db'
Logfile = Folder + '/RSC.log'
conn = sqlite3.connect(Database)
cursor = conn.cursor()
LOGS = False
def log(text, ):
    global LOGS, Logfile
    if LOGS == False:
        return
    with open(Logfile, 'a') as l:
        l.write(f'{text}\n')
log(f"{time.time()}  --  Starting")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    uniqid TEXT NOT NULL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

""")
conn.commit()
@app.route('/user/create', methods=['POST'])
def usercreate():
    try:
        conn = sqlite3.connect(Database)
        cursor = conn.cursor()
        
        if 'username' not in request.form:
            return jsonify({"error": "username is required"}), 400
        
        username = request.form['username']
        uniqid = str(uuid.uuid4())
        
        cursor.execute('INSERT INTO users (username, uniqid) VALUES (?, ?);', (username, uniqid))
        conn.commit()

        return jsonify({"code": 200, "username": username, "uniqid": uniqid})
    except Exception as e:
        return jsonify({"code": 500, "message": "internal server error"})
        log(e)


@app.route('/message/send', methods=["POST"])
def msgsend():
    try:
        conn = sqlite3.connect(Database)
        cursor = conn.cursor()
        uniqid = request.form['uniqid']
        contents = request.form['contents']
        cursor.execute('SELECT username FROM users WHERE uniqid = ?', (uniqid,))
        username = cursor.fetchone()[0]
        if not username:
            return jsonify({"code": 404, "message": "username not found for uniqid " + uniqid})
        if not contents:
            return jsonify({"code": 404, "message": "contents not found"})
        cursor.execute('INSERT INTO messages (username, content) VALUES (?, ?)', (username, contents))
        conn.commit()
        conn.close()
        return jsonify({'code': 200})
    except Exception as e:
        log(e)
        return jsonify({"code": 500, "message": "internal server error"})

@app.route('/message/get')
def getmsgs():
    try:
        conn = sqlite3.connect(Database)
        cursor = conn.cursor()

        cursor.execute('SELECT username, content, timestamp FROM messages ORDER BY timestamp ASC')
        rows = cursor.fetchall()
        conn.close()

        messages = []
        for row in rows:
            messages.append({
                "username": row[0],
                "contents": row[1],
                "timestamp": row[2]
            })

        return jsonify({"code": 200, "messages": messages})
    except Exception as e:
        log(e)
        return jsonify({"code": 500, "message": "internal server error"})
@app.route('/node/info')
def nodeinfo():
    try:
        return jsonify({
            "name": "RSC Instance",
            "version": 1.0,
            "admin": "pda@juanvel400.xyz"
        })
    except Exception as e:
        log(e)
        return jsonify({"code": 500, "message": "internal server error"})
@app.route('/')
def main():

    return """<html>
        <head>
            <title>RSC</title>
        </head>
        <body>
            <h1>RSC</h1>
            <p>If you are seeing this, RSC is installed and this is a new node</p>
            <footer>
                <hr>
                <p>Copyright &copy; 2025 juanvel400   -   <a href='/node/info'>View this node info</a></p>
            </footer>
        </body>
    </html>"""
@app.route('/user/list')
def userlist():
    conn = sqlite3.connect(Database)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"code": 200, "users": users})


if __name__ == '__main__':
    app.run(debug=True, port=1819)