import pickle

from multiclass_perceptron_network import MulticlassPerceptronNetwork
from internal_state import InternalState


class DecisionByPredictionBlock:
    """ The DecisionByPredictionBlock is a class aimed at modeling how decisions can be
    made through prediction. The brain seems to simulate a world and internal (self) model
    in order to predict the outcomes of the different options it is faced to. The decision is
    thus made by selecting the option that produces the closest outcome to a desired world and
    internal state """

    # INPUTS NUMBER
    INPUTS_NUMBER = 3
    # Input size (Each input's number of variables)
    INPUT_SIZE = 3
    # Internal state size
    INTERNAL_STATE_SIZE = 3
    #
    OUTPUT_SIZE = 3

    def __init__(self):
        # Create multiclass perceptron network with input size equal to
        # the size of a BCF(input size) plus the size of the internal state
        self.predictive_net = MulticlassPerceptronNetwork( DecisionByPredictionBlock.INPUT_SIZE
                                                         + DecisionByPredictionBlock.INTERNAL_STATE_SIZE,
                                                         DecisionByPredictionBlock.OUTPUT_SIZE)
        self.desired_state = None
        self.inputs = None
        self.output = None
        self.internal_state = None
        # Vector of predicted outcomes for the given inputs
        self.predicted_outcomes = None
        # Vector of calculated distances between the predicted outcomes and
        # the desired state
        self.distances = None

    def set_desired_state(self, desired_state):
        if isinstance(desired_state, InternalState):
            self.desired_state = desired_state
            return True
        return False

    def get_desired_state(self):
        return self.desired_state

    def set_inputs(self, inputs):
        if len(inputs) != DecisionByPredictionBlock.INPUTS_NUMBER:
            return False
        self.inputs = inputs

    def get_inputs(self):
        return self.inputs

    def get_output(self):
        self._make_decision()
        return self.output

    def get_predicted_outcomes(self):
        return self.predicted_outcomes

    def get_distances(self):
        return self.distances

    def set_internal_state(self, internal_state):
        if isinstance(internal_state, InternalState):
            self.internal_state = internal_state
            return True
        return False

    def remodel_predictive_net(self, training_set):
        self.predictive_net.training(training_set)

    def _make_decision(self):
        # No decision is made if there is lack of information
        if self.inputs is None or self.desired_state is None or self.internal_state is None:
            return False
        predicted_outcomes = []
        for input in self.inputs:
            net_input = self.internal_state.get_state() + input
            self.predictive_net.set_inputs(net_input)
            predicted_outcomes.append( self.predictive_net.get_outputs() )
        decision = self._select_from_predicted_outcomes(predicted_outcomes)
        self.output = decision
        self.predicted_outcomes = predicted_outcomes
        return True

    def _select_from_predicted_outcomes(self, predicted_outcomes):
        """ Select the closest outcome to desired state
        :param predicted_outcomes: set of predictive_net outcomes to input vector
        :return: index of predicted_outcome
        """
        self.distances = []
        for outcome in predicted_outcomes:
            distance = 0
            for outcome_j, desired_j in zip(outcome,self.desired_state.get_state()):
                distance += abs(desired_j-outcome_j)
            self.distances.append(distance)
        return self.distances.index(min(self.distances))

# Tests
if __name__ == '__main__':

    import random

    desired_state = InternalState()
    desired_state.set_state([0.5,1,1])
    internal_state = InternalState({'biology': 0.5, 'culture': 0.5, 'feelings': 0.5})

    decision_prediction = DecisionByPredictionBlock()
    decision_prediction.set_desired_state(desired_state)

    # Create a random training set so that the net can learn the relation prediction = (ei + choice.bcf)/2
    # We require a minimum of 18 points
    training_set = []
    for index in range(10):
        ei = [random.random(), random.random(), random.random() ]
        choice_bcf = [ random.random(), random.random(), random.random()]
        prediction = [ ei_j/2.0 + choice_bcf_j/2.0 for ei_j, choice_bcf_j in zip(ei, choice_bcf) ]
        training_set.append( (ei + choice_bcf, prediction ) )

    decision_prediction.remodel_predictive_net(training_set)

    decision_prediction.set_internal_state(internal_state)
    decision_prediction.inputs = [[0.5, 0.9, 0.2],[0.5, 0.9, 0.3],[0.4, 0.7, 0.9]]

    print "Decision = ", decision_prediction.get_output()
    print "Distances = ", decision_prediction.distances
    print "Predicted outcomes = ", decision_prediction.predicted_outcomes
    print "Weights = ", decision_prediction.predictive_net.weights

    # Weights to posibly be used as starting points for the brainCEMISID
    # Weights =  [[0.18812028041881285, 0.13849727997709485, 0.1381004345719828, 0.14446560005017783,
    # 0.12956668791495393, 0.12336769506630386],
    # [0.1455684236435773, 0.12788199329931116, 0.10319785645118171, 0.11201382530597757, 0.13567769257922965,
    # 0.08704799225129042],
    # [0.14427679571022395, 0.12150567866945464, 0.2118510950796081, 0.13439692578417978, 0.0900649700576292,
    # 0.17960324138197806]]
