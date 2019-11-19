from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

# Just for Designing Purpose
@app.route("/<foldername>/<filename>")
@app.route("/<filename>")
@app.route('/<foldername>/<sub_folder>/<filename>')
def open_any_file(foldername="", filename="", sub_folder=""):
    
    return render_template(
        filename,
    )


if __name__ == '__main__':
    app.run(debug=True)