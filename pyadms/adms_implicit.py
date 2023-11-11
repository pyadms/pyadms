
class dependency_visitor:
    def __init__(self):
        self.globalmodule = None
        self.globalassignment = None
        self.globalcontribution = None
        self.globalexpression = None
        self.globalopdependent = False
        self.globalpartitionning = None
        self.globaltreenode = None

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

    # implements logic of adms.implicit.xml.module
    def visit_module(self, module):
        self.globalmodule = module

        for node in module.node.get_list():
            if node.location == 'ground':
                node.grounded = True
            else:
                node.grounded = False

        for branch in module.branch.get_list():
            # need to check both nnode and pnode for this and next
            branch.discipline = branch.pnode().discipline
            branch.grounded = branch.nnode().grounded

        for source in module.source.get_list():
            source.discipline = source.branch().discipline
            source.grounded = source.branch().grounded

        for probe in module.probe.get_list():
            probe.discipline = probe.branch().discipline
            probe.grounded = probe.branch().grounded
#  <admst:for-each select="instance">
#    <admst:push into="module/instantiator" select=".." onduplicate="ignore"/>
#    <admst:assert select="terminal" test="nodefrommodule[location='external']"
#                  format="%(../instantiator).%(nodefrommodule/name): is not terminal\n"/>
#    <admst:assert select="parameterset" test="parameter[input='yes']"
#                  format="%(../instantiator).%(parameter/name): is not input parameter\n"/>
#  </admst:for-each>

        for analogfunction in module.analogfunction.get_list():
            analogfunction.tree().visit(self)

        for analog in module.analog.get_list():
            analog.code().visit(self)

        # this looks like module variable is actually variable prototype
        for v in module.variable.get_list():
            if v.dependency != 'constant':
                v.OPdependent = True
            v.output = v.input

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

            v.scope = None
            if (v.input and v.parametertype=='model') or ((not v.input) and (v.setinmodel or v.usedinmodel)
                and (v.setininstance or v.setininitial_step or v.setinevaluate or v.setinnoise or v.setinfinal
                or v.usedininstance or v.usedininitial_step or v.usedinevaluate or v.usedinnoise or v.usedinfinal or v.output)):
                v.scope = "global_model"
            elif ((not v.input) and (not v.setinmodel) and (not v.usedinmodel) and
                (((v.setininstance or v.usedininstance) and (v.setininitial_step or v.setinevaluate or v.setinnoise or v.setinfinal
                or v.usedininitial_step or v.usedinevaluate or v.usedinnoise or v.usedinfinal or v.output))
                or ((v.setininitial_step or v.usedininitial_step) and (v.setinevaluate or v.setinnoise or v.setinfinal
                or v.usedinevaluate or v.usedinnoise or v.usedinfinal or v.output))
                or ((v.setinevaluate or v.usedinevaluate) and (v.setinnoise or v.setinfinal
                  or v.usedinnoise or v.usedinfinal or v.output))
                or ((v.setinnoise or v.usedinnoise) and (v.setinfinal or v.usedinfinal or v.output))
                or ((v.setinfinal or v.usedinfinal) and v.output)
                or ((not v.setinmodel) and (not v.setininstance) and (not v.setinevaluate) and (not v.setinnoise) and (not v.setinfinal) and
                    (not v.usedinmodel) and (not v.usedininstance) and (not v.usedinevaluate) and (not v.usedinnoise) and (not v.usedinfinal) and v.output)
              )):
                v.scope = 'global_instance'

            if (not v.input) and v.scope=='global_instance' and v.setininitial_step and (v.setinevaluate or v.usedinevaluate):
                v.isstate = True
            else:
                v.isstate = False

    def visit_expression(self, expression):
        self.globalexpression = expression
        expression.variable = []
        expression.probe = []
        expression.TemperatureDependent = False
        tree = expression.tree()
        tree.visit(self)
        self.globalexpression = None

        expression.dependency = tree.dependency
        # this may be for each variable (see admst)
        if expression.dependency == 'constant' and self.globalopdependent:
            expression.dependency = 'constant'
        if self.globalpartitionning is None:
            self.usedinevaluate = True
        elif self.globalpartitionning == 'initial_model':
            self.usedinmodel = True
        elif self.globalpartitionning == 'initial_instance':
            self.usedininstance = True
        elif self.globalpartitionning == 'initial_step':
            self.usedininitial_step = True
        elif self.globalpartitionning == 'noise':
            self.usedinnoise = True
        elif self.globalpartitionning == 'final_step':
            self.usedinfinal = True

    def visit_probe(self, probe):
        probe.dependency = 'linear'
        if probe.id not in self.globalexpression.probe:
            self.globalexpression.probe.append(probe.id)

    def visit_array(self, array):
        pass
