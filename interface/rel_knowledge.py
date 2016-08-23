class RelKnowledge:

    def __init__(self, h_id, s_id, weight = 0):
        """ Create RelKnowledge instance given
        a hearing id (id_h), sight id (id_s) and weight which defaults to zero"""
        self.set_h_id(h_id)
        self.set_s_id(s_id)
        self.set_weight(weight)

    def set_h_id(self, h_id):
        """ Set hearing id """
        self._h_id = h_id

    def set_s_id(self, s_id):
        """ Set sight id """
        self._s_id = s_id

    def set_weight(self, w ):
        """ Set weight """
        if w >= 0:
            self._weight = w
        else:
            raise ValueError("Invalid value for w")

    def increase_weight(self, amount=1 ):
        """ Increase weight of relation by the amount given as a parameter. The default amount value is 1 """
        if self._weight + amount >= 0:
            self._weight += amount

    def get_h_id(self):
        """ Get hearing id """
        return self._h_id

    def get_s_id(self):
        """ Get sight id """
        return self._s_id

    def get_weight(self):
        """ Get relation weight """
        return self._weight

    def is_equal_hearing(self, h_id):
        """ Return true if knowledge's hearing id is equal to given parameter h_id and
        false in any other case """
        return self._h_id == h_id

    def is_equal_sight(self, s_id):
        """ Return true if knowledge sight id is equal to given parameter s_id and
        false in any other case """
        return self._s_id == s_id

    def is_equal(self, h_id, s_id):
        """ Return true if knowledge's sight id is equal to given parameter s_id and
                knowledge's hearing id is equal to given parameter h_id. Return false in any other case """
        return self._h_id == h_id and self._s_id == s_id

