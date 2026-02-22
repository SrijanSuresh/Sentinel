CONTROLS = '''
<div class="mb-6">
    <label class="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-2 block">Task Management</label>
    <div class="flex gap-2 mb-3">
        <input id="cmd-input" type="text" placeholder="CMD HERE" 
               class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-blue-500 transition-colors">
        <button onclick="runCmd()" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-xl text-sm font-bold transition-all active:scale-95">RUN</button>
    </div>
    <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
        <button onclick="preset('python3 tests/mod_simulator.py')" class="whitespace-nowrap bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded-lg text-[10px] font-bold border border-slate-600">MOD SIM</button>
        <button onclick="preset('python3 tests/heavy_compute.py')" class="whitespace-nowrap bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded-lg text-[10px] font-bold border border-slate-600">HEAVY LOAD</button>
    </div>
</div>
'''