#    <admst:when test="[datatypename='array']">
#      <admst:apply-templates select="variable" match="e:dependency"/>
#      <admst:value-to select="dependency" path="variable/dependency"/>
#    </admst:when>
    def visit_variable(self, variable):
        for probe in variable.probe.get_list():
            self.globalexpression.probe.append(probe, True)
        self.globalexpression.variable.append(variable)
#      <admst:push into="$globaltreenode/@variable" select="." onduplicate="ignore"/>
        variable.dependency = variable.prototype().dependency

    def visit_mapply_unary(self, unary):
        args = list(unary.args.get_list())
        args[0].visit(self)
        unary.dependency = args[0].dependency
#      <admst:value-to select="[name='minus']/math/value" string="-%(arg1/math/value)"/>

    def visit_mapply_binary(self, binary):
        args = list(binary.args.get_list())
        for arg in args:
            arg.visit(self)
#      <!--
#        +:             -:            *:            /:
#          c  np l  nl    c  np l  nl   c  np l  nl   c  np nl nl
#          np np l  nl    np np l  nl   np np l  nl   np np nl nl
#          l  l  l  nl    l  l  l  nl   l  l  nl nl   l  l  nl nl
#          nl nl nl nl    nl nl nl nl   nl nl nl nl   nl nl nl nl
#      -->
        deps = [x.dependency for x in args]
        if binary.name == 'multdiv' and  deps[1] == 'linear':
            binary.dependency = 'nonlinear'
        elif 'nonlinear' in deps:
            binary.dependency = 'nonlinear'
        elif 'linear' in deps:
            binary.dependency = 'nonlinear'
        elif 'noprobe' in deps:
            binary.dependency = 'noprobe'
        else:
            binary.dependency = 'constant'

    def visit_mapply_ternary(self, ternary):
#      <!--
#          ?: - arg1=c -  - arg1!=c -
#             c  np l  nl np np l  nl
#             np np l  nl np np l  nl
#             l  l  l  nl l  l  l  nl
#             nl nl nl nl nl nl nl nl
#      -->
        args = list(ternary.args.get_list())
        for arg in args:
            arg.visit(self)
        deps = [x.dependency for x in args]
        if 'nonlinear' in deps[1:]:
            ternary.dependency = 'nonlinear'
        elif 'linear' in deps[1:]:
            ternary.dependency = 'linear'
        elif 'constant' != deps[0] or 'noprobe' in args[1:]:
            ternary.dependency = 'noprobe'
        else:
            ternary.dependency = 'constant'

    def visit_function(self, function):
        function.name = function.lexval().string
        name = function.name
        args = list(function.arguments.get_list())
        if name in ('ddx', '$ddx', '$derivate',):
            self.globalassignment.lhs().derivate = True
            args[0].visit(self)
            if args[1] not in self.globalexpression.variable:
                self.globalexpression.variable.append(args[1])
                # handle ddxprobe
            if args[0].dependency in ('constant', 'noprobe',):
                function.dependency = args[0].dependency
            else:
                function.dependency = 'nonlinear'
        else:
            for arg in args:
                arg.visit(self)
            if name in ('ddt', '$ddt', 'idt', '$idt'):
                function.dependency = 'nonlinear'

            deps = set([x.dependency for x in args])
            if 'nonlinear' in deps:
                function.dependency = 'nonlinear'
            elif 'linear' in deps:
                function.dependency = 'nonlinear'
            elif 'noprobe' in deps:
                function.dependency = 'noprobe'
            else:
                function.dependency = 'constant'

            if function.dependency in ('linear', 'nonlinear'):
                self.globalexpression.hasVoltageDependentFunction = True
            else:
                self.globalexpression.hasVoltageDependentFunction = False
