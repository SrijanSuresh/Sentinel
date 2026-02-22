from flask import Flask, render_template_string, jsonify, request 
from components.header import HEADER
from components.controls import CONTROLS
from components.monitor import MONITOR
from components.logs import LOGS
import socket, os

app = Flask(__name__)
SOCKET_PATH = "/tmp/sentinel.socket"

def talk_to_sentinel(cmd):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.send(cmd.encode())
        res = client.recv(1024).decode()
        client.close()
        return res
    except: return "Error"

@app.route('/')
def index():
    # reading the external script logic
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, 'script.js')
    with open(script_path, 'r') as f:
        js_logic = f.read()

    # using a standard string (NO 'f' at the start)
    html_template = '''
    <!DOCTYPE html>
    <html class="dark">
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Sentinel C2</title>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex items-center justify-center font-sans">
        <div class="bg-slate-800 p-8 rounded-3xl shadow-2xl border border-slate-700 w-[28rem]">
            {HEADER}
            {CONTROLS}
            {MONITOR}
            <button onclick="kill()" class="w-full bg-red-600 hover:bg-red-700 py-4 rounded-2xl font-black text-sm tracking-widest transition-all active:scale-95">EMERGENCY TERMINATE</button>
            {LOGS}
        </div>
        <script>{JS_LOGIC}</script>
    </body>
    </html>
    '''

    # 3. Inject all components and the JS logic at once
    return render_template_string(html_template.format(
        HEADER=HEADER, 
        CONTROLS=CONTROLS, 
        MONITOR=MONITOR, 
        LOGS=LOGS,
        JS_LOGIC=js_logic
    ))
    
    
@app.route('/run')
def run_cmd():
    cmd = request.args.get('c')
    return talk_to_sentinel(f"run:{cmd}")

@app.route('/status')
def status(): return talk_to_sentinel("status")
@app.route('/kill')
def kill(): return talk_to_sentinel("stop")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)