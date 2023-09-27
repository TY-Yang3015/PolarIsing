## Project Polaris: Pre-Release Versions

Welcome to the Pre-release Repo of Project `Polaris`. The stable release will start from the version code `1.0.0` as scheduled.

---

#### Current Released Versions: Release Notes

- 0.1.1: `Simulated_annealing` doesn't work, do not use this version
- 0.1.2: Bug fixed, minor optimisation
- 0.2.0 (**major update**): 
  - Now support field visulisation via `visualise_field()` method.
  - Now support custom colormap for field and lattice. 
  - Fatal errors for field prameter are fixed in all algorithms. 
  - The graph style, grid and labels are adjusted. 

---

#### How to Install?

Please download the `.zip` file in each version folder. After you unzip the file, you should see:

- `setup.py`

- Polaris
  - `__init__.py` and other `.py` files
  
(Please let me know if this is not the case for you.) To install the module, you need to:

1. Use a commandline/powershell, go to the directory that is the same as the `setup.py` file (by `cd` command). Or simply, you can create a **jupyter notebook** at this directory to execute the following steps.
2. Run `pip install .`
3. If installed successfully, you should see "Successfully installed Polaris-x.x.x". 
4. call `Polaris` in Python by `import Polaris`, just like `numpy` or `matplotlib`!

**Note**: do NOT use `pip install Polaris` command, since there exists a project on `PyPI` called `polaris` (irrelevant). You may want to setup a **virtual environment** before you install `Polaris`.

--- 

#### The Standard Routine: High-Level Interface

One should always start with `from Polaris import Ising_model`. Then do the following:

```python
model = Ising_model()
model.create_lattice(size=30) # can be any size

#set up the config, use wolff as an example
algorithm = 'wolff'
backend = 'python'
field = 1
inputs = [2.3, 1000, field, True]

model.simulate(algorithm, backend, inputs)
model.show_results()
```
Then you should see some graphs showing up.(Note: **The `show_results()` method automatically catches the field config for you**) If you want to conduct more complicated analysis, you can always access the **Low-Level Interface** by calling `Metropolis`, `Wolff`, `Analyser`, etc. You cna design more sophisticated routines based on these elemental classes. 



