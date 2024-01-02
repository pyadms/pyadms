import pyadms
from pyadms import adms_loader
from pyadms import visitor
import sys

admst = adms_loader.load_json(sys.argv[1])
dv = visitor.dependency_visitor()
module = admst.get_module()
module.visit(dv)

# external nodes
print("\nEXTERNAL NODES")
external_nodes = [n for n in module.node.get_list() if n.location == 'external']
for n in external_nodes:
    print(f' {n.name}')

print("\nINTERNAL NODES")
internal_nodes = [n for n in module.node.get_list() if n.location == 'internal']
for n in internal_nodes:
    print(f' {n.name}')

model_parameters = [v for v in module.variableprototype.get_list() if (v.type == 'model' and v.input == True)]
# parameters
print("\nMODEL PARAMETERS")
for p in model_parameters:
        print(f'{p.name}')

instance_parameters = [v for v in module.variableprototype.get_list() if v.type == 'instance']
print("\nINSTANCE PARAMETERS")
for p in instance_parameters:
        print(f'{p.name}')