#      <admst:value-to select="subexpression/expression" path="$globalexpression"/>
#      <!-- fixme: these flags should be set after all contribs are transformed to ...<+F(...); canonical form -->
#      <admst:value-to test="[name='ddt']" select="$globalcontribution/#fixmedynamic" path="1"/>
#      <admst:value-to test="[name='white_noise']" select="$globalcontribution/#fixmewhitenoise" path="1"/>
#      <admst:value-to test="[name='flicker_noise']" select="$globalcontribution/#fixmeflickernoise" path="1"/>
#      <admst:value-to test="[name='\$temperature']" select="$globalassignment/lhs/TemperatureDependent" string="yes"/>
#      <admst:choose>
#        <admst:when test="[name='\$realtime' or name='\$temperature' or name='\$vt' or name='idt' or name='ddt' or
#                           name='\$param_given' or name='\$given' or name='ddx' or name='flicker_noise' or name='white_noise']"/>
#        <admst:when
#          test="[name='analysis' or name='\$analysis' or name='\$simparam' or name='simparam' or
#          name='\$shrinka' or name='\$shrinkl' or name='\$limexp' or
#          name='abs' or name='acos' or name='asin' or name='atan' or name='cos' or name='cosh' or name='exp' or
#          name='hypot' or name='limexp' or name='ln' or name='log' or name='max' or name='min' or name='pow' or
#          name='sin' or name='sinh' or name='sqrt' or name='tan' or name='tanh' or name='atanh' or name='floor' or name='ceil']">
#          <admst:push into="$globalexpression/function" select="."/>
#          <admst:value-to select="class" string="builtin"/>
#        </admst:when>
#        <admst:otherwise>
#          <admst:assert test="[exists(definition)]" format="%(lexval/(f|':'|l|':'|c)): analog function '%(name)' is undefined\n"/>
#        </admst:otherwise>
#      </admst:choose>
#    </admst:when>
    def visit_number(self, number):
        number.dependency = 'constant'
        scalingunit = self.scalingunits[number.scalingunit]
        number.value = number.lexval().string + scalingunit

    def visit_string(self, string):
        string.dependency = 'constant'

#  <admst:choose>
    def visit_callfunction(self, callfunction):
        pass
#    <admst:when test="[datatypename='callfunction']">
#      <admst:apply-templates select="function/arguments" match="e:dependency"/>
#      <admst:value-to select="dependency" path="function/dependency"/>
#    </admst:when>
    def visit_whileloop(self, whileloop):
#    <admst:when test="[datatypename='whileloop']">
#      <!--
#        w, logic(D,while.d)            , d=wb.d
#              c                 !c
#           c  wb,w,!c?(D,wb,!D) D,wb,!D
#           !c wb                wb
#      -->
        While = whileloop.While()
        While.visit(self)
        if self.globalopdependent or While.dependency == 'constant':
            whileloop.whileblock().visit(self)
        if not self.globalopdependent:
            if While.dependency == 'constant':
                whileloop.While.visit(self)
            if While.dependency != 'constant':
                self.globalopdependent = True
                whileloop.whileblock().visit(self)
                self.globalopdependent = False
