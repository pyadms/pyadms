# Copyright 2023 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

import json


class admst_reference:

    __slots__ = ('index',)

    def __init__(self, index):
        self.index = index

    def __call__(self):
        return admst.all_data[self.index]


class admst_reference_list:

    __slots__ = ('reference_list',)

    def __init__(self, reference_list):
        self.reference_list = reference_list
        if not all(isinstance(x, int) for x in self.reference_list):
            raise RuntimeError("mismatch type")

    def append(self, x, ignore_duplicate):
        # print(type(x))
        if isinstance(x, int):
            y = x
        elif isinstance(x, admst):
            y = x.id
        else:
            # print(type(x))
            raise RuntimeError("mismatch type")

        if ignore_duplicate:
            # linear scan
            if y not in self.reference_list:
                self.reference_list.append(y)
        else:
            self.reference_list.append(y)

    def extend(self, other, ignore_duplicate):
        if not isinstance(other, admst_reference_list):
            raise RuntimeError("mismatch type")

        for o in other.reference_list:
            self.append(o, ignore_duplicate)

    def get_list(self):
        for x in self.reference_list:
            yield admst.all_data[x]

    def get_item(self, i):
        return admst.all_data[self.reference_list[i]]

    def size(self):
        return len(self.reference_list)

    def get_head(self):
        return self.get_item(0)

    def copy(self):
        return admst_reference_list(self.reference_list[:])


class admst:
    all_data = None
    module_ = None
    simulator_ = None

    __slots__ = ('datatypename', 'id', 'uid', 'attributes', 'parameters', 'references', 'kwargs',)

    def __init__(self, **kwargs):
        for x in ['datatypename', 'id', 'uid', 'attributes', 'parameters', 'references']:
            setattr(self, x, kwargs[x])
            del kwargs[x]
        self.kwargs = kwargs

    @staticmethod
    def get_module():
        return admst.all_data[admst.module_]

    @staticmethod
    def get_simulator():
        return admst.all_data[admst.simulator_]

    def move_up_parameter(self, kw):
        setattr(self, kw, self.parameters.pop(kw))
        # if len(self.parameters) == 0:
        #     self.parameters = None

    def move_up_reference(self, kw, single=False):
        if single:
            slen = len(self.references[kw])
            if slen > 1:
                raise RuntimeError(f"not expecting moving up only 1 reference for {kw}")
            elif slen == 0:
                setattr(self, kw, None)
            else:
                setattr(self, kw, admst_reference(self.references.pop(kw)[0]))
        else:
            setattr(self, kw, admst_reference_list(self.references.pop(kw)))
        # if len(self.references) == 0:
        #     self.references = None

    def visit_implemented(self, visitor, *arg, **kwarg):
        return getattr(visitor, 'visit_' + self.__class__.__name__)(self, *arg, **kwarg)

    def visit(self, visitor, *arg, **kwarg):
        return self.visit_implemented(visitor, *arg, **kwarg)


