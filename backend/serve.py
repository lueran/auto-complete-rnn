import os
from backend.cors import crossdomain
from flask import Flask, jsonify, request, render_template

from backend.neural_complete import neural_complete
from backend.neural_complete import get_model


def read_models(base_path="models/"):
    return set([x.split(".")[0] for x in os.listdir(base_path)])


app = Flask(__name__)

models = {x: get_model(x) for x in read_models()}


def get_args(req):
    if request.method == 'POST':
        args = request.json
    elif request.method == "GET":
        args = request.args
    return args


@app.route("/predict", methods=["GET", "POST", "OPTIONS"])
@crossdomain(origin='*', headers="Content-Type")
def predict():
    args = get_args(request)
    keyword = args.get("keyword", "import")
    sentence = keyword
    model_name = "neural_char"
    suggestions = neural_complete(models[model_name], sentence, [0.2, 0.5, 1])
    return jsonify({"data": {"results": [x.strip() for x in suggestions]}})


@app.route("/get_models", methods=["GET", "POST", "OPTIONS"])
@crossdomain(origin='*', headers="Content-Type")
def get_models():
    return jsonify({"data": {"results": list(models)}})


@app.route("/", methods=["GET"])
@crossdomain(origin='*', headers="Content-Type")
def index():
    return render_template('editor.html')


@app.route("/editor", methods=["GET"])
@crossdomain(origin='*', headers="Content-Type")
def editor():
    return render_template('editor.html')


def main(host="127.0.0.1", port=9078):
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    main()
