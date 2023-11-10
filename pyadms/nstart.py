

class admst:
    all_data = None

    def __init__(self, **kwargs):
        for x in ['datatypename', 'id', 'uid', 'attributes', 'parameters', 'references']:
            self.__dict__[x] = kwargs[x]
            del kwargs[x]
        self.kwargs = kwargs

    def move_up_parameter(self, kw):
        self.__dict__[kw] = self.parameters.pop(kw)
        if len(self.parameters) == 0:
            self.parameters = None

    def move_up_reference(self, kw, single=False):
        if single:
            slen = len(self.references[kw])
            if slen > 1:
                raise RuntimeError(f"not expecting moving up only 1 reference for {kw}")
            elif slen == 0:
                self.__dict__[kw] = None
            else:
                self.__dict__[kw] = self.references.pop(kw)[0]
        else:
            self.__dict__[kw] = self.references.pop(kw)
        if len(self.references) == 0:
            self.references = None

class admsmain(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class analog(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('code')

class assignment(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'lhs', 'rhs', 'lexval'):
            self.move_up_reference(x, True)

class block(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # this is the parent block of this block
        for x in ('module', 'lexval', 'block'):
            self.move_up_reference(x, True)
        self.move_up_reference('item')

class branch(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'pnode', 'nnode', 'discipline'):
            self.move_up_reference(x, True)

class branchalias(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        for x in ('module', 'branch'):
            self.move_up_reference(x, True)

class conditional(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'if', 'then', 'else'):
            self.move_up_reference(x, True)

class contribution(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'lhs', 'rhs', 'branchalias'):
            self.move_up_reference(x, True)

class discipline(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['name', 'domain']:
            self.move_up_parameter(x)
        for x in ('flow', 'potential'):
            self.move_up_reference(x, True)

class expression(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('tree',):
            self.move_up_reference(x, True)

class function(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('unique_id')
        for x in ('lexval', 'definition'):
            self.move_up_reference(x, True)
        self.move_up_reference('arguments')

class lexval(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('string')

class mapply_binary(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = [self.references[x][0] for x in ['arg1', 'arg2']]
        self.move_up_parameter('name')

class mapply_ternary(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = [self.references[x][0] for x in ['arg1', 'arg2', 'arg3']]
        self.move_up_parameter('name')

class mapply_unary(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = [self.references[x][0] for x in ['arg1',]]
        self.move_up_parameter('name')

class module(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in [
            "analog",
            "node",
            "nodealias",
            "branch",
            "branchalias",
            "analogfunction",
            "instance",
            "variable",
            "block",
            "blockvariable",
            "assignment",
            "callfunction",
            "contribution",
            "conditional",
            "case",
            "forloop",
            "whileloop",
            "expression",
            "probe",
            "source",
            "range",
            "attribute",
            ]:
            self.move_up_reference(x)

class nature(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['access', 'name', 'ddt_name', 'idt_name', 'units']:
            self.move_up_parameter(x)
        for x in ('abstol', 'base', 'ddt_nature', 'idt_nature'):
            self.move_up_reference(x, True)

class nilled(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class node(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['name', 'direction', 'location']:
            self.move_up_parameter(x)
        for x in ('module', 'discipline'):
            self.move_up_reference(x, True)

class nodealias(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        for x in ('module', 'node'):
            self.move_up_reference(x, True)

class number(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['scalingunit', 'cast']:
            self.move_up_parameter(x)
        self.move_up_reference('lexval', True)

class probe(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'branch', 'nature'):
            self.move_up_reference(x, True)

class range(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'infexpr', 'supexpr'):
            self.move_up_reference(x, True)
        for x in ('name', 'infboundtype', 'supboundtype', 'type'):
            self.move_up_parameter(x)

class simulator(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class source(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'branch', 'nature'):
            self.move_up_reference(x, True)

class string(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('value')

class variable(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('prototype', True)

class variableprototype(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('instance')
        self.move_up_reference('range')

class whileloop(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('while', 'whileblock',):
            self.move_up_reference(x, True)

constructor_table = {
    'admsmain' : globals()['admsmain'],
    'analog' : globals()['analog'],
    'assignment' : globals()['assignment'],
    'block' : globals()['block'],
    'branch' : globals()['branch'],
    'branchalias' : globals()['branchalias'],
    'conditional' : globals()['conditional'],
    'contribution' : globals()['contribution'],
    'discipline' : globals()['discipline'],
    'expression' : globals()['expression'],
    'function' : globals()['function'],
    'lexval' : globals()['lexval'],
    'mapply_binary' : globals()['mapply_binary'],
    'mapply_ternary' : globals()['mapply_ternary'],
    'mapply_unary' : globals()['mapply_unary'],
    'module' : globals()['module'],
    'nature' : globals()['nature'],
    'nilled' : globals()['nilled'],
    'node' : globals()['node'],
    'nodealias' : globals()['nodealias'],
    'number' : globals()['number'],
    'probe' : globals()['probe'],
    'range' : globals()['range'],
    'simulator' : globals()['simulator'],
    'source' : globals()['source'],
    'string' : globals()['string'],
    'variable' : globals()['variable'],
    'variableprototype' : globals()['variableprototype'],
    'whileloop' : globals()['whileloop'],
}


dataarray = None

import json
import sys
if __name__ == "__main__":
    with open(sys.argv[1]) as inputfile:
        data = json.load(inputfile)
    n = max([x['id'] for x in data]) + 1
    print(n)
    admst.all_data = [None] * n
    for x in data:
        admst.all_data[x['id']] = constructor_table[x['datatypename']](**x)

