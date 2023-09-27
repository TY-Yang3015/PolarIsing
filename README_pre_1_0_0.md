# Project Polaris

Welcome to the Pre-release Repo of Project `Polaris`. The stable release will start from the version code `1.0.0` as scheduled.

**Warning: from `0.5.0` onwards, `tensorflow<2.11` will be required to install the module.** See [this page](https://www.tensorflow.org/install/pip) for how to install `tensorflow`. 

---

**A image from our cGAN**:

![image_at_epoch_0056](https://github.com/TeamIcing/Demo_Release/assets/107746785/05b4500f-2a4e-4185-9cc0-faa47d6e957e)


---

### Current Released Versions: Release Notes

- 0.1.1: `Simulated_annealing` doesn't work, do not use this version
- 0.1.2: Bug fixed, minor optimisation
- 0.2.0 (**major update**): 
  - Now support field visulisation via `visualise_field()` method.
  - Now support custom colormap for field and lattice. 
  - Fatal errors for field prameter are fixed in all algorithms. 
  - The graph style, grid and labels are adjusted. 
- 0.5.0 (**crucial major update**)
  - Now support conditional generative adversarial netwrok (cGAN) in 'beyond' mode.
  - The interface has been re-designed. Now `Polaris` consists of two submodules `Polaris.cGAN` and `Polaris.Simulator`
  - minor bug fixed.

---

### How to Install?

Please download the `.zip` file in each version folder. After you unzip the file, you should see:

- `setup.py`

- Polaris
  - `__init__.py` and other `.py` files
  
(Please let me know if this is not the case for you.) To install the module, you need to:

1. Use a commandline/powershell, go to the directory that is the same as the `setup.py` file (by `cd` command). Or simply, you can create a **jupyter notebook** at this directory to execute the following steps.
2. Run `pip install .`
3. If installed successfully, you should see "Successfully installed Polaris-x.x.x". 
4. call `Polaris` in Python by `import Polaris`, just like `numpy` or `matplotlib`!

**Note 1**: do NOT use `pip install Polaris` command, since there exists a project on `PyPI` called `polaris` (irrelevant). You may want to setup a **virtual environment** before you install `Polaris`.

**Note 2**: Why are the files for `0.5.0` onwards are so large? Since the network itself contains pre-trained parameters and datasets, it's hard to reduce the size of the file. I will do my best to reduce the file size in the future releases. 

--- 

### The Standard Routines

From `0.5.0` version onwards, the original functions are moved into the `Simulator` submodule. Here is a short standard routine. (It didn't change a lot, but the `backend` parameter was abolished)

```python
# import prerequisites
from Polaris.Simulator import Ising_model
import numpy as np

#create Ising_model instance
model = Ising_model()
model.create_lattice(50) #put size here

# use wolff with external field as an example
algorithm = 'wolff'
field = np.random.normal(0, 1, size=(50, 50))
inputs = [2.3, 1000, field, True]

# run the simulation and show results
model.simulate(algorithm, inputs);
model.show_results()

```

Here we introduce the access routine for `Polaris.cGAN`. Before you run the submodule, please make sure there is sufficient amount of memory (GPU, CPU). The only class you need will be `cGAN_Interface`. You need to switch the module mode from `present` to `beyond`, by running the following lines

```python

import Polaris

Polaris.__mode__ = 'beyond'

```

check it by `print(Polaris.__mode__)`, see if it's `'beyond'`. This is similar to the `tensorflow.nightly` provisonal support. This system is here to protect you from OS crush. If this is successful, then:

```python

from Polaris.cGAN import cGAN_Interface
ci = cGAN_Interface()


```

If everything goes right, you should see it asks:

```
'By using the "beyond" mode, it is assumed that you understand the potential risk and damage to the system or hardware.
Input y/Y to continue. Input e/E to exit'
```
Simply type `y` or `Y` to continue. (or `e` / `E` to exit) Now you can use the cGAN to generate graphs. 

```python
ci.generate_and_save() # returns 251 lattices at once.
ci.fit(#temperature from 1.50 to 4.00, 2dp required) # returns only one image at the given temp.
```

(Note: for some temperatures you may see a `KeyError` being raised, that's due to the data miss when the GAN was trained. Will fix it in future.) 

For the fisrt run it will be considerably slow, please bear with it. It will accelerate when used more times, especially when you have your GPU available. (require CUDNN and CUDA from NVIDIA)

---
