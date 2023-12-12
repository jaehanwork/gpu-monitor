from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/gpu-status')
def gpu_info():
    try:
        process = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode() if process.returncode == 0 else f"Error: {error.decode()}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15001)
