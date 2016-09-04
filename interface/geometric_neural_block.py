import pickle

class Neuron():
    def __init__(self, knowledge=None):
        if knowledge == None:
            self._has_knowledge = False
            self._knowledge = None
        else:
            self.set_knowledge(knowledge)

    def set_knowledge(self, knowledge):
        self._has_knowledge = True
        self._knowledge = knowledge

    def get_knowledge(self):
        return self._knowledge

    def has_knowledge(self):
        return self._has_knowledge


class QuantityNeuron(Neuron):
    pass


class OrderNeuron(Neuron):
    pass


class QuantityOrderGroup:
    def __init__(self):
        self._has_order = False
        self._order_neuron = None
        self._quantity_neuron = QuantityNeuron()

    def clack(self, knowledge):
        self._order_neuron = OrderNeuron(knowledge)
        self._has_order = True

    def get_order(self):
        return self._order_neuron

    def has_order(self):
        return self._has_order

class QuantityOrderNetwork:
    def __init__(self):
        self.group_list = []
        self._index = 0

    def bum(self):
        if len(self.group_list) == 0:
            self.group_list.append(QuantityOrderGroup())
        self._index = 0

    def bip(self):
        self._index += 1
        if len(self.group_list) <= self._index:
            self.group_list.append(QuantityOrderGroup())

    def clack(self, knowledge=None):
        if not self.group_list[self._index].has_order():
            if knowledge == None:
                raise ValueError("GeometricNeuralBlock: a kind of order knowledge must be passed")
            self.group_list[self._index].clack(knowledge)
        return self.group_list[self._index].get_order()


class AdditionStructure:
    def __init__(self):
        self.neurons = [Neuron() for i in range(10)]
        self.carry_over = Neuron(knowledge=False)
        self.index = 0

    def bum(self):
        self.carry_over.set_knowledge(False)
        self.index = 0

    def bip(self):
        self.index += 1
        if self.index >= len(self.neurons):
            self.index = 0
            self.carry_over.set_knowledge(True)

    def clack(self):
        return self.index

    def has_carry(self):
        return self.carry_over.get_knowledge()

    def clear_carry(self):
        self.carry_over.set_knowledge(False)


class GeometricNeuralBlock:
    def __init__(self):
        # Quantity-Order and Addition Structures
        self._order_structure = QuantityOrderNetwork
        self._addition_structure = AdditionStructure
        # Default operation
        self._operation = "COUNT"

    def set_operation(self, operation):
        if operation == "COUNT":
            self._operation = "COUNT"
        elif operation == "ADD":
            self._operation = "ADD"
        else:
            raise ValueError("invalid operation")

    def get_operation(self):
        return self._operation

    def bum(self, knowledge=None):
        if self._operation == "COUNT":
            self._bum_count()
        elif self._operation == "ADD":
            self._bum_add(knowledge)
        # Add here future operations
        else:
            return

    def bip(self, knowledge=None):
        if self._operation == "COUNT":
            self._bip_count()
        elif self._operation == "ADD":
            self._bip_add(knowledge)
        # Add here future operations
        else:
            return

    def clack(self, knowledge=None):
        if self._operation == "COUNT":
            self._clack_count(knowledge)
        # Add here future operations
        else:
            return

    def _bum_count(self):
        self._order_structure.bum()

    def _bip_count(self):
        self._order_structure.bip()

    def _clack_count(self, knowledge):
        self._order_structure.clack(knowledge)

    def _bum_add(self, knowledge):
        self._op1_queue = []
        self._op2_queue = []
        self._operator = None
        self._op1_queue.append(knowledge)
        return

    def _bip_add(self, knowledge):
        return



# Tests
if __name__ == '__main__':

    net = QuantityOrderNetwork()

    net.bum()
    net.bip()
    net.clack(2)

    net.bum()
    net.bip()
    net.bip()
    net.bip()
    net.bip()
    net.clack(5)

    net.bum()
    net.bip()
    quantity_1 = net.clack().get_knowledge()
    net.bum()
    net.bip()
    net.bip()
    net.bip()
    net.bip()
    quantity_2 = net.clack().get_knowledge()

    print "Quantity 1 is: ", quantity_1
    print "Quantity 2 is: ", quantity_2

    # AdditionStructure

    print "Adition Struture:  "
    add_s = AdditionStructure()
    add_s.bum()
    for i in range(15):
        add_s.bip()
    if add_s.has_carry():
        print "1", add_s.clack()
    else:
        print add_s.clack()