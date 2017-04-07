from __future__ import print_function
from __future__ import division

import tensorflow as tf

# http://stackoverflow.com/questions/41918795/minimize-a-function-of-one-variable-in-tensorflow#41948131

'''
x = tf.Variable(10.0, trainable=True)
f_x = 2 * x* x - 5 *x + 4

loss = f_x
opt = tf.train.GradientDescentOptimizer(0.1).minimize(f_x)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(100):
        print(sess.run([x,loss]))
        sess.run(opt)
'''

# now http://codeforces.com/problemset/problem/782/B

meet = tf.Variable(0.0, trainable=True)
positions = tf.constant([5, 10, 3, 2], dtype=tf.float32)
speeds = tf.constant([2, 3, 2, 4], dtype=tf.float32)

loss = tf.reduce_max(tf.abs(positions - meet) / speeds)  # Note: not tf.maximum, this is a single tensor

# manual learning rate decay
rate = 0.5
opt = tf.train.GradientDescentOptimizer(learning_rate=rate).minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    prev_loss = 10**10
    for i in range(100):
        meet_, loss_ = sess.run([meet, loss])
        print(meet_, loss_, rate)
        if loss_ > prev_loss:
            rate /= 2
            opt = tf.train.GradientDescentOptimizer(learning_rate=rate).minimize(loss)
        prev_loss = loss_
        sess.run(opt)