#      <!--
#          wl:  w=c          w!=c
#               c  np l  nl  np np l  nl
#               np np l  nl  np np l  nl
#               l  l  l  nl  l  l  l  nl
#               nl nl nl nl  nl nl nl nl
#      -->
        whileloop.dependency = 'constant'
        for d in ('nonlinear', 'linear', 'noprobe'):
            if d == whileloop.whileblock().dependency:
                whileloop.dependency = d
                break

    def visit_forloop(self, forloop):
        raise RuntimeError("implement forloop")
#    <admst:when test="[datatypename='forloop']">
#      <admst:apply-templates select="initial|update" match="dependency"/>
#      <admst:apply-templates select="condition" match="e:dependency"/>
#      <admst:apply-templates select="[$globalopdependent='yes' or nilled((initial|condition|update)/[dependency!='constant'])]/forblock" match="dependency"/>
#      <admst:if test="[$globalopdependent='no']">
#        <admst:apply-templates select="(initial|update)/[dependency='constant']" match="dependency"/>
#        <admst:apply-templates select="condition[dependency='constant']" match="e:dependency"/>
#        <admst:if test="[condition/dependency!='constant' or initial/dependency!='constant' or update/dependency!='constant']">
#          <admst:variable name="globalopdependent" string="yes"/>
#          <admst:apply-templates select="forblock" match="dependency"/>
#          <admst:variable name="globalopdependent" string="no"/>
#        </admst:if>
#      </admst:if>
#      <!--
#          fl:  f=c          f!=c
#               c  np l  nl  np np l  nl
#               np np l  nl  np np l  nl
#               l  l  l  nl  l  l  l  nl
#               nl nl nl nl  nl nl nl nl
#      -->
#      <admst:choose>
#        <admst:when test="[forblock/dependency='nonlinear']">
#          <admst:value-to select="dependency" string="nonlinear"/>
#        </admst:when>
#        <admst:when test="[forblock/dependency='linear']">
#          <admst:value-to select="dependency" string="linear"/>
#        </admst:when>
#        <admst:when test="[(condition!='constant' or initial!='constant' or update!='constant') or forblock/dependency='noprobe']">
#          <admst:value-to select="dependency" string="noprobe"/>
#        </admst:when>
#        <admst:otherwise>
#          <admst:value-to select="dependency" string="constant"/>
#        </admst:otherwise>
#      </admst:choose>
#    </admst:when>
    def visit_case(self, Case):
#        pass
#    <admst:when test="[datatypename='case']">
        raise RuntimeError("implement case")
#      <admst:variable name="globaltreenode" path="case"/>
#      <admst:apply-templates select="case" match="e:dependency"/>
#      <admst:variable name="globaltreenode"/>
#      <admst:for-each select="caseitem">
#        <admst:for-each select="condition">
#          <admst:variable name="globaltreenode" path="."/>
#          <admst:apply-templates select="." match="e:dependency"/>
#          <admst:variable name="globaltreenode"/>
#        </admst:for-each>
#        <admst:apply-templates select="code" match="dependency"/>
#      </admst:for-each>
#    </admst:when>
    def visit_conditional(self, conditional):
        self.globalmodule.conditional.append(conditional.id)
        conditional.If().visit(self)
        if (not self.globalopdependent) and conditional.If().dependency != 'constant':
            self.globalopdependent = True
            conditional.Then().visit(self)
            if conditional.Else:
                conditional.Else().visit(self)
            self.globalopdependent = False
        else:
            conditional.Then().visit(self)
            if conditional.Else:
                conditional.Else().visit(self)
