
class printer:

    def __init__(self):
        pass

    def visit_module(self, module):
        print(f'MODULE {module.name}')
        print(', '.join([n.name for n in module.external_nodes.get_list()]))

        all_nodes = list(module.external_nodes.get_list())
        all_nodes.extend(list(module.internal_nodes.get_list()))
        for n in all_nodes:
            print(f'{n.name} {n.discipline().name} {n.direction}')

        model_parameters = [v for v in module.variableprototype.get_list() if (v.type == 'model' and v.input == True)]
        print("\nMODEL PARAMETERS")
        for p in module.model_parameters.get_list():
            print(f'{p.name}')

        instance_parameters = [v for v in module.variableprototype.get_list() if v.type == 'instance']
        print("\nINSTANCE PARAMETERS")
        for p in module.instance_parameters.get_list():
            print(f'{p.name}')

        print("\nGLOBAL VARIABLES")
        for v in module.variableprototype.get_list():
            if not v.input:
                print(f'{v.name}')

        # Analog functions
        for analogfunction in module.analogfunction.get_list():
            analogfunction.visit(self)

        # Block Items
        print(f'\nVISIT MODULE CODE')
        module.analog().code().visit(self)

    def visit_block(self, block):
        print(f'\nVISIT BLOCK "{block.name}"')

        for item in block.item.get_list():
            print(item.datatypename)
