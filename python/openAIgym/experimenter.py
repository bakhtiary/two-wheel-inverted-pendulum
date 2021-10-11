import matplotlib.pyplot as plt

import numpy as np, scipy.stats as st

# def get_test_results_for_seed():
class ExperimenterRunner:
    def __init__(self, regressor, de):
        self.regressor = regressor
        self.data_extractor = de
        self.number_of_runs = 10

        self.data = {}
        self.train_errors = None
        self.errors = None
        self.number_of_train_episodes = 40

    def _get_errors_for_seed(self, i):
      train_dataX, train_dataY = self.data_extractor.get_data(10000+i*50, self.number_of_train_episodes)
      test_dataX, test_dataY = self.data_extractor.get_data(1+i, 1)
      self.data[i] = train_dataX, train_dataY, test_dataX, test_dataY

      self.regressor.fit(train_dataX, train_dataY)

      train_pred = self.regressor.predict(train_dataX)
      train_errors = train_dataY-train_pred
      test_pred = self.regressor.predict(test_dataX)
      errors = test_dataY-test_pred

      return errors, train_errors

    def compute_errors(self):
        self.errors = []
        self.train_errors = []
        for i in range(self.number_of_runs):
            test_error, train_error = self._get_errors_for_seed(i)
            self.errors.append(test_error)
            self.train_errors.append(train_error)



class ExperimentPlotter:

    def __init__(self, error_function):
        self.error_function = error_function

    def _conf_interval_for_step(self, errors_for_step_n):

        mean = np.mean(errors_for_step_n, axis=0)
        conf = st.t.interval(0.95, len(errors_for_step_n) - 1, loc=np.mean(errors_for_step_n, axis=0),
                             scale=st.sem(errors_for_step_n, axis=0))
        return mean, conf

    def get_errors_for_step_n(self, errors, n):
        errors_for_step_n = [x[n] for x in errors if len(x) > n]
        errors_for_step_n = self.error_function(errors_for_step_n)
        return errors_for_step_n

    def plot_errors_for_state(self, errors, state_idx, steps):
        all_errors_for_step_n = []
        for i in range(steps):
            all_errors_for_step_n.append(self.get_errors_for_step_n(errors, i))


        means = []
        confs = []
        for errors_for_step_n in all_errors_for_step_n:
            mean, conf = self._conf_interval_for_step(errors_for_step_n)
            means.append(mean)
            confs.append(conf)

        x1 = list(range(len(means)))

        y1 = [x[state_idx] for x in means]
        y2 = [x[0][state_idx] for x in confs]
        y3 = [x[1][state_idx] for x in confs]

        fig, ax1 = plt.subplots(1, 1)
        fig.suptitle('error wrt time step')

        ax1.plot(x1, y1, 'o-')
        ax1.plot(x1, y2, 'o-')
        ax1.plot(x1, y3, 'o-')
        ax1.set_ylabel('error')

        plt.show()

    def plot_paired_errors_for_state(self, exp_errors_1, exp_errors_2, state_idx, steps):
        means = []
        confs = []
        for i in range(steps):
            error1 = self.get_errors_for_step_n(exp_errors_1, i)
            error2 = self.get_errors_for_step_n(exp_errors_2, i)
            error_diff = error2-error1
            mean, conf = self._conf_interval_for_step(error_diff)
            means.append(mean)
            confs.append(conf)

        x1 = list(range(len(means)))

        y1 = [x[state_idx] for x in means]
        y2 = [x[0][state_idx] for x in confs]
        y3 = [x[1][state_idx] for x in confs]

        fig, ax1 = plt.subplots(1, 1)
        fig.suptitle('error wrt time step')

        ax1.plot(x1, y1, 'o-')
        ax1.plot(x1, y2, 'o-')
        ax1.plot(x1, y3, 'o-')
        ax1.set_ylabel('error')

        plt.show()