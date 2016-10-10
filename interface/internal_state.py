import pickle


class BiologyCultureFeelings:
    # Number of variables = 3 (Biology, Culture, Feelings)
    VARIABLES_NUMBER = 3

    def __init__(self, initial_state={'biology': 0.5, 'culture': 0, 'feelings': 1}):
        self.state = initial_state
        return

    def get_biology(self):
        return self.state['biology']

    def get_culture(self):
        return self.state['culture']

    def get_feelings(self):
        return self.state['feelings']

    def set_biology(self, val):
        """ Set biology value as 'val'
        :param val: real number between 0 and 1
        :return:
        """
        if 0 <= val <= 1:
            self.state['biology'] = val
            return True
        return False

    def set_culture(self, val):
        """ Set culture value as 'val'
        :param val: real number between 0 and 1
        :return:
        """
        if 0 <= val <= 1:
            self.state['culture'] = val
            return True
        return False

    def set_feelings(self, val):
        """ Set feelings value as 'val'
        :param val: real number between 0 and 1
        :return:
        """
        if 0 <= val <= 1:
            self.state['feelings'] = val
            return True
        return False

    def set_state(self, vals):
        if len(vals) != BiologyCultureFeelings.VARIABLES_NUMBER:
            return False
        return self.set_biology(vals[0]) and self.set_culture(vals[1]) and self.set_feelings(vals[2])

    def get_state(self):
        return [self.get_biology(), self.get_culture(), self.get_feelings()]


class InternalState(BiologyCultureFeelings):
    """ This class represents a very simplified version of an entity's
    internal state. It is a type of BCF, because such state has biological,
    cultural and emotional (here reduced to its less primitive and reflected
    counterpart 'feelings') components. Average methods are added to model"""

    BIOLOGY_UPPER_THRESHOLD = 0.8
    BIOLOGY_LOWER_THRESHOLD = 0.2

    def __init__(self, initial_state=None):
        if initial_state is None:
            BiologyCultureFeelings.__init__(self)
        else:
            BiologyCultureFeelings.__init__(self, initial_state)
        """
        :param initial_state: class BiologyCultureFeelings (BCF)
        """

    def average_biology(self, val):
        if val < 0 or val > 1:
            return False
        self.state['biology'] = (self.state['biology'] + val) / 2.0
        return True

    def average_culture(self, val):
        if val < 0 or val > 1:
            return False
        self.state['culture'] = (self.state['culture'] + val) / 2.0
        return True

    def average_feelings(self, val):
        if val < 0 or val > 1:
            return False
        self.state['feelings'] = (self.state['feelings'] + val) / 2.0
        return True

    def biology_alarm(self):
        if (self.state['biology'] >= InternalState.BIOLOGY_UPPER_THRESHOLD or
                self.state['biology'] <= InternalState.BIOLOGY_LOWER_THRESHOLD):
            return True
        return False

    def biology_up_alarm(self):
        if self.state['biology'] >= InternalState.BIOLOGY_UPPER_THRESHOLD:
            return True
        return False

# Tests
if __name__ == '__main__':
    ie = InternalState()
    print ie.state

    ie.set_biology(1)
    ie.set_culture(1)
    ie.set_feelings(1)
    print ie.state

    ie.average_biology(0)
    ie.average_culture(0.25)
    ie.average_feelings(0.5)
    print ie.state
