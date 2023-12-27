import pyadms.adms_loader
import pyadms.visitor as visitor
import sys

admst = pyadms.adms_loader.load_json(sys.argv[1])
dv = visitor.dependency_visitor()
admst.get_module().visit(dv)




