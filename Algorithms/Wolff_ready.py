import matplotlib.pyplot as plt
import numpy as np
from tqdm.notebook import tqdm

class Wolff:
    def __init__(self):
        pass
     
    def execute(self, lattice, temperature, iteration_step, field=False, progress_bar=False):
        # check if the lattice has been randomly initialised
        if abs(np.sum(lattice)) == lattice.shape[0]*lattice.shape[1]:
            raise ValueError('Lattice has not been randomly initialised.')
            
        from warnings import warn
        if T < 2.2 and field == False:
            warn('time required for T < Tc is significantly longer. try metropolis instead.', RuntimeWarning)
        
        # if no external field given
        if field == False: field = 0
            
        # initialise the lists
        energy_list = [self._get_energy(lattice, field)]
        magnetisation_list = [np.sum(lattice)]
        
        # setup progress bar 
        if progress_bar: 
            pbar = tqdm(range(iteration_step))
            pbar.set_description('Wolff')
           
        # start iterations
        for _ in range(iteration_step):
            energy, magnetisation, lattice = self._core(lattice, temperature, field)
            magnetisation_list.append(magnetisation)
            energy_list.append(energy)
            if progress_bar: pbar.update(1)
        
        return energy_list, magnetisation_list, lattice
    
    def _core(self, lattice, temperature, field):
        L = lattice.shape[0]

        i, j = np.random.randint(0, N, 2)
        cluster = [(i, j)]
        cluster_spin = lattice[i, j]
        stack = [(i, j)]

        while stack:
            i, j = stack.pop()
            neighbors = [((i-1)%L, j), ((i+1)%L, j), (i, (j-1)%L), (i, (j+1)%L)]

            for neighbor in neighbors:
                if lattice[neighbor] == cluster_spin and neighbor not in cluster:
                    # SW Criterion
                    if np.random.rand() < 1 - np.exp(-2 /  T):
                        cluster.append(neighbor)
                        stack.append(neighbor)
                        
        if field != 0:
            delta_field_e = -1*(lattice*field)
            for i, j in cluster:
                lattice[i, j] *= -1
            delta_field_e += lattice*field
            
            # field energy Metropolis Criterion
            if delta_field_e < 0 or np.random.rand() < np.exp(-delta_field_e / T):
                pass
            else:
                for i, j in cluster:
                    lattice[i, j] *= -1


        else:
            for i, j in cluster:
                lattice[i, j] *= -1
            
        energy = self._get_energy(lattice, field)
        magnetisation = np.sum(lattice)

        return energy, magnetisation, lattice
    
    # you can use this energy function for the global energy, provided for your convinience.
    def _get_energy(self, lattice, field):
        energy =  (-1 * np.sum(lattice * (np.roll(lattice, 1, axis=0) + np.roll(lattice, -1, axis=0) 
                                         + np.roll(lattice, 1 ,axis=1) + np.roll(lattice, -1, axis=1))) 
                                         - np.sum(lattice * field))
        return energy
   
