# from importlib import import_module

# def _get(data, index=0, e=None):
# 	try:return data[index] if type(data) in (list, dict, set, tuple) else data
# 	except:return e

# def require(module, package=None, args=[], kwargs={}, var=False):
# 	"""Import a module for only a particular function
# The 'module' argument vspecifies the module to import

# The 'package' argument is required when performing a relative import. It specifies the package to use as the anchor point from which to resolve the relative import to an absolute import.

# The function recieving the decorator must also recieve the module(s) as parameter(s)

# 	@require(["numpy", "pandas"])
# 	def main(np, pd):
# 		...

# 	@require("numpy")
# 	def main(np):
# 		...

# You could also assign the modules to variables
# 	np = require("numpy")

# 	np, pd, plt = require(["numpy", "pandas", "matplotlib.plot"])

# """
# 	if type(module) is str and type(package) in (str, None):
# 		modules = import_module(module, package)
# 	elif type(module) is list:
# 		modules = []
# 		for x in module:
# 			packag = _get(package, x)
# 			modules.append([import_module(x, packag)])
# 	else:modules=[]
	
# 	if var == False:
# 		def wrap(func):
# 			func(*modules, *args, **kwargs)
# 		return wrap
# 	else:
# 		return modules

import sys

def _get(data, index=0, e=None):
    try:return data[index] if type(data) in (list, dict, set, tuple) else data
    except:return e

def load(target, **namespace):
	# Source bottle.py:load
	module, target = target.split(":", 1) if ':' in target else (target, None)
	if module not in sys.modules: __import__(module)
	if not target: return sys.modules[module]
	if target.isalnum(): return getattr(sys.modules[module], target)
	package_name = module.split('.')[0]
	namespace[package_name] = sys.modules[package_name]
	return eval('%s.%s' % (module, target), namespace)

class require:
    def __init__(self, module):
        """Import a module for only a particular function
The 'module' argument vspecifies the module to import

The 'package' argument is required when performing a relative import. It specifies the package to use as the anchor point from which to resolve the relative import to an absolute import.

The function recieving the decorator must also recieve the module(s) as parameter(s)

Other function related arguments are passed when calling the function
```python
    @require(["numpy", "pandas"])
    def main(np, pd, x):
        ...
        print(x)
    
    main(5)
    # prints 5

    @require("numpy")
    def main(np):
        ...
```
You can also call specific functions from modules
```python
	@require("numpy:array")
	def plt(func, array):
		arr = func(array)
		return arr
	plt([2,4,5,6,8])

 # Is same as:

	def plt(array):
		from numpy import array as func
		arr = func(array)
		return arr
	plt([2,4,5,6,8])
```
You could also assign the modules to variables.. just put an extra parentheses to simulate function call
```python
    np = require("numpy")()

    np, pd, plt = require(["numpy", "pandas", "matplotlib.plot"])()
```
"""
        self.module = module
        
        if type(self.module) is str:
            self.modules = load(self.module)
        elif type(self.module) is list:
            self.modules = []
            for x in self.module:
                self.modules.append(load(x))
        else:self.modules=[]
    
    def __call__(self, func=None):
        if not func:
            return self.modules
        if type(self.modules) is not list:
            self.modules = [self.modules]
        return wrap(func, self.modules)
 
class wrap:
    def __init__(self, f, m):
        self.f = f
        self.m = m
    
    def __call__(self, *args, **kwargs):
        return self.f(*self.m, *args, **kwargs)
