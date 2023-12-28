# Copyright 2023 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

class dependency_visitor:
    __slots__ = ('partition',)

    def __init__(self):
        self.partition = None

    def visit_module(self, module):
        for node in module.node.get_list():
            if node.location == 'ground':
                node.grounded = True
            else:
                node.grounded = False

        for branch in module.branch.get_list():
            branch.discipline = branch.pnode().discipline
            branch.grounded = branch.nnode().grounded

        for source in module.source.get_list():
            source.discipline = source.branch().discipline
            source.grounded = source.branch().grounded

        for probe in module.probe.get_list():
            probe.discipline = probe.branch().discipline
            probe.grounded = probe.branch().grounded

        for analogfunction in module.analogfunction.get_list():
            analogfunction.tree().visit(self)

        for analog in module.analog.get_list():
            analog.code().visit(self)

        for v in module.variableprototype.get_list():
            if 'type' in v.attributes:
                if v.attributes['type'] == 'instance':
                    v.parametertype = 'instance'
            elif 'ask' in v.attributes:
                if v.attributes['ask'] == 'yes':
                    v.output == True
                elif v.attributes['ask'] == 'no':
                    v.output == False
                else:
                    raise RuntimeError('not valid type')

            if v.default is not None:
                default = v.default()
                default.visit(self)

    def visit_expression(self, expression):
        expression.tree().visit(self)

    def visit_probe(self, probe):
        pass

    def visit_array(self, array):
        pass

    def visit_variable(self, variable):
        if self.partition:
            variable.variableprototype().setinblock(self.partition)

    def visit_mapply_unary(self, unary):
        args = list(unary.args.get_list())
        args[0].visit(self)

    def visit_mapply_binary(self, binary):
        args = list(binary.args.get_list())
        for arg in args:
            arg.visit(self)

    def visit_mapply_ternary(self, ternary):
        args = list(ternary.args.get_list())
        for arg in args:
            arg.visit(self)

    def visit_function(self, function):
        function.name = function.lexval().string
        args = list(function.arguments.get_list())
        for arg in args:
            arg.visit(self)

    scalingunits = {
      '1' : '',
      'E' : 'e+18',
      'P' : 'e+15',
      'T' : 'e+12',
      'G' : 'e+9',
      'M' : 'e+6',
      'k' : 'e+3',
      'h' : 'e+2',
      'D' : 'e+1',
      'd' : 'e-1',
      'c' : 'e-2',
      'm' : 'e-3',
      'u' : 'e-6',
      'n' : 'e-9',
      'A' : 'e-10',
      'p' : 'e-12',
      'f' : 'e-15',
      'a' : 'e-18',
    }

    def visit_number(self, number):
        number.dependency = 'constant'
        scalingunit = self.scalingunits[number.scalingunit]
        number.value = number.lexval().string + scalingunit

    def visit_string(self, string):
        string.dependency = 'constant'

    def visit_callfunction(self, callfunction):
        # visit function arguments
        pass

    def visit_whileloop(self, whileloop):
        While = whileloop.While()
        While.visit(self)
        whileloop.While.visit(self)
        whileblock().visit(self)

    def visit_forloop(self, forloop):
        pass

    def visit_conditional(self, conditional):
        conditional.If().visit(self)
        conditional.Then().visit(self)
        if conditional.Else is not None:
            conditional.Else().visit(self)

    def visit_contribution(self, contribution):
        #self.globalcontribution = contribution
        contribution.rhs().visit(self)
        #self.globalcontribution = None
        #contribution.lhs().probe
        #for probe in contribution.rhs().probe:
        #    contribution.lhs().probe.append(probe)
        #contribution.dependency = 'nonlinear'

    def visit_assignment(self, assignment):
        ldn = assignment.datatypename
        if ldn == 'array':
            lhs = assignment.lhs().variable()
        else:
            lhs = assignment.lhs()

        rhs = assignment.rhs()
        rhs.visit(self)

        if not hasattr(lhs, 'variable'):
            lhs.variable = []

    def visit_block(self, block):
        block.name = block.lexval().string

        #if self.partition is not None:
        #    print(str(self.partition.lexval().fl))
        #    print(str(block.lexval().fl))
        #    raise RuntimeError(f'new block evaluated while processing another')

        if block.name in  ('initial_model', 'initial_instance', 'initial_step', 'noise', 'final_step', ''):
            self.partition = block
        else:
            raise RuntimeError(f'unexpected block name: {block.name}')

        for item in block.item.get_list():
            item.visit(self)

        self.partition = None

    def visit_nilled(self, nilled):
        pass

    def visit_blockvariable(self, blockvariable):
        pass

