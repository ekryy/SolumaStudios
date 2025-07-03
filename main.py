from flask import Flask, render_template_string, request

app = Flask(__name__, static_folder='static', static_url_path='/static')

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  
  <title>Loading...</title>
  
  <link rel="icon" href="/static/Solumalogo.png" type="image/png">
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    input, textarea { width: 100%; margin-bottom: 10px; }
    button { padding: 10px 20px; margin-right: 10px; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
    button:disabled { background: #ccc; cursor: not-allowed; }
  </style>
</head>
<body>

  <h1> Soluma Studios</h1>

  
  <div>
    <label>PCU values (comma-separated):</label>
    <input id="pcu_values" value="0.85, 0.70, 0.65, 0.60, 0.50, 0.45, 0.40, 0.35, 0.30">
    <label style="background: #98FB98;">PCU costs:</label>
    <input style="background: #98FB98;" id="pcu_costs" value="20, 55, 125, 179, 490, 900, 15000, 45000">

    <label>MMU values:</label>
    <input id="mmu_values" value="1.5, 2, 2.5, 3, 3.5, 4, 5, 8, 10, 20">
    <label style="background: #98FB98;">MMU costs:</label>
    <input style="background: #98FB98;" id="mmu_costs" value="10, 40, 100, 200, 330, 500, 1200, 1600, 6000, 100000">

    <label>BPU values:</label>
    <input id="bpu_values" value="25,50,100,200,400,800,1600,3200,6400,12800,25000,50000">
    <label style="background: #98FB98;">BPU costs:</label>
    <input style="background: #98FB98;" id="bpu_costs" value="15,30,60,120,210,480,800,1500,3000,50000,70000,200000">

    <div>
      <button id="btn_pcu">Upgrade PCU</button>
      <button id="btn_mmu">Upgrade MMU</button>
      <button id="btn_bpu">Upgrade BPU</button>
      <button id="btn_reset" >Reset Steps</button>
    </div>
  </div>

  <table id="results">
    <thead>
      <tr>
        <th>Step</th>
        <th>Type</th>
        <th>Old Value</th>
        <th>New Value</th>
        <th>Cost</th>
        <th style="background: #e05351;">Step Time (s)</th>
        <th>Cumulative Time (s)</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <script>
  
    const parse = id => document.getElementById(id).value.split(',').map(Number);
    let pcu_vals;
    let pcu_costs;
    let mmu_vals;
    let mmu_costs;
    let bpu_vals;
    let bpu_costs;
    let idx = { pcu: 0, mmu: 0, bpu: 0};
    let cur = { pcu: 1, mmu: 1, bpu: 1};
    let cumTime = 0;
    let stepCounter = 1;

    function saveSettings() {
      localStorage.setItem('pcu_vals', document.getElementById('pcu_values').value);
      localStorage.setItem('pcu_costs', document.getElementById('pcu_costs').value);
      localStorage.setItem('mmu_vals', document.getElementById('mmu_values').value);
      localStorage.setItem('mmu_costs', document.getElementById('mmu_costs').value);
      localStorage.setItem('bpu_vals', document.getElementById('bpu_values').value);
      localStorage.setItem('bpu_costs', document.getElementById('bpu_costs').value);
    }

    function loadSettings() {
      if (localStorage.pcu_vals) {
        document.getElementById('pcu_values').value = localStorage.pcu_vals;
        document.getElementById('pcu_costs').value = localStorage.pcu_costs;
        document.getElementById('mmu_values').value = localStorage.mmu_vals;
        document.getElementById('mmu_costs').value = localStorage.mmu_costs;
        document.getElementById('bpu_values').value = localStorage.bpu_vals;
        document.getElementById('bpu_costs').value = localStorage.bpu_costs;
      }
    }



    
    function init() {
      loadSettings();

      
      pcu_vals = parse('pcu_values');
      pcu_costs = parse('pcu_costs');
      mmu_vals = parse('mmu_values');
      mmu_costs = parse('mmu_costs');
      bpu_vals = parse('bpu_values');
      bpu_costs = parse('bpu_costs');


      ['pcu_values','pcu_costs','mmu_values','mmu_costs','bpu_values','bpu_costs']
        .forEach(id => {
          document.getElementById(id).onchange = saveSettings;
        });
    }

    function upgrade(type) {
      const costArr = type === 'pcu' ? pcu_costs : type === 'mmu' ? mmu_costs : bpu_costs;
      
      if (idx[type] >= costArr.length) {
        document.getElementById(`btn_${type}`).disabled = true;
        return;
      }
      
      const valArr = type === 'pcu' ? pcu_vals : type === 'mmu' ? mmu_vals : bpu_vals;
      const oldVal = valArr[idx[type]];
      const newVal = valArr[idx[type] + 1] || valArr[valArr.length - 1];
      const rate = cur.pcu * cur.mmu;
      const cost = costArr[idx[type]];
      const stepTime = cost / rate;
      cumTime += stepTime;
      cur[type] = newVal;
      idx[type] = idx[type] + 1;

      if (idx[type] >= costArr.length) {
        document.getElementById(`btn_${type}`).disabled = true;
      }

      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${stepCounter}</td>
        <td>${type.toUpperCase()}</td>
        <td>${oldVal}</td>
        <td>${newVal}</td>
        <td>${cost}</td>
        <td style="background: #e05351">${stepTime.toFixed(2)}</td>
        <td>${cumTime.toFixed(2)}</td>
      `;
      document.querySelector('#results tbody').appendChild(row);
      stepCounter += 1;
    }

    

    document.getElementById('btn_pcu').onclick = () => upgrade('pcu');
    document.getElementById('btn_mmu').onclick = () => upgrade('mmu');
    document.getElementById('btn_bpu').onclick = () => upgrade('bpu');
    const btnReset = document.getElementById('btn_reset');
    btnReset.onclick = () => {
      document.querySelector('#results tbody').innerHTML = '';
      cumTime = 0;
      stepCounter = 1;
      idx = { pcu: 0, mmu: 0, bpu: 0 };
      cur = { pcu: 1, mmu: 1, bpu: 1 };
      document.getElementById('btn_pcu').disabled = false;
      document.getElementById('btn_mmu').disabled = false;
      document.getElementById('btn_bpu').disabled = false;
      
      saveSettings();
    };

    init();
  </script>

<script src="/static/typing.js"></script>

  
</body>
</html>
"""


@app.route('/')
def index():
  return render_template_string(TEMPLATE)


@app.route('/upload', methods=['POST'])
def upload_image():
  if 'file' not in request.files:
    return 'No file selected', 400

  file = request.files['file']
  if file.filename == '':
    return 'No file selected', 400

  if file and file.filename.lower().endswith('.png'):
    # Save to static folder
    import os
    os.makedirs('static', exist_ok=True)
    file.save(os.path.join('static', file.filename))
    return f'Image uploaded successfully: /static/{file.filename}'

  return 'Invalid file type. Please upload a PNG file.', 400


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000)
