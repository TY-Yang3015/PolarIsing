### PolarIsing 1.0.0

- 1.0.0 (**stable release**)
  - Module renamed as `PolarIsing`, combined `Polaris`, `Polarise` and `Ising`.
  - Added dynamic file handling system for the `cGAN` submodule, with `File_dir_handler` class; now support manual directory input.
  - Now the mandatory random-initialisation restriction on `metropolis` algorithm is removed, only `RuntimeWarning` will be shown.
  - Errors about temperature restriction in `Wolff` is now fixed.
  - The model size has been **significantly reduced**. (only ~ 600 MB now, was ~ 2 GB for `0.5.0`)
  - Improved error handling and warning systems.
 
The module is around ~600 MB. The link is: https://drive.google.com/file/d/169EJMzPd1yu2bQE3t7WSphn9Y7aAGGnW/view?usp=drive_link

