# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm



class Metropolis:
    def __init__(self):
        # this is here in case we want to add variables in future
        pass
     
    def execute(self, lattice, temperature, iteration_step, field=False, progress_bar=False):
        
        # check if the lattice has been randomly initialised
        if abs(np.sum(lattice)) == lattice.shape[0]*lattice.shape[1]:
            raise ValueError('Lattice has not been randomly initialised.')
        
        # if no external field given
        if field == False: field = 0
            
        # initialise the lists
        energy_list = [self._get_energy(lattice, field)]
        magnetisation_list = [np.sum(lattice)]
        
        # setup progress bar 
        if progress_bar: # stands for if progress_bar == True. Please get used to this.
            pbar = tqdm(range(iteration_step))
            pbar.set_description('Metropolis')
       
        # start iterations   
        for _ in range(iteration_step):
            delta_e, magnetisation, lattice = self._core(lattice, temperature, field)
            magnetisation_list.append(magnetisation)
            energy_list.append(energy_list[-1] + delta_e)
            if progress_bar: pbar.update(1)
        
        if progress_bar: pbar.close()
        
        return energy_list, magnetisation_list, lattice
    
    def _core(self, lattice, temperature, field):
        
        L = lattice.shape[0]
        pair_list = [(i, j) for i in range(L) for j in range(L)]
        final_delta_e = 0
        
        for _ in range(L**2):
            
            i, j = pair_list.pop(int(np.random.randint(len(pair_list), size=1)))
            
            spin = -lattice[i, j]
            delta_e = -2 * spin * (lattice[(i + 1) % L, j] 
                                        + lattice[i, (j + 1) % L] + lattice[(i - 1) % L, j] + lattice[i, (j - 1) % L])


            if field == 0:
                pass
            else:
                delta_e += -2*field[i, j]*spin

            if delta_e < 0 or np.random.rand() < np.exp(-delta_e / (temperature)):
                lattice[i, j] = spin
            else: delta_e = 0
                
            final_delta_e += delta_e*2

        magnetisation = np.sum(lattice)


        return final_delta_e , magnetisation, lattice
    
    # you can use this energy function for the global energy, provided for your convinience.
    def _get_energy(self, lattice, field):
        energy =  (-1 * np.sum(lattice * (np.roll(lattice, 1, axis=0) + np.roll(lattice, -1, axis=0) 
                                         + np.roll(lattice, 1 ,axis=1) + np.roll(lattice, -1, axis=1))) 
                                         - np.sum(lattice * field))
        return energy
