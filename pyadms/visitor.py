# Copyright 2023 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0
import adms_loader


class dependency_visitor:
    __slots__ = ('globalpartition', 'globalassignment', 'globalexpression',)

    def __init__(self):
        self.globalpartition = None

    def visit_module(self, module: adms_loader.module):
        for node in module.node.get_list():
            if node.location == 'ground':
                node.grounded = True
            else:
                node.grounded = False

        for branch in module.branch.get_list():
            nlist = list(branch.node.get_list())
            if nlist[1].discipline is None:
                branch.discipline = nlist[0].discipline
            elif nlist[0].discipline is None:
                branch.discipline = nlist[1].discipline
            elif nlist[0].discipline().name == nlist[1].discipline().name:
                branch.discipline = nlist[0].discipline
            else:
                raise RuntimeError('discipliine mismatch')
            # print(branch.uid)
            # print(nlist[0].discipline)
            # print(nlist[1].discipline)
            branch.grounded = any([n.grounded for n in nlist])

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
                    v.output = True
                elif v.attributes['ask'] == 'no':
                    v.output = False
                else:
                    raise RuntimeError('not valid type')

            if v.default is not None:
                default = v.default()
                default.visit(self)

    def visit_expression(self, expression: adms_loader.expression):
        self.globalexpression = expression
        tree = expression.tree()
        tree.visit(self)
        self.globalexpression = None
        expression.dependency = tree.dependency

    def visit_probe(self, probe: adms_loader.probe):
        probe.dependency = 'linear'

    def visit_array(self, array: adms_loader.array):
        pass

    def visit_variable(self, variable: adms_loader.variable):
        if variable.variableprototype().name is None:
            variable.variableprototype().name = variable.variableprototype().lexval().string
        if self.globalpartition:
            # print(f'variable "{variable.variableprototype().name}" is set in "{self.globalpartition.name}"')
            variable.variableprototype().setinblock(self.globalpartition)

    def visit_mapply_unary(self, unary: adms_loader.mapply_unary):
        args = list(unary.args.get_list())
        args[0].visit(self)

    def visit_mapply_binary(self, binary: adms_loader.mapply_binary):
        args = list(binary.args.get_list())
        for arg in args:
            arg.visit(self)

    def visit_mapply_ternary(self, ternary: adms_loader.mapply_ternary):
        args = list(ternary.args.get_list())
        for arg in args:
            arg.visit(self)

    def visit_function(self, function: adms_loader.function):
        function.name = function.lexval().string
        args = list(function.arguments.get_list())
        for arg in args:
            arg.visit(self)

    scalingunits = {
      '1': '',
      'E': 'e+18',
      'P': 'e+15',
      'T': 'e+12',
      'G': 'e+9',
      'M': 'e+6',
      'k': 'e+3',
      'h': 'e+2',
      'D': 'e+1',
      'd': 'e-1',
      'c': 'e-2',
      'm': 'e-3',
      'u': 'e-6',
      'n': 'e-9',
      'A': 'e-10',
      'p': 'e-12',
      'f': 'e-15',
      'a': 'e-18',
    }

    def visit_number(self, number: adms_loader.number):
        number.dependency = 'constant'
        scalingunit = self.scalingunits[number.scalingunit]
        number.value = number.lexval().string + scalingunit

    def visit_string(self, string: adms_loader.string):
        string.dependency = 'constant'

    def visit_callfunction(self, callfunction: adms_loader.callfunction):
        pass

    def visit_whileloop(self, whileloop: adms_loader.whileloop):
        While = whileloop.While()
        While.visit(self)
        whileloop.While.visit(self)
        whileloop.whileblock().visit(self)

    def visit_forloop(self, forloop: adms_loader.forloop):
        pass

    def visit_conditional(self, conditional: adms_loader.conditional):
        conditional.If().visit(self)
        conditional.Then().visit(self)
        if conditional.Else is not None:
            conditional.Else().visit(self)

    def visit_contribution(self, contribution: adms_loader.contribution):
        # self.globalcontribution = contribution
        contribution.rhs().visit(self)
        # self.globalcontribution = None
        # contribution.lhs().probe
        # for probe in contribution.rhs().probe:
        #     contribution.lhs().probe.append(probe)
        # contribution.dependency = 'nonlinear'

    def visit_assignment(self, assignment: adms_loader.assignment):
        ldn = assignment.lhs().datatypename
        if ldn == 'array':
            lhs = assignment.lhs().variable()
        else:
            lhs = assignment.lhs()

        rhs = assignment.rhs()
        self.globalassignment = assignment
        rhs.visit(self)
        self.globalassignment = None

        if not hasattr(lhs, 'variable'):
            lhs.variable = []

    def visit_block(self, block: adms_loader.block):
        block.name = block.lexval().string

        if block.name in ('initial_model', 'initial_instance', 'initial_step', 'noise', 'final_step'):
            self.globalpartition = block
        elif block.name == '':
            self.globalpartition = None
        else:
            print(f'unexpected block name: {block.name}')
            # raise RuntimeError(f'unexpected block name: {block.name}')

        for item in block.item.get_list():
            item.visit(self)

        self.globalpartition = None

    def visit_nilled(self, nilled: adms_loader.nilled):
        pass

    def visit_blockvariable(self, blockvariable: adms_loader.blockvariable):
        # this is a list for multiple declarations in the same statement
        for vp in blockvariable.variableprototype.get_list():
            if vp.name is None:
                vp.name = vp.lexval().string
        
