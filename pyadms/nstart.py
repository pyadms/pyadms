import pyadms.adms_loader
import pyadms.adms_implicit as adms_implicit

admst = pyadms.adms_loader.load_json('foo.json')
dv = adms_implicit.dependency_visitor()
admst.get_module().visit(dv)




