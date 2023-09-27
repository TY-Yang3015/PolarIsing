

<img src="https://github.com/TeamIcing/Demo_Release/assets/107746785/61bb0446-1492-424b-9a01-93874b5c26be" alt="diagram-20230623" width="400"/>


Welcome to the release Repo of Project PolarIsing. The stable release `1.0.0` is now available.!
**Warning: from `0.5.0` onwards, `tensorflow<2.11` will be required to install the module.** See [this page](https://www.tensorflow.org/install/pip) for how to install `tensorflow`. 

---

**A image from our cGAN**:

<img src="https://github.com/TeamIcing/Demo_Release/assets/107746785/e8ab6dc2-8b2e-4cec-8d91-f518756ff431" alt="242946150-05b4500f-2a4e-4185-9cc0-faa47d6e957e" width="600"/>


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
 
- 1.0.0 (**stable release**)
  - Module renamed as `PolarIsing`, combined `Polaris`, `Polarise` and `Ising`.
  - Added dynamic file handling system for the `cGAN` submodule, with `File_dir_handler` class; now support manual directory input.
  - Now the mandatory random-initialisation restriction on `metropolis` algorithm is removed, only `RuntimeWarning` will be shown.
  - Errors about temperature restriction in `Wolff` are now fixed.
  - The model size has been **significantly reduced**. (only ~ 600 MB now, was ~ 2 GB for `0.5.0`)
  - Improved error handling and warning systems.

---

### How to Install?

Please download the `.zip` file in each version folder. After you unzip the file, you should see:

- `setup.py`

- PolarIsing
  - `__init__.py` and other `.py` files
  
(Please let me know if this is not the case for you.) To install the module, you need to:

1. Use a commandline/powershell, go to the directory that is the same as the `setup.py` file (by `cd` command). Or simply, you can create a **jupyter notebook** at this directory to execute the following steps.
2. Run `pip install .`
3. If installed successfully, you should see "Successfully installed PolarIsing-x.x.x". 
4. call `PolarIsing` in Python by `import PolarIsing`, just like `numpy` or `matplotlib`!

**Note**: Why are the files for `0.5.0` onwards are so large? Since the network itself contains pre-trained parameters and datasets, it's hard to reduce the size of the file. I will do my best to reduce the file size in the future releases. 

--- 

### The Standard Routines

From `0.5.0` version onwards, the original functions are moved into the `Simulator` submodule. Here is a short standard routine. (It didn't change a lot, but the `backend` parameter was abolished)

```python
# import prerequisites
from PolarIsing.Simulator import Ising_model
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

Here we introduce the access routine for `PolarIsing.cGAN`. Before you run the submodule, please make sure there is sufficient amount of memory (GPU, CPU). The only class you need will be `cGAN_Interface`. You need to switch the module mode from `present` to `beyond`, by running the following lines

```python

import PolarIsing

Polaris.__mode__ = 'beyond'

```

check it by `print(PolarIsing.__mode__)`, see if it's `'beyond'`. This is similar to the `tensorflow.nightly` provisonal support. This system is here to protect you from OS crush. If this is successful, then:

```python

from PolarIsing.cGAN import cGAN_Interface
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

(Note: for some temperatures，you may see a `KeyError` being raised, that's due to the data miss when the GAN was trained.) 

For the first run it will be considerably slower, please bear with it. It will accelerate when used more times, especially when you have your GPU available. (require CUDNN and CUDA from NVIDIA)

If you see any error about the path or file, always check your current working directory. You can easily manage your directories by invoking the `File_dir_handler` class. Please refer to the source code. The `manual_dir` parameter in `fit()` will allow you to manually specify the directory of the `label_mapping.txt` file. 

---

