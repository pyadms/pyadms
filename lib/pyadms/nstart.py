import pyadms
from pyadms import adms_loader
from pyadms import visitor
import sys

admst = adms_loader.load_json(sys.argv[1])
dv = visitor.dependency_visitor()
admst.get_module().visit(dv)