class admsmain(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class analog(admst):

    __slots__ = ('code',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('code', True)


class assignment(admst):

    __slots__ = ('module', 'lhs', 'rhs', 'lexval', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'lhs', 'rhs', 'lexval'):
            self.move_up_reference(x, True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class block(admst):

    __slots__ = ('module', 'lexval', 'block', 'item', 'name', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # this is the parent block of this block
        for x in ('module', 'lexval', 'block'):
            self.move_up_reference(x, True)
        self.move_up_reference('item')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class blockvariable(admst):

    __slots__ = ('block', 'variableprototype', 'probes', 'nodes')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('block', True)
        self.move_up_reference('variableprototype', False)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class branch(admst):

    __slots__ = ('module', 'nodes', 'discipline', 'grounded')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'discipline'):
            self.move_up_reference(x, True)
        self.nodes = admst_reference_list([self.references.pop(x)[0] for x in ['pnode', 'nnode']])


class branchalias(admst):

    __slots__ = ('module', 'branch', 'name',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        for x in ('module', 'branch'):
            self.move_up_reference(x, True)


class conditional(admst):

    __slots__ = ('module', 'If', 'Then', 'Else', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.references['If'] = self.references.pop('if')
        self.references['Then'] = self.references.pop('then')
        self.references['Else'] = self.references.pop('else')
        for x in ('module', 'If', 'Then', 'Else'):
            self.move_up_reference(x, True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class contribution(admst):

    __slots__ = ('module', 'lhs', 'rhs', 'branchalias', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'lhs', 'rhs', 'branchalias'):
            self.move_up_reference(x, True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class discipline(admst):

    __slots__ = ('name', 'domain', 'flow', 'potential',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['name', 'domain']:
            self.move_up_parameter(x)
        for x in ('flow', 'potential'):
            self.move_up_reference(x, True)


class expression(admst):

    __slots__ = ('tree', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('tree',):
            self.move_up_reference(x, True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class function(admst):

    __slots__ = ('unique_id', 'lexval', 'definition', 'arguments', 'name', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('unique_id')
        for x in ('lexval', 'definition'):
            self.move_up_reference(x, True)
        self.move_up_reference('arguments')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class lexval(admst):

    __slots__ = ('string', 'f', 'l', 'c', 'fl')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('string')
        self.move_up_parameter('f')
        self.move_up_parameter('l')
        self.move_up_parameter('c')
        self.fl = f'{self.f}:{self.l}'


class mapply_binary(admst):

    __slots__ = ('args', 'name', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = admst_reference_list([self.references.pop(x)[0] for x in ['arg1', 'arg2']])
        self.move_up_parameter('name')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class mapply_ternary(admst):

    __slots__ = ('args', 'name', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = admst_reference_list([self.references.pop(x)[0] for x in ['arg1', 'arg2', 'arg3']])
        self.move_up_parameter('name')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class mapply_unary(admst):

    __slots__ = ('args', 'name', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args = admst_reference_list([self.references.pop(x)[0] for x in ['arg1']])
        self.move_up_parameter('name')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class attribute(admst):

    __slots__ = ('name', 'value',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        self.move_up_parameter('value')


class module(admst):

    __slots__ = (
        'analog',
        'analogfunction',
        'assignment',
        'attribute',
        'block',
        'blockvariable',
        'branch',
        'branchalias',
        'callfunction',
        'case',
        'conditional',
        'contribution',
        'expression',
        'external_nodes',
        'forloop',
        'instance',
        'instance_parameters',
        'internal_nodes',
        'model_parameters',
        'name',
        'node',
        'nodealias',
        'probe',
        'range',
        'source',
        'variableprototype',
        'whileloop',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        for x in (
            'analogfunction',
            'assignment',
            'attribute',
            'block',
            'blockvariable',
            'branch',
            'branchalias',
            'callfunction',
            'case',
            'conditional',
            'contribution',
            'expression',
            'forloop',
            'instance',
            'node',
            'nodealias',
            'probe',
            'range',
            'source',
            'variableprototype',
            'whileloop',
        ):
            self.move_up_reference(x)
        self.move_up_reference('analog', True)

class analogfunction(admst):

    __slots__ = ('name', 'lexval', 'tree')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('tree', True)
        self.move_up_reference('lexval', True)

class callfunction(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise RuntimeError('callfunction needs to be implemented')


class nature(admst):

    __slots__ = ('access', 'name', 'ddt_name', 'idt_name', 'units', 'abstol', 'base', 'ddt_nature', 'idt_nature',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['access', 'name', 'ddt_name', 'idt_name', 'units']:
            self.move_up_parameter(x)
        for x in ('abstol', 'base', 'ddt_nature', 'idt_nature'):
            self.move_up_reference(x, True)


class nilled(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class node(admst):

    __slots__ = ('name', 'direction', 'location', 'module', 'discipline', 'grounded')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['name', 'direction', 'location']:
            self.move_up_parameter(x)
        for x in ('module', 'discipline'):
            self.move_up_reference(x, True)


class nodealias(admst):

    __slots__ = ('name', 'module', 'node')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('name')
        for x in ('module', 'node'):
            self.move_up_reference(x, True)


class number(admst):

    __slots__ = ('value', 'scalingunit', 'cast', 'lexval', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ['scalingunit', 'cast']:
            self.move_up_parameter(x)
        self.move_up_reference('lexval', True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])

class probe(admst):

    __slots__ = ('module', 'branch', 'nature', 'discipline', 'grounded', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'branch', 'nature'):
            self.move_up_reference(x, True)
        self.probes = admst_reference_list([self.id,])
        self.nodes = admst_reference_list([])


class Range(admst):

    __slots__ = ('module', 'infexpr', 'supexpr', 'name', 'infboundtype', 'supboundtype', 'type',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'infexpr', 'supexpr'):
            self.move_up_reference(x, True)
        for x in ('name', 'infboundtype', 'supboundtype', 'type'):
            self.move_up_parameter(x)


class simulator(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class source(admst):

    __slots__ = ('module', 'branch', 'nature', 'probe', 'discipline', 'grounded')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for x in ('module', 'branch', 'nature'):
            self.move_up_reference(x, True)


class string(admst):

    __slots__ = ('value', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_parameter('value')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class variable(admst):

    __slots__ = ('variableprototype', 'variable', 'name', 'dependency', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('variableprototype', True)
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])


class variableprototype(admst):

    __slots__ = ('instance', 'range', 'default', 'parametertype', 'setin', 'name', 'lexval', 'dependency', 'input', 'output', 'type', 'probes', 'nodes', 'has_ddt', 'has_resistive', 'has_noise', 'has_ddx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.move_up_reference('instance')
        self.move_up_reference('range', False)
        self.move_up_reference('default', True)
        self.move_up_reference('lexval', True)
        self.setin = admst_reference_list([])
        self.move_up_parameter('parametertype')
        self.move_up_parameter('input')
        self.probes = admst_reference_list([])
        self.nodes = admst_reference_list([])

    def setinblock(self, b):
        self.setin.append(b, True)


class whileloop(admst):

    __slots__ = ('While', 'whileblock',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.references['While'] = self.references.pop('while')
        for x in ('While', 'whileblock',):
            self.move_up_reference(x, True)


class forloop(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class array(admst):

    __slots__ = tuple()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


constructor_table = {
    'admsmain': globals()['admsmain'],
    'analog': globals()['analog'],
    'analogfunction': globals()['analogfunction'],
    'assignment': globals()['assignment'],
    'attribute': globals()['attribute'],
    'block': globals()['block'],
    'blockvariable': globals()['blockvariable'],
    'branch': globals()['branch'],
    'branchalias': globals()['branchalias'],
    'conditional': globals()['conditional'],
    'contribution': globals()['contribution'],
    'discipline': globals()['discipline'],
    'expression': globals()['expression'],
    'function': globals()['function'],
    'lexval': globals()['lexval'],
    'mapply_binary': globals()['mapply_binary'],
    'mapply_ternary': globals()['mapply_ternary'],
    'mapply_unary': globals()['mapply_unary'],
    'module': globals()['module'],
    'nature': globals()['nature'],
    'nilled': globals()['nilled'],
    'node': globals()['node'],
    'nodealias': globals()['nodealias'],
    'number': globals()['number'],
    'probe': globals()['probe'],
    'range': globals()['Range'],
    'simulator': globals()['simulator'],
    'source': globals()['source'],
    'string': globals()['string'],
    'variable': globals()['variable'],
    'variableprototype': globals()['variableprototype'],
    'whileloop': globals()['whileloop'],
}


def load_json(fname):

    with open(fname) as inputfile:
        data = json.load(inputfile)
    n = max([x['id'] for x in data]) + 1
    print(n)
    admst.all_data = [None] * n
    for x in data:
        dtname = x['datatypename']
        admst.all_data[x['id']] = constructor_table[dtname](**x)
        if dtname == 'module':
            if admst.module_ is None:
                admst.module_ = x['id']
            else:
                raise RuntimeError("Expecting only 1 module")
        elif dtname == 'simulator':
            if admst.simulator_ is None:
                admst.simulator_ = x['id']
            else:
                raise RuntimeError("Expecting only 1 module")

    return admst
