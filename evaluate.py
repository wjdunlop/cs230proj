import train

def evaluate(X_train, y_train, X_dev, y_dev, X_test, y_test, encoding_size, weights_name):
    model = train.get_model(X_dev, encoding_size)
    model.load_weights(weights_name)

    print("TRAIN STATS:")
    print(model.evaluate(X_train, y_train))

    print("DEV STATS:")
    print(model.evaluate(X_dev, y_dev))

    print("TEST STATS:")
    print(model.evaluate(X_test, y_test))