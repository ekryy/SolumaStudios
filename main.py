from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# HTML template as a string
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upgrade Simulator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        textarea { width: 100%; height: 100px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
    </style>
</head>
<body>
    <h1>MMU & PCU Upgrade Simulator</h1>
    <form method="post">
        <label>MMU Prices (comma-separated):</label><br>
        <textarea name="mmu_prices">{{ mmu_prices }}</textarea><br>
        <label>PCU Prices (comma-separated):</label><br>
        <textarea name="pcu_prices">{{ pcu_prices }}</textarea><br>
        <label>Production Rates (comma-separated):</label><br>
        <textarea name="rates">{{ rates }}</textarea><br>
        <button type="submit">Simulate</button>
    </form>
    {% if result %}
    <h2>Results</h2>
    <table>
        <tr><th>Upgrade #</th><th>Type</th><th>Step Time</th><th>Cumulative Time</th></tr>
        {% for row in result %}
        <tr>
            <td>{{ row.step }}</td>
            <td>{{ row.upgrade }}</td>
            <td>{{ "%.2f"|format(row.step_time) }}</td>
            <td>{{ "%.2f"|format(row.cum_time) }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    mmu_prices = request.form.get('mmu_prices', '20,50,90')
    pcu_prices = request.form.get('pcu_prices', '40,80,120')
    rates = request.form.get('rates', '1,1')
    result = []
    if request.method == 'POST':
        mmu = list(map(float, mmu_prices.split(',')))
        pcu = list(map(float, pcu_prices.split(',')))
        rate = list(map(float, rates.split(',')))
        # initial values
        time = 0.0
        step = 1
        # simulate alternating upgrades: MMU then PCU until both lists exhausted
        i = j = 0
        cum = 0.0
        while i < len(mmu) or j < len(pcu):
            if i < len(mmu):
                dt = mmu[i] / ( (pcu[j-1] if j>0 else 1) * (rate[0] if rate else 1) )
                cum += dt
                result.append({'step': step, 'upgrade': 'MMU', 'step_time': dt, 'cum_time': cum})
                i += 1; step += 1
            if j < len(pcu):
                dt = pcu[j] / ( (mmu[i-1] if i>0 else 1) * (rate[1] if len(rate)>1 else 1) )
                cum += dt
                result.append({'step': step, 'upgrade': 'PCU', 'step_time': dt, 'cum_time': cum})
                j += 1; step += 1
    return render_template_string(TEMPLATE,
                                  mmu_prices=mmu_prices,
                                  pcu_prices=pcu_prices,
                                  rates=rates,
                                  result=result)

if __name__ == '__main__':
    app.run(debug=True)
