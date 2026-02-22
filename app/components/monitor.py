MONITOR = '''
<div class="mb-8">
    <div class="flex items-center justify-between bg-slate-900/50 p-3 rounded-xl border border-slate-700/50 mb-4">
        <span class="text-[10px] uppercase tracking-widest text-slate-400 font-bold">Auto-Pilot Protection</span>
        <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="auto-pilot" class="sr-only peer">
            <div class="w-9 h-5 bg-slate-700 rounded-full peer peer-checked:bg-blue-600 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:after:translate-x-full"></div>
        </label>
    </div>
    <div class="flex justify-between text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-2">
        <span>Memory Usage</span>
        <span id="mem-text">0MB / 512MB</span>
    </div>
    <div class="w-full bg-slate-900 rounded-full h-3 border border-slate-700 overflow-hidden">
        <div id="mem-bar" class="bg-blue-500 h-full transition-all duration-700 ease-in-out" style="width: 0%"></div>
    </div>
</div>
'''