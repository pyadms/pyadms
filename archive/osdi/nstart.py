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
for n in module.node.get_list():
    if n.grounded or (n.location == 'internal'):
        continue
    print(f' {n.name}')

# parameters
print("\nMODEL PARAMETERS")
for v in module.variableprototype.get_list():
    if v.type == 'model':
        print(v.name)
print("\nINSTANCE PARAMETERS")
for v in module.variableprototype.get_list():
    if v.type == 'instance':
        print(v.name)
