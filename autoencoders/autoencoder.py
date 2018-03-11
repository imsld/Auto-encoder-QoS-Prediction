'''
Created on 21 janv. 2018

@author: N'TIC
'''

import tensorflow as tf
import math

def create(x, layer_sizes):
    
    # Build the encoding layers
    next_layer_input = x

    encoding_matrices = []
    for dim in layer_sizes:
        input_dim = int(next_layer_input.get_shape()[1])

        # Initialize W using random values in interval [-1/sqrt(n) , 1/sqrt(n)]
        W = tf.Variable(tf.random_uniform([input_dim, dim], -1.0 / math.sqrt(input_dim), 1.0 / math.sqrt(input_dim)))

        # Initialize b to zero
        b = tf.Variable(tf.zeros([dim]))

        # We are going to use tied-weights so store the W matrix for later reference.
        encoding_matrices.append(W)

        output = (tf.matmul(next_layer_input, W) + b)

        # the input into the next layer is the output of this layer
        next_layer_input = output

    # The fully encoded x value is now stored in the next_layer_input
    encoded_x = next_layer_input

    # build the reconstruction layers by reversing the reductions
    layer_sizes.reverse()
    encoding_matrices.reverse()


    for i, dim in enumerate(layer_sizes[1:] + [ int(x.get_shape()[1])]) :
        # we are using tied weights, so just lookup the encoding matrix for this step and transpose it
        W_prime = tf.transpose(encoding_matrices[i])
        b_prime = tf.Variable(tf.zeros([dim]))
        output = (tf.matmul(next_layer_input, W_prime) + b_prime)
        next_layer_input = output

    # the fully encoded and reconstructed value of x is here:
    reconstructed_x = next_layer_input
    
    return{
        'encoded': encoded_x,
        'decoded': reconstructed_x,
        'RMSE' : tf.sqrt(tf.reduce_mean(tf.square(x - reconstructed_x))),
        #'MAE' : tf.reduce_mean(tf.abs(x - reconstructed_x)),
        'weight': W,
        'bias':b,
        'weight_prime': W_prime,
        'bias_prime': b_prime
    }
    
def get_rmse_mae_Vlaues(sess, matrix, best_model, data):

    _x = tf.cast(matrix, tf.float32) 
    _w = best_model['weight']
    _b = best_model['bias']               
    _x_encoded = (tf.matmul(_x, _w) + _b)
    
    
    _w_prime = best_model['weight_prime']
    _b_prime = best_model['bias_prime']    
    _x_decoded = (tf.matmul(_x_encoded, _w_prime) + _b_prime)
    
        
    xx_nan = data.as_matrix()
    yy_nan = _x_decoded    
    diff = xx_nan - yy_nan    
    nan_v = tf.is_nan(diff)
    
    diff_nan = tf.logical_not(nan_v)

    valeur = tf.boolean_mask(diff, diff_nan)
    
    result_new_rmse_nan = sess.run(tf.sqrt(tf.reduce_mean(tf.square(valeur))))
    result_new_mae_nan = sess.run(tf.reduce_mean(tf.abs(valeur)))
    
    return result_new_rmse_nan, result_new_mae_nan
