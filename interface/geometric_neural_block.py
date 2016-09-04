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

    def compare(self, knowledge):
        if self._has_order:
            return knowledge == self._order_neuron.get_knowledge()
        return False


class QuantityOrderNetwork:
    def __init__(self):
        self.group_list = []
        self._index = 0

    def bum(self):
        self._index = 0

    def bip(self):
        if len(self.group_list) <= self._index:
            self.group_list.append(QuantityOrderGroup())
        self._index += 1

    def clack(self, knowledge=None):
        if not self.group_list[self._index-1].has_order():
            if knowledge is None:
                raise ValueError("GeometricNeuralBlock: a kind of order knowledge must be passed")
            self.group_list[self._index-1].clack(knowledge)
        return self.group_list[self._index-1].get_order()

    def get_bip_count(self, knowledge):
        for index in range(len(self.group_list)):
            if self.group_list[index].compare(knowledge):
                return index+1
        return None


class AdditionStructure:
    def __init__(self):
        self.neurons = [Neuron() for i in range(10)]
        self.carry_over = False
        self.index = 0

    def bum(self):
        if self.carry_over:
            self.index = 1
            self.carry_over = False
        else:
            self.index = 0

    def bip(self):
        self.index += 1
        if self.index >= len(self.neurons):
            self.index = 0
            self.carry_over = True

    def clack(self):
        return self.index

    def has_carry(self):
        return self.carry_over

    def clear_carry(self):
        self.carry_over = False


class GeometricNeuralBlock:
    def __init__(self):
        # Quantity-Order and Addition Structures
        self._order_structure = QuantityOrderNetwork()
        self._addition_structure = AdditionStructure()
        # Default operation
        self._operation = "COUNT"
        # Queues for operands
        self._op1_queue = []
        self._op2_queue = []
        # Operator
        self._operator = None
        # Sum operator
        self._add_operator = None
        # Equal sign
        self._equal_sign = None

    def set_operation(self, operation):
        if operation == "COUNT":
            self._operation = "COUNT"
        elif operation == "ADD":
            self._operation = "ADD"
        else:
            raise ValueError("invalid operation")

    def get_operation(self):
        return self._operation

    def set_add_operator(self, knowledge):
        self._add_operator = knowledge

    def get_add_operator(self):
        return self._add_operator

    def set_equal_sign(self, knowledge):
        self._equal_sign = knowledge

    def get_equal_sign(self):
        return self._equal_sign

    def set_zero(self, knowledge):
        self._zero = knowledge

    def bum(self):
        if self._operation == "COUNT":
            self._bum_count()
        elif self._operation == "ADD":
            self._bum_add()
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
        elif self._operation == "ADD":
            self._bip_add(knowledge)
            # Add here future operations
        else:
            return

    def _bum_count(self):
        self._order_structure.bum()

    def _bip_count(self):
        self._order_structure.bip()

    def _clack_count(self, knowledge):
        self._order_structure.clack(knowledge)

    def _bum_add(self):
        self._addition_structure.bum()
        self._op1_queue = []
        self._op2_queue = []
        self._operator = None

    def _bip_add(self, knowledge):

        # if knowledge correspond to some operator, store in _operator attribute
        if knowledge == self._add_operator:
            self._operator = knowledge
        elif knowledge == self._equal_sign:
            self._check_add(knowledge)
        # Else if the oprator has not been introduced yet, knowledge is part of first operand
        elif self._operator is None:
            self._op1_queue.append(knowledge)
        # Else it is part of second operand
        else:
            self._op2_queue.append(knowledge)

    def _check_add(self, knowledge):
        # If the given knowledge corresponds to what the brain understands to be an equal sign
        if knowledge == self._equal_sign:
            # If the given operator corresponds to what the brain knows that is an addition operator, add
            if self._operator == self._add_operator:
                return self._add()
        else:
            return False

    def _add(self):
        addition_result = []
        # While there is a digit to be added
        while len(self._op1_queue) != 0 or len(self._op2_queue) != 0:
            # Get first operand
            if len(self._op1_queue) != 0:
                digit_op_1 = self._op1_queue.pop()
            else:
                digit_op_1 = self._zero
            # Get second operand
            if len(self._op2_queue) != 0:
                digit_op_2 = self._op2_queue.pop()
            else:
                digit_op_2 = self._zero

            # Get bip count of operands
            bip_count_1 = self._get_bip_count(digit_op_1)
            bip_count_2 = self._get_bip_count(digit_op_2)

            # Validate
            if bip_count_1 is None or bip_count_2 is None:
                raise ValueError("An operand cannot be recognized")

            # Add using addition_structure
            self._addition_structure.bum()
            for index in range(bip_count_1):
                self._addition_structure.bip()
            for index in range(bip_count_2):
                self._addition_structure.bip()
            addition_result.append(self._addition_structure.clack())

        if self._addition_structure.has_carry():
            self._addition_structure.bum()
            addition_result.append(self._addition_structure.clack())

        self.addition_result = []
        for digit in addition_result:
            # The zero is a special concept to be addressed possibly in future versions
            if digit == 0:
                self.addition_result.append(self._zero)
            # For the rest of digits, use the Quantity-order structure
            else:
                self._order_structure.bum()
                for i in range(digit):
                    self._order_structure.bip()
                digit_representation = self._order_structure.clack().get_knowledge()
                self.addition_result.append(digit_representation)

    def _get_bip_count(self, digit ):
        if digit == self._zero:
            return 0
        return self._order_structure.get_bip_count(digit)

    def _get_operand_1(self):
        if len(self._op1_queue) != 0:
            return self._op1_queue.pop()
        return self._zero

    def _get_operand_2(self):
        if len(self._op2_queue) != 0:
            return self._op2_queue.pop()
        return self._zero

    def get_addition_result(self):
        return self.addition_result


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

    # Geometric Neural Block
    gnb = GeometricNeuralBlock()

    # Start count
    gnb.bum()
    gnb.bip()
    gnb.clack('1')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.clack('2')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('3')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('4')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('5')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('6')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('7')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('7')

    gnb.bum()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.bip()
    gnb.clack('9')


    gnb.set_add_operator('+')
    gnb.set_equal_sign('=')
    gnb.set_zero('0')

    gnb.set_operation("ADD")

    gnb.bum()
    gnb.bip('2')
    gnb.bip('+')
    gnb.bip('1')
    gnb.bip('=')

    print gnb.get_addition_result()

    gnb.bum()
    gnb.bip('5')
    gnb.bip('2')
    gnb.bip('6')
    gnb.bip('+')
    gnb.bip('5')
    gnb.bip('7')
    gnb.bip('4')
    gnb.bip('=')
    print gnb.get_addition_result()
