from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('9_index.html')

@app.route('/run_function', methods=['POST'])
def run_function():
    # Your function logic here
    result = "Function executed!"  # Replace with the result of your function
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
