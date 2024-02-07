
class printer:

    def __init__(self):
        pass

    def visit_module(self, module):
        print(f'MODULE {module.name}')
        print(', '.join([m.name for m in module.external_nodes.get_list()]))

