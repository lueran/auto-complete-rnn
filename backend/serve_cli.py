import os



from backend.neural_complete import get_model, neural_complete


def read_models(base_path="models/"):
    return set([x.split(".")[0] for x in os.listdir(base_path)])


def predict(sentence="from", model_name="neural_char"):
    if model_name not in models:
        models[model_name] = get_model(model_name)
    suggestions = neural_complete(models[model_name], sentence, [0.2, 0.5, 1])
    return {"data": {"results": [x.strip() for x in suggestions]}}


models = {x: get_model(x) for x in read_models()}


def main():
    print(predict())

    while True:
        sentence = input()
        print(predict(sentence))


if __name__ == '__main__':
    main()