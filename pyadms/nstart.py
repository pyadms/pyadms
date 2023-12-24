import pyadms.adms_loader
import pyadms.adms_implicit as adms_implicit
import sys

admst = pyadms.adms_loader.load_json(sys.argv[1])
dv = adms_implicit.dependency_visitor()
admst.get_module().visit(dv)




