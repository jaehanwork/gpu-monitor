from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    # Serve an HTML page with enhanced JavaScript and CSS
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>GPU Status</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: monospace;
            }
            .highlight {
                background-color: white;
                color: black;
            }
        </style>
        <script>
            let previousData = "";

            function fetchGPUStatus() {
                fetch("/gpu-status")
                .then(response => response.text())
                .then(data => {
                    const gpuStatusElement = document.getElementById("gpu-status");
                    highlightChanges(gpuStatusElement, data);
                    previousData = data;
                });
            }

            function highlightChanges(element, newData) {
                if (newData !== previousData) {
                    element.innerHTML = newData.replace(/./g, (char, index) => {
                        return (char !== previousData[index] ? '<span class="highlight">' + char + '</span>' : char);
                    });
                }
            }

            setInterval(fetchGPUStatus, 1000); // Refresh every 1000 milliseconds (1 second)
        </script>
    </head>
    <body onload="fetchGPUStatus()">
        <h1>GPU Status</h1>
        <pre id="gpu-status">Loading...</pre>
    </body>
    </html>
    ''')

@app.route('/gpu-status')
def gpu_status():
    try:
        process = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            return f"Error: {error.decode()}"

        return f"{output.decode()}"

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/gpu-processes')
def gpu_processes():
    try:
        process = subprocess.Popen(['nvidia-smi', '--query-compute-apps=pid,name,gpu_memory_used', '--format=csv'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            return f"Error: {error.decode()}"

        return f"<pre>{output.decode()}</pre>"

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)