#      <!--
#          cd:  i=c          i!=c
#               c  np l  nl  np np l  nl
#               np np l  nl  np np l  nl
#               l  l  l  nl  l  l  l  nl
#               nl nl nl nl  nl nl nl nl
#      -->

        if conditional.Else:
            deps = [conditional.Then().dependency, conditional.Else().dependency]
        else:
            deps = [conditional.Then().dependency,]
        conditional.dependency = 'constant'
        for d in ('nonlinear', 'linear', 'noprobe',):
            if d in deps:
                conditional.dependency = d
                break

    def visit_contribution(self, contribution):
        self.globalcontribution = contribution
        contribution.rhs().visit(self)
        self.globalcontribution = None
        contribution.lhs().probe
        for probe in contribution.rhs().probe:
            contribution.lhs().probe.append(probe)
        contribution.dependency = 'nonlinear'

    def visit_assignment(self, assignment):
        assignment.TemperatureDependent = False
        ldn = assignment.get_datatypename()
        if ldn == 'array':
            lhs = assignment.lhs().variable()
        else:
            lhs = assignment.lhs()

        if self.globalpartitionning == 'initial_model':
            lhs.prototype().setinmodel = True
        elif self.globalpartitionning == 'initial_instance':
            lhs.prototype().setininstance = True
        elif self.globalpartitionning == 'initial_step':
            lhs.prototype().setininitial_step = True
        elif self.globalpartitionning == 'noise':
            lhs.prototype().setinnoise = True
        elif self.globalpartitionning == 'final_step':
            lhs.prototype().setinfinal = True
        else:
            lhs.prototype().setinevaluate = True

        self.globalassignment = assignment
        rhs = assignment.rhs()
        rhs.visit(self)
        self.globalassignment = None

        if not hasattr(lhs, 'variable'):
            lhs.variable = []

        lhs.TemperatureDependent = False
        for x in rhs.variable:
            if x not in lhs.variable:
                lhs.variable.append(x)
                if rhs.TemperatureDependent:
                    lhs.TemperatureDependent = rhs.TemperatureDependent
#      <!--
#        d=rhs.d,d=(c and D)?np
#        l(l,r,$globalopdependent)
#        $globalopdependent='no'  $globalopdependent='yes'
#        c  np l  nl               np np l  nl
#        np np l  nl               np np l  nl
#        l  l  l  nl               l  l  l  nl
#        nl nl nl nl               nl nl nl nl
#      -->
        assignment.dependency = rhs.dependency

        deps = [lhs.prototype().dependency, rhs.dependency]

        lhs.dependency = 'constant'
        lhs.prototype().dependency = 'constant'
        isset = False
        for d in ('nonlinear', 'linear', 'noprobe'):
            if d in deps:
                lhs.dependency = d
                lhs.prototype().dependency = d
                isset = True
                break

        if (not isset) and self.globalopdependent:
            lhs.dependency = 'noprobe'
            lhs.prototype().dependency = 'noprobe'
        for probe in rhs.probe:
            lhs.probe.append(probe, True)
#      </admst:choose>
#      <admst:push into="$lhs/probe" select="rhs/probe" onduplicate="ignore"/>
#    </admst:when>
    def visit_block(self, block):
        forcepartitionning = True
        name = block.lexval
        if name in  ('initial_model', 'initial_instance', 'initial_step', 'noise', 'final_step,'):
            self.globalpartitionning = name
            forcepartitionning = True
        else:
            forcepartitionning = False

        for item in block.item.get_list():
            item.visit(self)

        if forcepartitionning:
            self.globalpartitionning = None

        deps = set([x.dependency for x in block.item.get_list()])
        block.dependency = 'constant'
        for d in ('nonlinear', 'linear', 'noprobe'):
            if d in deps:
                block.dependency = d
                break

    def visit_nilled(self, nilled):
        nilled.dependency = 'constant'

    def visit_blockvariable(self, blockvariable):
        pass
