from flask import Flask, redirect, url_for
from flask import Flask, render_template
app = Flask(__name__)



@app.route("/") #no html
def home_0():
	return "Hello! This is the home page <h1>HELLO</h1>"

@app.route("/uno") #index_1: escribe lo que le mandes en content
def home_1():
    return render_template("1_index.html", content="Testing")

@app.route("/dos") #index_2: mandar true u otra cosa
def home_2():
    return render_template("2_index.html", content="true")

@app.route("/tres") #index_3: tiene un ciclo 
def home_3():
    return render_template("3_index.html", content="true")

@app.route("/cuatro") #index_3: tiene un ciclo 
def home_4():
    return render_template("4_index.html", content=["max", "asael", "valeria", "norman"])

@app.route("/<name>")
def user(name):
	return f"Hello {name}!"

@app.route("/admin")
def admin():                    #admin
    return redirect(url_for("user", nombre="Admin!"))
if __name__ == "__main__":
	app.run()