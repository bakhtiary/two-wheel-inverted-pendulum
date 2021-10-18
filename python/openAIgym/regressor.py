# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""tfdbg example: debugging tf.keras models training on tf.data.Dataset."""

import argparse
import sys
import tempfile

import numpy as np
import tensorflow

from tensorflow.python import debug as tf_debug

tf = tensorflow.compat.v1

from openAIgym.data_extractor import *
import gym
import xgboost
import tensorflow as tf2
import tensorflow_addons as tfa
import matplotlib.pyplot as plt
from keras import backend as K
from tensorflow.python import debug as tf_debug

sess = K.get_session()
sess = tf_debug.LocalCLIDebugWrapperSession(sess)
K.set_session(sess)

from sklearn.multioutput import MultiOutputRegressor

env = gym.make('LunarLander-v2')
de = DataExtractor(env,get_real_obs_for_luner_lander,RandomLunarAgent())
cache_de = CachingExtractorDecorator(de)
regressor1 = xgboost.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1, max_depth = 5, alpha = 10, n_estimators = 100)

ANGLE = 4
ANGULAR_VEL = 5
ACTION = 8
sub_target = ANGULAR_VEL
test_data = cache_de.get_data(1000, 100).sub_target_dataset(sub_target)
val_data = cache_de.get_data(2000, 100).sub_target_dataset(sub_target)
train_data = cache_de.get_data(3000, 100).sub_target_dataset(sub_target)

def run_training():
    from sklearn import datasets, linear_model
    from sklearn.model_selection import cross_val_score, KFold
    from keras.models import Sequential
    from sklearn.metrics import accuracy_score
    from keras.layers import Dense
    from keras.wrappers.scikit_learn import KerasRegressor
    from keras_contrib.callbacks import CyclicLR

    def baseline_model():
        model = Sequential()
        model.add(Dense(20, input_dim=12, activation='relu'))
        model.add(Dense(1))
        clr = tfa.optimizers.CyclicalLearningRate(initial_learning_rate=0.001,
                                                  maximal_learning_rate=0.01,
                                                  scale_fn=lambda x: 1.,
                                                  scale_mode="cycle",
                                                  step_size=10
                                                  )
        adam = tf2.optimizers.Adam(clr)
        model.compile(loss='mean_squared_error', optimizer=tf2.optimizers.SGD())
        return model

    nnRegressor = KerasRegressor(build_fn=baseline_model, epochs=10, batch_size=4,
                                 validation_data=(val_data.x, val_data.y),
                                 verbose=True,
                                 # callbacks = [tensorboard_callback]
                                 )

    nnRegressor.fit(train_data.x, train_data.y)

    train_pred = nnRegressor.predict(train_data.x)
    train_errors = train_data.y - train_pred
    test_pred = nnRegressor.predict(test_data.x)
    errors = test_data.y - test_pred


def main(_):
  # Create a dummy dataset.
  num_examples = 8
  steps_per_epoch = 2
  input_dims = 3
  output_dims = 1
  xs = np.zeros([num_examples, input_dims])
  ys = np.zeros([num_examples, output_dims])
  dataset = tf.data.Dataset.from_tensor_slices(
      (xs, ys)).repeat(num_examples).batch(int(num_examples / steps_per_epoch))

  sess = tf.Session()
  if FLAGS.debug:
    # Use the command-line interface (CLI) of tfdbg.
    config_file_path = (
        tempfile.mktemp(".tfdbg_config")
        if FLAGS.use_random_config_path else None)
    sess = tf_debug.LocalCLIDebugWrapperSession(
        sess, ui_type=FLAGS.ui_type, config_file_path=config_file_path)
  elif FLAGS.tensorboard_debug_address:
    # Use the TensorBoard Debugger Plugin (GUI of tfdbg).
    sess = tf_debug.TensorBoardDebugWrapperSession(
        sess, FLAGS.tensorboard_debug_address)
  tf.keras.backend.set_session(sess)

  run_training()

  # Create a dummy model.
  # model = tf.keras.Sequential(
  #     [tf.keras.layers.Dense(1, input_shape=[input_dims])])
  # model.compile(loss="mse", optimizer="sgd")
  #
  # # Train the model using the dummy dataset created above.
  # model.fit(dataset, epochs=FLAGS.epochs, steps_per_epoch=steps_per_epoch)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  parser.add_argument(
      "--debug",
      type="bool",
      nargs="?",
      const=True,
      default=False,
      help="Use debugger to track down bad values during training. "
      "Mutually exclusive with the --tensorboard_debug_address flag.")
  parser.add_argument(
      "--ui_type",
      type=str,
      default="curses",
      help="Command-line user interface type (curses | readline).")
  parser.add_argument(
      "--use_random_config_path",
      type="bool",
      nargs="?",
      const=True,
      default=False,
      help="""If set, set config file path to a random file in the temporary
      directory.""")
  parser.add_argument(
      "--tensorboard_debug_address",
      type=str,
      default=None,
      help="Connect to the TensorBoard Debugger Plugin backend specified by "
      "the gRPC address (e.g., localhost:1234). Mutually exclusive with the "
      "--debug flag.")
  parser.add_argument(
      "--epochs",
      type=int,
      default=2,
      help="Number of epochs to train the model for.")
  FLAGS, unparsed = parser.parse_known_args()
  with tf.Graph().as_default():
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)