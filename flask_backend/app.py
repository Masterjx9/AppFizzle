from flask import Flask, request
import json
import common

app = Flask(__name__)

@app.route('/builder', methods=['POST'])
def builder():
    if request.method == 'POST':
        data = request.json
        print(data)
        backend_config = json.loads(common.get_config(data["backend"], "backends"))
        backend_dockerfile = common.build_dockerfile(backend_config)
        
        if "frontend" in data:
            frontend_config = json.loads(common.get_config(data["frontend"], "frontends"))
            frontend_dockerfile = common.build_dockerfile(frontend_config)
        else:
            frontend_config = None
            frontend_dockerfile = None
        
        processed_dockerfile = common.replace_template_variables(backend_dockerfile, backend_config["defaults"], frontend_dockerfile, frontend_config)
        return {"result": "success", "dockerfile": processed_dockerfile}
    
if __name__ == '__main__':
    app.run(debug=True)    