

class admst_reference:
    def __init__(self, index):
        self.index = index

    def __call__(self):
        return admst.all_data[self.index]

class admst_reference_list:
    def __init__(self, reference_list):
        self.reference_list = reference_list
        if not all(isinstance(x, int) for x in self.reference_list):
            raise RuntimeError("mismatch type")

    def append(self, x, ignore_duplicate = False):
        self.reference_list.append(x)
        if not isinstance(x, int):
            raise RuntimeError("mismatch type")

    def get_list(self):
        for x in self.reference_list:
            yield admst.all_data[x]

class admst:
    all_data = None
    module_ = None

    def __init__(self, **kwargs):
        for x in ['datatypename', 'id', 'uid', 'attributes', 'parameters', 'references']:
            self.__dict__[x] = kwargs[x]
            del kwargs[x]
        self.kwargs = kwargs

    def get_module():
        return admst.all_data[admst.module_]

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
                self.__dict__[kw] = admst_reference(self.references.pop(kw)[0])
        else:
            self.__dict__[kw] = admst_reference_list(self.references.pop(kw))
        if len(self.references) == 0:
            self.references = None

    def visit_implemented(self, visitor):
        getattr(visitor, 'visit_' + self.__class__.__name__)(self)

    def visit(self, visitor):
        self.visit_implemented(visitor)

    def get_datatypename(self):
        return self.__class__.__name__


class admsmain(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class analog(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('code', True)

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

        self.references['If'] = self.references.pop('if')
        self.references['Then'] = self.references.pop('then')
        self.references['Else'] = self.references.pop('else')
        for x in ('module', 'If', 'Then', 'Else'):
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
        self.args = admst_reference_list([self.references[x][0] for x in ['arg1', 'arg2']])
        self.move_up_parameter('name')

class mapply_ternary(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = admst_reference_list([self.references[x][0] for x in ['arg1', 'arg2', 'arg3']])
        self.move_up_parameter('name')

class mapply_unary(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = admst_reference_list([self.references[x][0] for x in ['arg1']])
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
        self.probe = admst_reference_list([])

class string(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('value')

class variable(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('prototype', True)
        self.probe = admst_reference_list([])

class variableprototype(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('instance')
        self.move_up_reference('range', True)
        self.move_up_reference('default', True)
        self.dependency = None
        self.input = None
        self.setinmodel = False
        self.usedinmodel = False
        self.setininstance = False
        self.usedininstance = False
        self.setininitial_step = False
        self.usedininitial_step = False
        self.setinevaluate = False
        self.usedinevaluate = False
        self.setinnoise = False
        self.usedinnoise = False
        self.setinfinal = False
        self.usedinfinal = False

class whileloop(admst):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.references['While'] = self.references.pop('while')
        for x in ('While', 'whileblock',):
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
import adms_implicit
if __name__ == "__main__":
    with open(sys.argv[1]) as inputfile:
        data = json.load(inputfile)
    n = max([x['id'] for x in data]) + 1
    print(n)
    admst.all_data = [None] * n
    for x in data:
        dtname = x['datatypename']
        admst.all_data[x['id']] = constructor_table[dtname](**x)
        if dtname == 'module':
            if admst.module_ == None:
                admst.module_ = x['id']
            else:
                raise RuntimeError("Expecting only 1 module")

    dv = adms_implicit.dependency_visitor()
    admst.get_module().visit(dv)




