import pickle

from biclass_perceptron_network import BiclassPerceptronNetwork


class ConsciousDecisionsBlock():
    """ The Conscious Decisions Block is in charge of 'rationally' evaluating
     current internal state and goals in order to make decisions. The quotes in
     'rationally' stand for the agent trying to choose what he thinks is the best
     course of action according to past experiences, but not what is really
     best in the mathematical sense (objective function). The result from
     the last decision taken can be fed back for evaluation and evolution of its
     behaviour """

    INPUT_SIZE = 9

    def __init__(self):
        self.rational_net = BiclassPerceptronNetwork(ConsciousDecisionsBlock.INPUT_SIZE)
        self.inputs = None
        self.output = None

