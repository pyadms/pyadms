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
for n in module.external_nodes.get_list():
    print(f' {n.name}')

print("\nINTERNAL NODES")
for n in module.internal_nodes.get_list():
    print(f' {n.name}')

model_parameters = [v for v in module.variableprototype.get_list() if (v.type == 'model' and v.input == True)]
# parameters
print("\nMODEL PARAMETERS")
for p in module.model_parameters.get_list():
        print(f'{p.name}')

instance_parameters = [v for v in module.variableprototype.get_list() if v.type == 'instance']
print("\nINSTANCE PARAMETERS")
for p in module.instance_parameters.get_list():
        print(f'{p.name}')

for i in module.analog().code().item.get_list():
        if i.datatypename == 'block':
            nprobe = len(list(i.probes.get_list()))
            print(f'block "{i.name}" has {nprobe} probes')
        else:
            nprobe = len(list(i.probes.get_list()))
            print(f'"{i.datatypename}" has {nprobe} probes')
        for j in ('has_resistive', 'has_ddt', 'has_noise'):
            p = getattr(i, j)
            print(f'"{j}={p}"')
