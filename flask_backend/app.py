from flask import Flask, request
import json
import common

app = Flask(__name__)

@app.route('/builder', methods=['POST'])
def builder():
    if request.method == 'POST':
        data = request.json
        print(data)
        backend_config = common.get_config(data["backend"], "backends")
        frontend_config = common.get_config(data["frontend"], "frontends")
        print(backend_config)
        print(frontend_config)
        return {"result": "success"}
    
if __name__ == '__main__':
    app.run(debug=True)    