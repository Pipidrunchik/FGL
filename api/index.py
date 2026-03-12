from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random, math

app = Flask(__name__)
CORS(app) # Это чтобы Flutter не ругался на запросы

class QuantumCore:
    def __init__(self):
        self.base_temp = 32.4
        self.gates = {
            "constant": {"c": "┌───┐ ░ ┌───┐ ┌─┐\nq0: ──┤ H ├─░─┤ H ├─┤M├\nq1: ──┤ X ├─░─┤ H ├──╫──", "fid": 0.99},
            "balanced": {"c": "┌───┐ ░ ┌───┐ ┌─┐\nq0: ──┤ H ├─░─┤ H ├─┤M├\nq1: ──┤ X ├─░─┤ H ├──╫──", "fid": 0.95},
            "bell": {"c": "┌───┐ ┌─┐\nq0: ──┤ H ├──■───┤M├\nq1: ───────┤ X ├──╫──", "fid": 0.99}
        }

    def process_run(self, gate_name):
        if gate_name == "batch": return self.run_batch(100)
        info = self.gates.get(gate_name, self.gates["constant"])
        temp = self.base_temp + random.uniform(0, 4.0)
        noise = (math.exp(temp / 40) - 1) * 0.1
        fidelity = max(0.0, min(1.0, info['fid'] - noise))
        return {"type": "SINGLE", "mode": gate_name, "temp": round(temp, 1), "fidelity": round(fidelity, 4), "c": info["c"]}

    def run_batch(self, count):
        fids = [0.99 - (math.exp((self.base_temp + random.uniform(0, 5.0))/40)-1)*0.1 for _ in range(count)]
        return {"type": "BATCH", "mode": "batch_process", "temp": round(self.base_temp + 2.0, 1), "fidelity": round(sum(fids)/count, 4), "c": " [ BATCH_DATA_STREAM ] ", "count": count}

core = QuantumCore()

@app.route('/api')
def handle_quantum():
    gate = request.args.get('gate', 'constant')
    return jsonify(core.process_run(gate))

# Для локальной отладки (если захочешь запустить на мобиле)
if __name__ == '__main__':
    app.run(port=8080)
