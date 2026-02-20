from flask import Flask, render_template_string, jsonify, request 
import socket

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
    return render_template_string('''
    <!DOCTYPE html>
    <html class="dark">
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Sentinel C2</title>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex items-center justify-center font-sans">
        <div class="bg-slate-800 p-8 rounded-3xl shadow-2xl border border-slate-700 w-[28rem]">
            <h1 class="text-3xl font-black mb-6 text-blue-400 text-center tracking-tighter">SENTINEL COMMAND</h1>
            
            <div class="mb-8">
                <label class="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-2 block">New Task</label>
                <div class="flex gap-2">
                    <input id="cmd-input" type="text" placeholder="CMD HERE" 
                           class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-blue-500 transition-colors">
                    <button onclick="runCmd()" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-xl text-sm font-bold transition-all active:scale-95">RUN</button>
                </div>
            </div>

            <div class="mb-8">
                <div class="flex justify-between text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-2">
                    <span>Memory Enforcement</span>
                    <span id="mem-text">0MB / 512MB</span>
                </div>
                <div class="w-full bg-slate-900 rounded-full h-3 border border-slate-700 overflow-hidden">
                    <div id="mem-bar" class="bg-blue-500 h-full transition-all duration-700 ease-in-out" style="width: 0%"></div>
                </div>
            </div>

            <button onclick="kill()" class="w-full bg-red-600 hover:bg-red-700 py-4 rounded-2xl font-black text-sm tracking-widest transition-all transform active:scale-95 shadow-lg shadow-red-900/20">
                EMERGENCY TERMINATE
            </button>
        </div>

        <script>
            async function runCmd() {
                const cmd = document.getElementById('cmd-input').value;
                const res = await fetch(`/run?c=${encodeURIComponent(cmd)}`);
                alert("Launch Status: " + await res.text());
            }

            setInterval(async () => {
                try {
                    const res = await fetch('/status');
                    const mem = await res.text();
                    const percent = Math.min((parseFloat(mem) / 512) * 100, 100);
                    document.getElementById('mem-text').innerText = mem + "MB / 512MB";
                    document.getElementById('mem-bar').style.width = percent + "%";
                    document.getElementById('mem-bar').className = percent > 80 ? "bg-red-500 h-full transition-all duration-700" : "bg-blue-500 h-full transition-all duration-700";
                } catch (e) {}
            }, 2000);

            async function kill() { await fetch('/kill'); }
        </script>
    </body>
    </html>
    ''')

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