from flask import Flask, redirect, url_for

app = Flask(__name__)

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return "Hello! this is the main page <h1>HELLO</h1>"  # some basic inline html

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
	return redirect(url_for("user", name="hijodetuputamadre")) #no le pongas name="admin" pq truena xd 

if __name__ == "__main__":
    app.run()
    
    
 
    



