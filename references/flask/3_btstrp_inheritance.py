from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    #llamamos 7_index (tiene el contenido de los bloques), que extiende a 6_base (donde esta el bootstrap)
    return render_template("7_index.html") 

if __name__ == "__main__":
    app.run(debug=True)