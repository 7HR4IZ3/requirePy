# requirePy
Import a module for only a particular function
The 'module' argument vspecifies the module to import

The 'package' argument is required when performing a relative import. It specifies the package to use as the anchor point from which to resolve the relative import to an absolute import.

The function recieving the decorator must also recieve the module(s) as parameter(s)

Other function related arguments are passed when calling the function

# Usage
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