#
# start implementation
#
#  <admst:reverse select="/argv|/discipline|/nature"/>
#  <admst:for-each select="/nature">
#    <admst:value-to select="ddt_nature" path="/nature[name='%(../../ddt_name)']"/>
#    <admst:value-to select="idt_nature" path="/nature[name='%(../../idt_name)']"/>
#  </admst:for-each>
#</admst:template>
#
#
#
#</admst>
#  <admst:template match="modify">
#    <admst:choose>
#      <admst:when test="[datatypename='block']">
#        <admst:apply-templates select="reverse(item)" match="modify"/>
#        <admst:value-to test="item[#modifys=1]" select="#modifys" path="1"/>
#        <admst:value-to test="item[#modifyd=1]" select="#modifyd" path="1"/>
#        <admst:value-to test="item[#modifyn=1]" select="#modifyn" path="1"/>
#        <admst:value-to test="item[#modifyc=1]" select="#modifyc" path="1"/>
#      </admst:when>
#      <admst:when test="[datatypename='conditional']">
#        <admst:apply-templates select="else|then" match="modify"/>
#        <admst:value-to test="[then/#modifys=1 or else/#modifys=1]" select="#modifys|if/#modifys|if/variable/#modifys" path="1"/>
#        <admst:value-to test="[then/#modifyd=1 or else/#modifyd=1]" select="#modifyd|if/#modifyd|if/variable/#modifyd" path="1"/>
#        <admst:value-to test="[then/#modifyn=1 or else/#modifyn=1]" select="#modifyn|if/#modifyn|if/variable/#modifyn" path="1"/>
#        <admst:value-to test="[then/#modifyc=1 or else/#modifyc=1]" select="#modifyc|if/#modifyc|if/variable/#modifyc" path="1"/>
#      </admst:when>
#      <admst:when test="[datatypename='whileloop']">
#        <admst:apply-templates select="whileblock" match="modify"/>
#        <admst:value-to test="[whileblock/#modifys=1]" select="#modifys|while/#modifys|while/variable/#modifys" path="1"/>
#        <admst:value-to test="[whileblock/#modifyd=1]" select="#modifyd|while/#modifyd|while/variable/#modifyd" path="1"/>
#        <admst:value-to test="[whileblock/#modifyn=1]" select="#modifyn|while/#modifyn|while/variable/#modifyn" path="1"/>
#        <admst:value-to test="[whileblock/#modifyc=1]" select="#modifyc|while/#modifyc|while/variable/#modifyc" path="1"/>
#        <admst:apply-templates select="whileblock" match="modify"/>
#      </admst:when>
#      <admst:when test="[datatypename='forloop']">
#        <admst:choose>
#          <admst:when test="[update/lhs/datatypename='array']">
#            <admst:variable name="lhs" path="update/lhs/variable"/>
#          </admst:when>
#          <admst:otherwise>
#            <admst:variable name="lhs" path="update/lhs"/>
#          </admst:otherwise>
#        </admst:choose>
#        <admst:apply-templates select="forblock" match="modify"/>
#        <admst:value-to test="[forblock/#modifys=1]" select="#modifys|(condition|update)/#modifys|(condition|update/rhs)/($lhs|variable)/#modifys" path="1"/>
#        <admst:value-to test="[forblock/#modifyd=1]" select="#modifyd|(condition|update)/#modifyd|(condition|update/rhs)/($lhs|variable)/#modifyd" path="1"/>
#        <admst:value-to test="[forblock/#modifyn=1]" select="#modifyn|(condition|update)/#modifyn|(condition|update/rhs)/($lhs|variable)/#modifyn" path="1"/>
#        <admst:value-to test="[forblock/#modifyc=1]" select="#modifyc|(condition|update)/#modifyc|(condition|update/rhs)/($lhs|variable)/#modifyc" path="1"/>
#        <admst:apply-templates select="forblock" match="modify"/>
#      </admst:when>
#      <admst:when test="[datatypename='case']">
#        <admst:apply-templates select="caseitem/code" match="modify"/>
#        <admst:for-each select="caseitem">
#          <admst:value-to test="[code/#modifys=1 and defaultcase='no']" select="#modifys|condition/#modifys|condition/@variable/#modifys" path="1"/>
#          <admst:value-to test="[code/#modifyd=1 and defaultcase='no']" select="#modifyd|condition/#modifyd|condition/@variable/#modifyd" path="1"/>
#          <admst:value-to test="[code/#modifyn=1 and defaultcase='no']" select="#modifyn|condition/#modifyn|condition/@variable/#modifyn" path="1"/>
#          <admst:value-to test="[code/#modifyc=1 and defaultcase='no']" select="#modifyc|condition/#modifyc|condition/@variable/#modifyc" path="1"/>
#        </admst:for-each>
#        <admst:value-to test="caseitem[#modifys=1]" select="#modifys|case/@variable/#modifys" path="1"/>
#        <admst:value-to test="caseitem[#modifyd=1]" select="#modifyd|case/@variable/#modifyd" path="1"/>
#        <admst:value-to test="caseitem[#modifyn=1]" select="#modifyn|case/@variable/#modifyn" path="1"/>
#        <admst:value-to test="caseitem[#modifyc=1]" select="#modifyc|case/@variable/#modifyc" path="1"/>
#      </admst:when>
#      <admst:when test="[datatypename='assignment']">
#        <admst:choose>
#          <admst:when test="[lhs/datatypename='array']">
#            <admst:variable name="lhs" path="lhs/variable"/>
#          </admst:when>
#          <admst:otherwise>
#            <admst:variable name="lhs" path="lhs"/>
#          </admst:otherwise>
#        </admst:choose>
#        <admst:value-to test="$lhs[exists(prototype/instance[#modifys=1])]" select="#modifys|rhs/#modifys|rhs/variable/#modifys" path="1"/>
#        <admst:value-to test="$lhs[exists(prototype/instance[#modifyd=1])]" select="#modifyd|rhs/#modifys|rhs/variable/#modifyd" path="1"/>
#        <admst:value-to test="$lhs[exists(prototype/instance[#modifyn=1])]" select="#modifyn|rhs/#modifys|rhs/variable/#modifyn" path="1"/>
#        <admst:value-to test="$lhs[exists(prototype/instance[#modifyc=1])]" select="#modifyc|rhs/#modifys|rhs/variable/#modifyc" path="1"/>
#        <admst:value-to test="$lhs/ddxprobe" select="#ddxprobe" string="yes"/>
#        <admst:push into="rhs/variable/ddxprobe" select="$lhs/ddxprobe" onduplicate="ignore"/>
#      </admst:when>
#      <admst:when test="[datatypename='contribution']">
#        <admst:choose>
#          <admst:when test="[#fixmedynamic=1]">
#            <admst:value-to select="#modifyd|(lhs|rhs|rhs/variable)/#modifyd" path="1"/>
#          </admst:when>
#          <admst:when test="[#fixmeflickernoise=1]">
#            <admst:value-to select="flickernoise|lhs/flickernoise" string="yes"/>
#            <admst:value-to select="#modifyn|(lhs|rhs|rhs/variable)/#modifyn" path="1"/>
#          </admst:when>
#          <admst:when test="[#fixmewhitenoise=1]">
#            <admst:value-to select="whitenoise|lhs/whitenoise" string="yes"/>
#            <admst:value-to select="#modifyn|(lhs|rhs|rhs/variable)/#modifyn" path="1"/>
#          </admst:when>
#          <admst:otherwise>
#            <admst:value-to select="#modifys|(lhs|rhs|rhs/variable)/#modifys" path="1"/>
#          </admst:otherwise>
#        </admst:choose>
#      </admst:when>
#      <admst:when test="[datatypename='blockvariable']">
#      </admst:when>
#      <admst:when test="[datatypename='nilled']"/>
#      <admst:when test="[datatypename='callfunction']">
#        <admst:value-to select="#modifyc|function/arguments/variable/#modifyc" path="1"/>
#      </admst:when>
#      <admst:otherwise><admst:fatal format="%(datatypename): case not handled\n"/></admst:otherwise>
#    </admst:choose>
#  </admst:template>
#  <admst:apply-templates select="analog/code" match="modify"/>
#  <admst:push into="@analogitems" select="assignment|assignment/rhs|contribution|contribution/rhs|block|forloop|whileloop|case|callfunction|conditional|conditional/if"/>
#  <admst:value-to select="@analogitems[#modifys=1 or #modifyn=1 or #modifyc=1]/static" string="yes"/>
#  <admst:value-to select="@analogitems[#modifys!=1 and #modifyn!=1 and #modifyc!=1]/dynamic" string="yes"/>
#
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifys=1])]/#modifys" path="1"/>
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifyd=1])]/#modifyd" path="1"/>
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifyn=1])]/#modifyn" path="1"/>
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifyc=1])]/#modifyc" path="1"/>
#
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifys=1 or #modifyd=1 or #modifyn=1])]/insource" string="yes"/>
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifys=1 or #modifyn=1 or #modifyc=1])]/static" string="yes"/>
#  <admst:value-to select="(.|blockvariable)/variable[exists(instance[#modifyd=1])]/dynamic" string="yes"/>
#  <admst:value-to select="source[#modifys=1 or #modifyn=1]/static" string="yes"/>
#  <admst:value-to select="source[#modifyd=1]/dynamic" string="yes"/>
#
#  <!-- jacobian -->
#  <admst:for-each select="contribution">
#    <admst:variable name="mycontribution" path="."/>
#    <admst:variable name="mysource" path="lhs"/>
#    <admst:push into="$mysource/attribute" select="attribute"/>
#    <!-- case I() <+ .V(). -->
#    <admst:for-each select="rhs/probe[(nature=discipline/potential)and($mysource/nature=$mysource/discipline/flow)]">
#      <admst:new datatype="jacobian" inputs="module,$mysource/branch/pnode,branch/pnode">
#        <admst:push into="/@jacobian" select="." onduplicate="ignore"/>
#      </admst:new>
#      <admst:new test="branch/nnode[grounded='no']" datatype="jacobian" inputs="module,$mysource/branch/pnode,branch/nnode">
#        <admst:push into="/@jacobian" select="." onduplicate="ignore"/>
#      </admst:new>
#      <admst:new test="$mysource/branch/nnode[grounded='no']" datatype="jacobian" inputs="module,$mysource/branch/nnode,branch/pnode">
#        <admst:push into="/@jacobian" select="." onduplicate="ignore"/>
#        <admst:new test="../branch/nnode[grounded='no']" datatype="jacobian" inputs="module,$mysource/branch/nnode,../branch/nnode">
#          <admst:push into="/@jacobian" select="." onduplicate="ignore"/>
#        </admst:new>
#      </admst:new>
#      <admst:for-each select="/reverse(@jacobian)">
#        <admst:choose>
#          <admst:when test="module/jacobian[row=../../row and column=../../column]">
#            <admst:variable name="jacobian" path="module/jacobian[row=../../row and column=../../column]"/>
#          </admst:when>
#          <admst:otherwise>
#            <admst:variable name="jacobian" path="."/>
#            <admst:value-to select="[row=column]/diagonal" string="yes"/>
#            <admst:push into="module/jacobian" select="."/>
#          </admst:otherwise>
#        </admst:choose>
#        <admst:value-to test="$mycontribution[dynamic='yes']" select="$jacobian/dynamic" string="yes"/>
#        <admst:value-to test="$mycontribution[dynamic='no']" select="$jacobian/static" string="yes"/>
#      </admst:for-each>
#      <admst:value-to select="/@jacobian"/>
#    </admst:for-each>
#  </admst:for-each>
#  <admst:reverse select="jacobian"/>
#</admst:template>

