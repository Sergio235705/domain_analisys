import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import csv

def model_creation(neurons, nb_features, nb_targets):
    # Session
    sess = tf.InteractiveSession()

    # Placeholders
    X = tf.placeholder(tf.float32, shape=[None, nb_features])
    Y = tf.placeholder(tf.float32, shape=[None, nb_targets])

    # Definition on number of neurons and layers
    if len(neurons)<1 :
        raise Exception("You must have at least one hidden layer")

    weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=1)
    bias_initializer = tf.zeros_initializer()
    layers_dict = {} #

    # Hidden weight and bias
    for id in range(len(neurons)) :
        if id == 0:
            layers_dict["weight_hidden_"+str(id)] = tf.Variable(weight_initializer([nb_features , neurons[id]]))
            layers_dict["bias_hidden_"+str(id)] = tf.Variable(bias_initializer([neurons[id]]))
        else:
            layers_dict["weight_hidden_"+str(id)] = tf.Variable(weight_initializer([neurons[id-1] , neurons[id]]))
            layers_dict["bias_hidden_"+str(id)] = tf.Variable(bias_initializer([neurons[id]]))

    # Out layers and bias
    layers_dict["weight_out"] = tf.Variable(weight_initializer([neurons[-1], nb_targets]))
    layers_dict["bias_out"] = tf.Variable(bias_initializer([nb_targets]))

    # Hidden layers
    for id in range(len(neurons)) :
        if id==0 :
            layers_dict["hidden_layer_"+str(id)] = tf.sigmoid(tf.add(
                tf.matmul(X, layers_dict["weight_hidden_"+str(id)]),
                layers_dict["bias_hidden_"+str(id)]
                ))
        else :
            layers_dict["hidden_layer_"+str(id)] = tf.sigmoid(tf.add(
                tf.matmul(layers_dict["hidden_layer_"+str(id-1)], layers_dict["weight_hidden_"+str(id)]),
                layers_dict["bias_hidden_"+str(id)]
                ))

    # Output layer
    layers_dict["output_layer"] = tf.abs(tf.transpose(tf.add(
        tf.matmul(layers_dict["hidden_layer_"+str(len(neurons)-1)],layers_dict["weight_out"]),
        layers_dict["bias_out"]
        )))

    #Cost_function
    mse = tf.sqrt(tf.reduce_mean(tf.squared_difference(layers_dict["output_layer"], Y)))

    # Optimizer
    opt = tf.train.AdamOptimizer(0.001).minimize(mse)

    # Init
    sess.run(tf.global_variables_initializer())

    return ((X, Y, sess, opt, mse, layers_dict))

def model_training(X, Y,
                   session,
                   optimizer,
                   error_fn,
                   layers_dict,
                   batch_size,
                   epochs,
                   training_labels,
                   training_targets,
                   test_labels,
                   test_targets):

    training_error, test_error, validation_error = [], [], []
    validation_min, validation_max, validation_mean, validation_std = np.array([]), np.array([]), np.array([]), np.array([])

    for e in range(epochs) :
        for i in range(len(training_targets) // batch_size) :
            training_labels_batch = training_labels[i*batch_size : (i+1)*batch_size]
            training_targets_batch = training_targets[i*batch_size : (i+1)*batch_size]
            session.run(optimizer, feed_dict={X: training_labels_batch, Y: training_targets_batch})

            training_error.append(session.run(error_fn, feed_dict={X: training_labels, Y: training_targets}))
            print ("Epoch: {}, Batch: {}, Training error: {}"
                    .format(e+1, i+1, training_error[-1]))

        # if e == epochs-1 :
        #     validation_path = os.path.join(sys.path[0], "validation_image", "256.png")
        #     make_prediction(validation_path)

    return optimizer

def create_labels_targets(reader, nb_features, nb_targets):
    # labels = np.zeros((len,nb_features))
    # targets = np.zeros((len,nb_targets))
    labels = []
    targets = []
    id_row = 0
    for row in reader:
        # print("\n\nLa row :\n", row, "\n", type(row))
        features = []
        for id_feature in range(1, nb_features+1):
            features.append(row["Feature"+str(id_feature)])
        labels.append(features)
        is_suspicious = row["is_suspicious"]
        if is_suspicious == 'TRUE':
            targets.append([1])
        elif is_suspicious == 'FALSE':
            targets.append([0])
        else:
            raise Exception("Bad suspiciousness value")
        # print(row["is_suspicious"])

    return labels, targets


def main():
    # Data processing
    training_file_path = 'training_fake.csv'
    training_file = open(training_file_path, 'r')

    test_file_path = 'test_fake.csv'
    test_file = open(test_file_path, 'r')
    
    nb_features = 3
    nb_targets = 1
    hidden_neurons = [20, 20]

    training_dictReader = csv.DictReader(training_file)
    test_dictReader = csv.DictReader(test_file)

    training_labels, training_targets = create_labels_targets(training_dictReader, nb_features, nb_targets)
    test_labels, test_targets = create_labels_targets(test_dictReader, nb_features, nb_targets)

    # Model creation
    X, Y, session, optimizer, error_fn, layers_dict = model_creation(hidden_neurons, nb_features, nb_targets)

    # print("\n\nFIINI\n\n")

    # Model training
    next = 1
    while next==1 :
        epochs = int(input("Combien d'epochs ? "))
        model_training(
                X=X, Y=Y,
                session = session,
                optimizer = optimizer,
                error_fn = error_fn,
                layers_dict=layers_dict,
                batch_size = 50,
                epochs = epochs,
                training_labels = training_labels,
                training_targets = training_targets,
                test_labels = test_labels,
                test_targets = test_targets)
        next = int(input("On continue ? "))


if __name__ == "__main__":
    main()