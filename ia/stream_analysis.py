import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

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
        )), name = "output_layer")

    #Cost_function
    mse = tf.sqrt(tf.reduce_mean(tf.squared_difference(layers_dict["output_layer"], Y)))

    # Optimizer
    opt = tf.train.AdamOptimizer(0.001).minimize(mse)

    # Init
    sess.run(tf.global_variables_initializer())

    return ((X, Y, sess, opt, mse, layers_dict))


def make_prediction(session, features, X, layers_dict):
    np_array = np.array(features)
    # prediction = session.run("output_layer", feed_dict={X:np.reshape(np_array, (-1, 3))})
    prediction = session.run(layers_dict["output_layer"], feed_dict={X:[[0.7242, 0.2116, 0.4853]]})
    return prediction

    # [[0.7242], [0.2116], [0.4853]] -> (3,1)
    # [0.7242, 0.2116, 0.4853] -> (3,)
    # [[0.7242, 0.2116, 0.4853]] -> (1,3

def main():
    print("\n\n\n\n============================")
    tf.reset_default_graph()
    imported_meta = tf.train.import_meta_graph("model_final.meta")
    session = tf.Session()
    imported_meta.restore(session, tf.train.latest_checkpoint('./'))

    nb_features = 3
    nb_targets = 1
    hidden_neurons = [20, 20]
    X, Y, session, optimizer, error_fn, layers_dict = model_creation(hidden_neurons, nb_features, nb_targets)

    # print(session.run(tf.global_variables))
    # print(session.run('output_layer'))

    web_site = "test.com"
    features =[0.7242, 0.2116, 0.4853]
    suspiciousness = make_prediction(session, features, X, layers_dict)
    print(suspiciousness)

if __name__ == "__main__":
    main()