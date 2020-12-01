import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import csv
import logging
import certstream
import os
import sys
import random
project_root = "/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
data_treatment_folder = project_root + "/data_treatment/"
sys.path.append(project_root)
sys.path.append(data_treatment_folder)
from domain_name_analysis import Analyser
from cert_treatment import CertTreatment

def test(nb):
    if nb>=0.5:
        return 1
    else:
        return 0

def model_creation(neurons, nb_features, nb_targets, learning_rate):
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
    opt = tf.train.AdamOptimizer(learning_rate).minimize(mse)

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
                   training_targets):

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
        
    # #Uncomment if you want to see the content of the layers
    # xXx = training_labels
    # wh0 = session.run(layers_dict["weight_hidden_0"])
    # bh0 = session.run(layers_dict["bias_hidden_0"])
    # # hl0ws = session.run(layers_dict["hidden_layer_ws_0"], feed_dict={X: training_labels})
    # hl0 = session.run(layers_dict["hidden_layer_0"], feed_dict={X: training_labels})
    # wh1 = session.run(layers_dict["weight_hidden_1"])
    # bh1 = session.run(layers_dict["bias_hidden_1"])
    # # hl1ws = session.run(layers_dict["hidden_layer_ws_1"], feed_dict={X: training_labels})
    # hl1 = session.run(layers_dict["hidden_layer_1"], feed_dict={X: training_labels})
    # who = session.run(layers_dict["weight_out"])
    # bho = session.run(layers_dict["bias_out"])
    # hlo = session.run(layers_dict["output_layer"], feed_dict={X: training_labels})
    
    
    # print("------------------------X------------------------\n", xXx)
    # print("-----------------------wh0-----------------------\n", wh0)
    # print("-----------------------bh0-----------------------\n", bh0)
    # print("-----------------------hl0-----------------------\n", hl0)
    # # print("----------------------wshl0----------------------\n", hl0)
    # print("-----------------------wh1-----------------------\n", wh1)
    # print("-----------------------bh1-----------------------\n", bh1)
    # # print("----------------------wshl1----------------------\n", hl1)
    # print("-----------------------hl1-----------------------\n", hl1)
    # print("-----------------------who-----------------------\n", who)
    # print("-----------------------bho-----------------------\n", bho)
    # print("-----------------------hlo-----------------------\n", hlo)


        # if e == epochs-1 :
        #     validation_path = os.path.join(sys.path[0], "validation_image", "256.png")
        #     make_prediction(validation_path)

    # prediction = session.run(layers_dict["output_layer"], feed_dict={X:training_labels})

    return optimizer

def strbool_to_int(str):
    if (str=="True" or str=="TRUE"):
        return 1
    elif (str=="False" or str=="FALSE"):
        return 0

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
            if (id_feature == 1):
                features.append(min(int(row["Feature"+str(id_feature)])/50, 1))
            elif (id_feature == 2 or (id_feature>=10 and id_feature<=16)):
                features.append(strbool_to_int(row["Feature"+str(id_feature)]))
            else:
                features.append(int(row["Feature"+str(id_feature)]))
        labels.append(features)
        targets.append([strbool_to_int(row["is_suspicious"])])
        # print(row["is_suspicious"])

    return labels, targets

def handle_callback(message, context):
    global session, layers_dict, X
    handler = CertTreatment(message)
    domain_name = handler.get_domain_name()
    authority = handler.get_authority()

    analyser = Analyser(domain_name, authority)
    features = []
    features.append(min(analyser.levenshtein()/50, 1))
    features.append(int(analyser.issued_from_free_CA())) #2
    features.append(int(analyser.deeply_nested_subdomains())) #3
    features.append(int(analyser.suspicious_tld())) #4
    features.append(int(analyser.inner_tld_in_subdomain())) #5
    features.append(int(analyser.suspicious_keywords())) #6
    features.append(int(analyser.hyphens_in_subdomain())) #7
    features.append(int(analyser.suspicious_domain_length())) #8
    features.append(int(analyser.suspicious_characters())) #9
    features.append(int(analyser.suspicious_age_domain())) #10
    features.append(int(analyser.suspicious_date_creation()))
    features.append(int(analyser.suspicious_date_expiry()))
    features.append(int(analyser.suspicious_valid_period_domain()))
    features.append(int(analyser.suspicious_registrant_name()))
    features.append(int(analyser.suspicious_registrant_organization()))
    features.append(int(analyser.suspicious_registrarURL())) #16
 

    prediction = session.run(layers_dict["output_layer"], feed_dict={X:[features]})
    print(domain_name, " is suspicious at ", str(round(prediction[0][0]*100, 2)), "%")

def stream_handling():
    logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)
    certstream.listen_for_events(handle_callback, url='wss://certstream.calidog.io/')



def main():
    # Data processing
    training_file_path = project_root + 'TRAINING_SET.csv'
    training_file = open(training_file_path, 'r')
    
    nb_features = 16
    nb_targets = 1

    training_dictReader = csv.DictReader(training_file)

    training_labels, training_targets = create_labels_targets(training_dictReader, nb_features, nb_targets)
    c = list(zip(training_labels, training_targets))
    random.shuffle(c)
    training_labels, training_targets = zip(*c)

    # Parameters
    learning_rate = 0.0001
    hidden_neurons = [200, 200, 200]

    # Model creation
    global session, layers_dict, X
    X, Y, session, optimizer, error_fn, layers_dict = model_creation(hidden_neurons, nb_features, nb_targets, learning_rate)

    # Model training
    total_epochs = 0
    next = 1
    while next==1 :
        epochs = int(input("How many epochs for the training? "))
        model_training(X=X, Y=Y,
                       session = session,
                       optimizer = optimizer,
                       error_fn = error_fn,
                       layers_dict=layers_dict,
                       batch_size = 50,
                       epochs = epochs,
                       training_labels = training_labels,
                       training_targets = training_targets)
        total_epochs += epochs
        next = int(input("Continue training? (1:yes, 0:no) "))
    
    stream_handling()

if __name__ == "__main__":
    main()