import pyadms
from pyadms import adms_loader
from pyadms import adms_visitor
from pyadms import adms_printer
import sys

def run():
    admst = adms_loader.load_json(sys.argv[1])
    dv = adms_visitor.dependency_visitor()
    module = admst.get_module()
    module.visit(dv)

    # # external nodes
    # print("\nEXTERNAL NODES")
    # for n in module.external_nodes.get_list():
    #     print(f' {n.name}')

    # print("\nINTERNAL NODES")
    # for n in module.internal_nodes.get_list():
    #     print(f' {n.name}')

    # model_parameters = [v for v in module.variableprototype.get_list() if (v.type == 'model' and v.input == True)]
    # print("\nMODEL PARAMETERS")
    # for p in module.model_parameters.get_list():
    #     print(f'{p.name}')

    # instance_parameters = [v for v in module.variableprototype.get_list() if v.type == 'instance']
    # print("\nINSTANCE PARAMETERS")
    # for p in module.instance_parameters.get_list():
    #     print(f'{p.name}')

    for i in module.analog().code().item.get_list():
        if i.datatypename == 'block':
            nprobe = len(list(i.probes.get_list()))
            print(f'block "{i.name}" has {nprobe} probes')
        else:
            nprobe = len(list(i.probes.get_list()))
            print(f'"{i.datatypename}" has {nprobe} probes')
        for j in ('has_resistive', 'has_ddt', 'has_noise', 'has_ddx'):
            p = getattr(i, j)
            print(f'"{j}={p}"')

    print("\nANALOG FUNCTIONS")
    for i in module.analogfunction.get_list():
        print(f'analog function {i.name}')

    print("\nCONTRIBUTIONS")
    for i in module.contribution.get_list():
        print(i.uid)
        for j in ('has_resistive', 'has_ddt', 'has_noise', 'has_ddx'):
            p = getattr(i, j)
            print(f'"{j}={p}"')
        for j in i.nodes.get_list():
            print(j.uid)


    print('\n\nBEGIN PRINT\n')
    printer = adms_printer.printer()
    module.visit(printer)

if __name__ == '__main__':
    run()
