document.addEventListener('DOMContentLoaded', () => {
    logEvent("JS Bridge Connected: Sentinel C2 is online.");
});

// 1. Helper for logging events to the UI
function logEvent(msg, type = "info") {
    const log = document.getElementById('event-log');
    if (!log) return;
    const entry = document.createElement('div');
    const color = type === "error" ? "text-red-400" : (type === "success" ? "text-green-400" : "text-slate-400");
    entry.className = color;
    entry.innerText = `> ${new Date().toLocaleTimeString()}: ${msg}`;
    log.prepend(entry);
}

// 2. Task Management Functions
async function runCmd() {
    const cmd = document.getElementById('cmd-input').value;
    if (!cmd) return;
    logEvent(`Dispatching: ${cmd}`);
    const res = await fetch(`/run?c=${encodeURIComponent(cmd)}`);
    const status = await res.text();
    logEvent(`Guardian: ${status}`, status.includes("Error") ? "error" : "success");
}

function preset(cmd) {
    document.getElementById('cmd-input').value = cmd;
    logEvent(`Preset loaded: ${cmd}`);
}

async function kill() { 
    logEvent("!!! EMERGENCY TERMINATION ISSUED !!!", "error");
    await fetch('/kill'); 
}

// 3. Real-time Telemetry Loop
setInterval(async () => {
    try {
        const res = await fetch('/status');
        const mem = await res.text();
        const memVal = parseFloat(mem);
        
        if (isNaN(memVal)) return;

        const percent = Math.min((memVal / 512) * 100, 100);
        const bar = document.getElementById('mem-bar');
        const text = document.getElementById('mem-text');
        
        text.innerText = memVal.toFixed(2) + "MB / 512MB";
        bar.style.width = percent + "%";

        if (percent > 90) {
            bar.className = "bg-red-500 h-full transition-all duration-700 shadow-[0_0_10px_#ef4444]";
            if (document.getElementById('auto-pilot').checked) {
                logEvent("AUTO-PILOT: Threshold reached. Killing process.", "error");
                kill();
            }
        } else if (percent > 70) {
            bar.className = "bg-orange-500 h-full transition-all duration-700";
        } else {
            bar.className = "bg-blue-500 h-full transition-all duration-700";
        }
    } catch (e) {}
}, 2000);