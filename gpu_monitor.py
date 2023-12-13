from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)
servers = ['143.248.55.122', '143.248.53.147', '143.248.57.147', '143.248.38.64']  # Replace with the IPs of your GPU servers

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Central GPU Monitoring</title>
        <style>
            body { background-color: black; color: white; font-family: monospace; }
            select {
                padding: 10px;
                border: 2px solid #fff;
                background-color: #555;
                color: #fff;
                margin-bottom: 20px;
                font-size: 100%;
            }
            .highlight { 
                background-color: white; 
                color: black; 
                font-weight: bold; 
            }
            #gpu-status { 
                white-space: pre-wrap; 
                word-wrap: break-word; 
            }
        </style>
    </head>
    <body>
        <h1>GPU Status</h1>
        <select id="server-select" onchange="fetchGPUStatus()">
            {% for server in servers %}
            <option value="{{ server }}">{{ server }}</option>
            {% endfor %}
        </select>
        <div id="gpu-status">Select a server to display GPU info</div>

        <script>
            let previousData = {};
            let lastRequestedServer = '';

            function fetchGPUStatus() {
                var server = document.getElementById('server-select').value;
                lastRequestedServer = server;  // Update the last requested server
                fetch('/get-gpu-status?server=' + server)
                .then(response => response.json())
                .then(data => {
                    // Check if the response is for the last requested server
                    if (server === lastRequestedServer) {
                        const gpuStatusElement = document.getElementById('gpu-status');
                        if (!previousData[server] || previousData[server] !== data.content) {
                            gpuStatusElement.innerHTML = highlightChanges(data.content, previousData[server] || "");
                            previousData[server] = data.content;
                        }
                    }
                });
            }

            function highlightChanges(newData, oldData) {
                return newData.split('').map((char, index) => {
                    return (char !== oldData.charAt(index) ? '<span class="highlight">' + char + '</span>' : char);
                }).join('');
            }

            setInterval(fetchGPUStatus, 1000); // Refresh every 1000 milliseconds (1 second)
        </script>
    </body>
    </html>
    ''', servers=servers)

@app.route('/get-gpu-status')
def get_gpu_status():
    server = request.args.get('server')
    if not server:
        return jsonify({'content': "No server selected"})
    try:
        response = requests.get(f'http://{server}:15001/gpu-status')
        return jsonify({'content': response.text})
    except requests.RequestException as e:
        return jsonify({'content': f"Error connecting to server {server}: {e}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)
