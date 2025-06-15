from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/review', methods=['POST'])
def review():
    data = request.json
    pr_diff = data.get("diff")
    # TODO: Run ONNX/Phi-4 inference on diff and generate comments.
    comments = [
        {"file": "example.py", "line": 10, "comment": "Consider renaming this variable for clarity."}
    ]
    return jsonify({"comments": comments})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
