from flask import Flask, request, send_file, g, render_template
from flask_cors import CORS
import common
import uuid
import os
import shutil
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/builder_dockerfile', methods=['POST'])
def builder():
    if request.method == 'POST':
        data = request.json
        print(data)
        if "frontend" in data:
            processed_dockerfile = common.dockerfile_flow(data["backend"], data["frontend"])
        else:
            processed_dockerfile = common.dockerfile_flow(data["backend"])
        return {"result": "success", "dockerfile": processed_dockerfile}

@app.route('/builder_dockerpackage', methods=['POST'])
def builder_dockerpackage():
    if request.method == 'POST':
        data = request.json
        print(data)
        if "frontend" in data:
            processed_dockerfile = common.dockerfile_flow(data["backend"], data["frontend"])
        else:
            processed_dockerfile = common.dockerfile_flow(data["backend"])
            
        unique_id = uuid.uuid4()
        g.unique_id = unique_id  # Store the unique_id in g for later cleanup
        packaged_dockerfile = common.package_dockerfile(unique_id, data, processed_dockerfile)
        
        # Ensure the file exists
        if os.path.exists(packaged_dockerfile):
            return send_file(packaged_dockerfile, as_attachment=True, download_name=f"dockerfile_package_{unique_id}.zip")
        else:
            return {"error": "Packaged Dockerfile not found."}, 404

@app.after_request
def cleanup(response):
    unique_id = getattr(g, 'unique_id', None)
    if unique_id:
        temp_dir = os.path.join(os.getcwd(), "temp", str(unique_id))
        if os.path.isdir(temp_dir):
            print("Removing directory:", temp_dir)
            shutil.rmtree(temp_dir)  # Delete the entire directory tree
            g.unique_id = None # Reset the flag
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)