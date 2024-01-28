from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='public', template_folder='public')

@app.route('/')
def index():
    # Render 'index.html' from the 'public' folder
    return render_template('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # Serve static files from the 'public' folder
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
