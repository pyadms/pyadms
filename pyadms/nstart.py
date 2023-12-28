import adms_loader
import visitor as visitor
import sys

admst = adms_loader.load_json(sys.argv[1])
dv = visitor.dependency_visitor()
admst.get_module().visit(dv)
