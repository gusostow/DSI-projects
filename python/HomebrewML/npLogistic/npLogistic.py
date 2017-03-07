import numpy as np


#helper functions
def sigmoid(x):

    return 1 / (1 + np.exp(-1 * x))



class BinaryLogistic(object):

    def __init__(self):

        self.fitted = False


    def getGrad(self, X, y, w):
        N = self.X.shape[0]

        #initialize empty vector for gradient
        grad = np.zeros(w.shape[0])

        delta = y - sigmoid(np.dot(X, w))

        for i in range(grad.size):
            grad[i] = (-1.0 / N) * np.dot(delta.T, X[:, i])

        return grad


    def fit(self, X, y, lr = 1, e = 0.01):
        """
        Compute optimal parameters for Logistic Regression using gradient descent

        Inputs
            X: Numpy array of numeric or dummy coded predictor columns
            y: Binary outcome column
            lr: gradient descent learning rate
            e: convergance criterion
        Output
            None
        """
        #initialize global variables
        self.X = X
        self.y = y
        self.lr = lr
        self.e = e

        self.w = np.random.random(self.X.shape[1])

        update_norm = np.inf
        epoch = 0

        while update_norm > self.e:

            grad = self.getGrad(self.X, self.y, self.w)
            update =  -1 * self.lr * grad
            self.w += update
            epoch += 1
            update_norm = np.linalg.norm(update)
            if epoch > 1000:
                break

        self.fitted = True

        print "Parameters were optimized after", epoch, "epochs!"


    def predict_proba(self, X):
        if not self.fitted:
            raise Exception("Warning: Parameters have not yet been fit on training data")

        proba = sigmoid(np.dot(X, self.w))

        return proba


    def predict(self, X):

        if not self.fitted:
            raise Exception("Warning: Parameters have not yet been fit on training data")

        proba = sigmoid(np.dot(X, self.w))

        #identify probabilities that would lead to positive classification
        mask = proba >= 0.5

        predictions = np.where(mask, np.ones(mask.size), np.zeros(mask.size))

        return predictions


