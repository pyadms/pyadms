

# need to do something with keeping accessors?  or derivate takers
# worry about zero elimation, subexpression, etc
# collect tokens into base
class expression_base:

    def __init__(self, **kwargs):
        pass


class add(expression_base):
    __slots__ = ('args')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = kwargs['args']

    def get_expression(self):
        e = [a.get_expression() for a in self.args]
        return ' + '.join(t)

    def get_derivative(self, arg):
        # zero elimination later
        d = [a.get_derivative(arg).expression() for a in self.args]
        return ' + '.join(t)


class multiply(expression_base):
    __slots__ = ('args')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = kwargs['args']

    def get_expression(self):
        t = [a.get_expression() for a in self.args]
        return ' * '.join(t)

    def get_derivative(self, arg):
        # zero elimination later
        # one multiple elimination
        # (a*b*c)' = a'*(b*c) + b'*(a*c)+c'*(a*b)
        e = [a.get_expression() for a in self.args]
        d = [a.get_derivative(arg).expression() for a in self.args]
        o = []

        for i, ld in enumerate(d):
            le =e[:]
            le[i] = ld
            o.append(' * '.join(le))
        return ' * '.join(o)

