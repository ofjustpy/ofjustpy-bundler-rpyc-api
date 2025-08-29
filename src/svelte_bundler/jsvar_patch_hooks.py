from unittest.mock import patch
import importlib
import sys
import inspect

from jsexprs import JSVar



    
def list_jsvars_in_module(mod_name,
                                       dep_modules):

    class JSVarWrapper:

        def __init__(self, *args, **kwargs):
            self.import_stmts = set()
            self.var_map_key_value_stmt = set()
            pass
            
        def __call__(self, *args, **kwargs):
            print("JSVar args", args)
            print(f"""import {{ {args[1]} }} from "{args[0]}";""")
            
            self.import_stmts.add(f"""import {{ {args[1]} }} from "{args[0]}";""")

            self.var_map_key_value_stmt.add(f"  {args[1]}: {args[1]}")
            return JSVar(*args, **kwargs)
        def __getattr__(self, name):
            assert False
            


    if mod_name in sys.modules:
        del sys.modules[mod_name]

    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]
        
    with patch('jsexprs.JSVar', new=JSVarWrapper(JSVar)
               ):
        target_mod = importlib.import_module(mod_name)

        

        
