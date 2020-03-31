from lib.perceptron_helper import *


class Perceptron():

    def __init__(self, epoch_threshold=100, l_rate=1, batch_size=1):
        self.weights = np.random.uniform(size=4)
        self.epoch_threshold = epoch_threshold
        self.l_rate = l_rate
        self.batch_size = batch_size
        pass

    ###
    def compute(self, x, y, weights):
        """
        Fully vectorized function to compute the product between weights, feature vector and true label
        """

        y_compute = np.dot(x, weights) * y
        return y_compute

    def fit(self, train, labels, init_weights=None, l_rate=None, batch_size=None, epoch_threshold=None, verbose=False):
        """
        Function to train the perceptron model and update the weights

        :param train: Array of input to train the model on
        :param labels: Array of output labels for loss computation
        :param init_weights:
        :param l_rate:
        :param batch_size:
        :param epoch_threshold:
        :param verbose:
        :return:
        """

        epoch = 0

        if init_weights is None : weights = self.weights
        else : weights = init_weights
        if l_rate is None : l_rate = self.l_rate
        if batch_size is None : batch_size = self.batch_size
        if epoch_threshold is None: epoch_threshold = self.epoch_threshold

        train_batches = make_batches(train, batch_size, 0)
        label_batches = make_batches(labels, batch_size, 0)

        print("Number of batches formed: ", len(train_batches))
        print()

        while epoch <= epoch_threshold:
            total_miss_class = 0
            for tbatch, lbatch, batch_num in zip(train_batches, label_batches, range(len(train_batches) + 1)):
                computed_value = self.compute(tbatch, lbatch, weights)
                miss_class = len(tbatch[computed_value < 0])
                total_miss_class += miss_class

                # Filtering for the miss classified samples using computed_value
                weights_update = l_rate * np.dot(lbatch[computed_value < 0], tbatch[computed_value < 0])
                weights = weights + weights_update
                if verbose is True:
                    print("---> epoch : %d | batch : %d | Misclassified : %d" % (epoch, batch_num, miss_class))
            print("Summary of epoch : %d | Total batches : %d | Total Misclassified : %d" \
                  % (epoch, batch_num + 1, total_miss_class))
            if total_miss_class == 0: break

            epoch += 1

        print()
        print("\nClassification Hyperplane : %.2fx + %.2fy + %.2fz + %.2f" % tuple(weights))

        return weights, epoch + 1


    def predict(self, test):

