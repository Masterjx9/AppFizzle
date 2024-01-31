from flask import Flask, render_template, send_from_directory, render_template_string, Response
import os

app = Flask(__name__, static_folder='public', template_folder='public')

@app.route('/')
def index():
    ### Change the render_template call to render_template_string 
    ### based on if you are using a different
    ### frontend other than Flask
    
    # RENDER_INDEX
    return render_template('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # Serve static files from the 'public' folder
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
