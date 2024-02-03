

# need to do something with keeping accessors?  or derivate takers
# worry about zero elimation, subexpression, etc
# collect tokens into base
class expression_base:

    def __init__(self, *args, **kwargs):
        pass

class add(expression_base):
    __slots__ = ('args',)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.args = args[:]

    def get_expression(self):
        e = [a.get_expression() for a in self.args]
        return ' + '.join(t)

    def get_derivative(self, arg):
        # zero elimination later
        d = [a.get_derivative(arg).expression() for a in self.args]
        return ' + '.join(t)


class multiply(expression_base):
    __slots__ = ('args')

    def __init__(self, *args):
        super().__init__(**kwargs)
        self.args = args

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

class numeric_constant(expression_base):
    __slots = ('numeric_value', 'string_value')

    def __init__(self, numeric_value, string_value)
        self.numeric_value = numeric_value
        self.string_value = string_value

    def get_expression(self):
        return self.string_value

    def get_derivative(self, arg):
        return None


# implement derivative of generic function call here
# d_arg1, d_arg2, d_arg3 ... are derivatives with respect to each positional argument
# use the chain rule to resolve derivatives with respect to arbitrary parameter
# use None in position for which no derivative is exists
# maybe: make it possible to substitute an expression for derivatives instead of function
# maybe: use symdiff to generate expression functions
