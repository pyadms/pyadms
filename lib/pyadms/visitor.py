# Copyright 2023 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0
from . import adms_loader


class dependency_visitor:
    __slots__ = ('globalpartition', 'globalassignment', 'globalexpression',)

    def __init__(self):
        self.globalpartition = None

    def visit_module(self, module: adms_loader.module):
        module.internal_nodes = adms_loader.admst_reference_list([])
        module.external_nodes = adms_loader.admst_reference_list([])
        for node in module.node.get_list():
            if node.location == 'ground':
                node.grounded = True
            elif node.location == 'external':
                node.grounded = False
                module.external_nodes.append(node)
            elif node.location == 'internal':
                node.grounded = False
                module.internal_nodes.append(node)
            else:
                raise RuntimeError(f"Unknown node location {node.location}")

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

        module.model_parameters = adms_loader.admst_reference_list([])
        module.instance_parameters = adms_loader.admst_reference_list([])
        for v in module.variableprototype.get_list():
            v.visit(self)
            if v.type == 'model' and v.input == True:
                module.model_parameters.append(v)
            elif v.type == 'instance':
                module.instance_parameters.append(v)


    def visit_expression(self, expression: adms_loader.expression):
        self.globalexpression = expression
        tree = expression.tree()
        tree.visit(self)
        self.globalexpression = None
        expression.dependency = tree.dependency
        expression.probes = tree.probes.copy()

    def visit_probe(self, probe: adms_loader.probe):
        probe.dependency = 'linear'

    def visit_array(self, array: adms_loader.array):
        pass

    def visit_variable(self, variable: adms_loader.variable):
        # TODO: it may be necessary to do this on an additional pass if we want to know about all assignments to this variable, even if it happens later.
        vp = variable.variableprototype()
        vp.visit(self)
        variable.name = vp.name
        variable.dependency = vp.dependency
        variable.probes.extend(vp.probes, True)

        if self.globalpartition:
            # print(f'variable "{vp.name}" is set in "{self.globalpartition.name}"')
            vp.setinblock(self.globalpartition)

    def visit_variableprototype(self, prototype: adms_loader.variableprototype):
        # TODO: somehow collect probes from assignments
        if not hasattr(prototype, 'name'):
            prototype.name = prototype.lexval().string
        if not hasattr(prototype, 'dependency'):
            prototype.dependency = 'constant'
        if not hasattr(prototype, 'type'):
            if prototype.parametertype == 'analogfunction':
                prototype.type = prototype.parametertype
            elif 'type' not in prototype.attributes:
                prototype.type = 'model'
            else:
                prototype.type = prototype.attributes['type']
                if prototype.type not in ('instance', 'model'):
                    raise RuntimeError(f'{prototype.name} has an invalid type {prototype.parametertype}')
        if not hasattr(prototype, 'output'):
            prototype.output = False
            if 'ask' in prototype.attributes:
                ask = prototype.attributes['ask']
                if ask == 'yes':
                    prototype.output = True
                elif ask == 'no':
                    prototype.output = False
                else:
                    raise RuntimeError(f'not valid ask {ask}')
        if hasattr(prototype, 'default') and prototype.default is not None:
            prototype.default().visit(self)

    def visit_mapply_unary(self, unary: adms_loader.mapply_unary):
        args = list(unary.args.get_list())
        args[0].visit(self)
        unary.probes.extend(unary.args, True)
        name = unary.name
        if name in ('minus', 'plus', 'not'):
            unary.dependency = args[0].dependency
        else:
            raise RuntimeError(f"unexpected mapply_unary function {name}")

    def visit_mapply_binary(self, binary: adms_loader.mapply_binary):
        args = list(binary.args.get_list())
        for arg in args:
            arg.visit(self)
            binary.probes.extend(arg.probes, True)
        deps = [b.dependency for b in binary.args.get_list()]
        name = binary.name
        if all([d=='constant' for d in deps]):
            binary.dependency = 'constant'
        elif any([d=='nonlinear' for d in deps]):
            binary.dependency = 'nonlinear'
        elif name in ('addp', 'addm'):
            if any([d=='linear' for d in deps]):
                binary.dependency = 'linear'
            else:
                raise RuntimeError(f"unexpected mapply_binary dependency for {name}")
        elif name == 'multtime':
            if deps[0] == 'constant':
                binary.dependency = deps[1]
            elif deps[1] == 'constant':
                binary.dependency = deps[0]
            else:
                binary.dependency = 'nonlinear'
        elif name == 'multdiv':
            if deps[1] == 'constant':
                binary.dependency = deps[0]
            else:
                binary.dependency = 'nonlinear'
        elif name in ('gt', 'gt_equ', 'lt', 'lt_equ',):
            binary.dependency = 'constant'
        else:
            raise RuntimeError(f"unexpected mapply_binary function {name}")


    def visit_mapply_ternary(self, ternary: adms_loader.mapply_ternary):
        args = list(ternary.args.get_list())
        for arg in args:
            arg.visit(self)
            ternary.probes.extend(arg.probes)
        deps = [b.dependency for b in ternary.args.get_list()]
        name = ternary.name

        if name == 'conditional':
            if any([d=='nonlinear' for d in deps]):
                ternary.dependency = 'nonlinear'
            elif any([d=='linear' for d in deps]):
                ternary.dependency = 'linear'
            else:
                ternary.dependency = 'constant'
        else:
            raise RuntimeError(f"unexpected mapply_ternary function {name}")

    def visit_function(self, function: adms_loader.function):
        function.name = function.lexval().string
        args = list(function.arguments.get_list())
        for arg in args:
            arg.visit(self)
            function.probes.extend(arg.probes)
        deps = [f.dependency for f in args]
        # print(function.name)
        if (all(d == 'constant' for d in deps)):
            function.dependency = 'constant'
        else:
            function.dependency = 'nonlinear'

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
        raise RuntimeError('callfunction not implemented')
        pass

    def visit_whileloop(self, whileloop: adms_loader.whileloop):
        While = whileloop.While()
        While.visit(self)
        whileloop.While().visit(self)
        whileloop.whileblock().visit(self)

    def visit_forloop(self, forloop: adms_loader.forloop):
        raise RuntimeError('forloop not implemented')
        pass

    def visit_conditional(self, conditional: adms_loader.conditional):
        conditional.If().visit(self)
        conditional.Then().visit(self)
        if conditional.Else is not None:
            conditional.Else().visit(self)
        conditional.probes.extend(conditional.If().probes, True)
        conditional.probes.extend(conditional.Then().probes, True)
        if conditional.Else is not None:
            conditional.probes.extend(conditional.Else().probes, True)

    def visit_contribution(self, contribution: adms_loader.contribution):
        # self.globalcontribution = contribution
        contribution.rhs().visit(self)
        contribution.probes.extend(contribution.rhs().probes)
        # self.globalcontribution = None
        # contribution.lhs().probe
        # for probe in contribution.rhs().probe:
        #     contribution.lhs().probe.append(probe)
        # contribution.dependency = 'nonlinear'

    def visit_assignment(self, assignment: adms_loader.assignment):
        ldn = assignment.lhs().datatypename
        if ldn == 'array':
            lhs = assignment.lhs().variable()
            raise RuntimeError("ARRAY not implemented yet")
        else:
            lhs = assignment.lhs()

        rhs = assignment.rhs()
        self.globalassignment = assignment
        rhs.visit(self)
        self.globalassignment = None

        vp = lhs.variableprototype()
        if not hasattr(vp, 'dependency'):
            vp.dependency = rhs.dependency
        elif (vp.dependency == rhs.dependency) or (vp.dependency == 'nonlinear'):
            pass
        elif (vp.dependency == 'linear') and (rhs.dependency in ('linear', 'nonlinear')):
            vp.dependency = rhs.dependency
        else:
            vp.dependency = 'constant'

        # this specific variableprototype is using these probes
        vp.probes.extend(rhs.probes, True)
        # this specific variable is using these probes
        lhs.probes.extend(rhs.probes, True)
        # this assignment statement has these probes
        assignment.probes.extend(rhs.probes, True)
        lhs.visit(self)

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
            block.probes.extend(item.probes)

        self.globalpartition = None

    def visit_nilled(self, nilled: adms_loader.nilled):
        pass

    def visit_blockvariable(self, blockvariable: adms_loader.blockvariable):
        for vp in blockvariable.variableprototype.get_list():
            vp.visit(self)
            blockvariable.probes.extend(vp.probes)

