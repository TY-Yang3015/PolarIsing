#!/usr/bin/env python
# coding: utf-8

# **Author:** Matthew Howarth

# In[5]:


import numpy as np
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm


# **Simulated Annealing Class**

# In[34]:


class Simulated_annealing:
    def __init__(self):
        self.annealing_schedule = None
    
    def execute(self, lattice, ti, tf, _type, iteration_step, field=False, progress_bar=False):
        # check if the lattice has been randomly initialised
        if abs(np.sum(lattice)) == lattice.shape[0]*lattice.shape[1]:
            raise ValueError('Lattice has not been randomly initialised.')

        if field == False: field = np.zeros((lattice.shape[0],lattice.shape[0]))

        # initialise the lists
        energy_list = [self._get_energy(lattice, field)]
        magnetisation_list = [np.sum(lattice)]

        # setup progress bar 
        if progress_bar: # stands for if progress_bar == True.
            pbar = tqdm(range(iteration_step))
            pbar.set_description('Simulated Annealing')

        self.annealing_schedule = self._make_annealing_schedule(_type, ti, tf, iteration_step)
    

        for n in range(iteration_step):
            delta_e, magnetisation, lattice = self._core(lattice, field, n)
            magnetisation_list.append(magnetisation)
            energy_list.append(energy_list[-1] + delta_e)
            if progress_bar: pbar.update(1)
        
        if progress_bar: pbar.close() # close the progress bar

        return energy_list, magnetisation_list, lattice

    def _core(self, lattice, field, n):
        T=self.annealing_schedule[n] #T(n)
        
        for _ in range(lattice.shape[0]*lattice.shape[0]):
            position=np.random.randint(lattice.shape[0],size=2) 
            local_energy_before=self._local_energy(lattice,field,position[0],position[1]) 
            lattice[position[0],position[1]]=-lattice[position[0],position[1]] #spin flip
            local_energy_after=self._local_energy(lattice,field,position[0],position[1]) 
            delta_e=local_energy_after-local_energy_before
        
            if delta_e<=0 or np.random.rand()<np.exp(-delta_e/T):
                pass
            else:
                lattice[position[0],position[1]]=-lattice[position[0],position[1]]
                delta_e=0
        
        magnetisation = np.sum(lattice)
        return delta_e , magnetisation, lattice

    def _get_energy(self, lattice, field):
        #global energy
        energy =  (-1 * np.sum(lattice * (np.roll(lattice, 1, axis=0) + np.roll(lattice, -1, axis=0) 
                                         + np.roll(lattice, 1 ,axis=1) + np.roll(lattice, -1, axis=1))) 
                                         - np.sum(lattice * field))
        return energy
    
    def _local_energy(self,lattice,field,i,j):
        L = lattice.shape[0]
        return -(lattice[i,j]*(lattice[(i+1)%L,j]+lattice[i,(j+1)%L]+lattice[(i-1)%L,j]+lattice[i,(j-1)%L]+field[i,j]))
    
    def _make_annealing_schedule(self, _type, ti, tf, iteration_step):
        #return annealing schedule.
        eq_time=iteration_step/4 #time for which temperature is stabilised at ti
        schedule_runtime=int(iteration_step-eq_time) 
        n=np.linspace(0,schedule_runtime,schedule_runtime) 
        delta_t=ti-tf
        equilibrium=(np.full((1,int(eq_time)),tf)).flatten() #array after reaching equilibrium, concactenated later.
        if _type not in ['log', 'linear','step']:
            raise ValueError('unknown type of annealing schedule.')
        if _type=='linear':
            annealing_schedule=np.linspace(ti,tf,schedule_runtime)
        if _type=='log':
            d=(schedule_runtime)/(np.exp(delta_t)-1)
            c=ti+np.log(d)
            annealing_schedule=-np.log(n+d)+c
        if _type=='step':
            line=np.linspace(ti,tf,schedule_runtime)
            annealing_schedule=np.floor(line)
        
        annealing_schedule=(np.concatenate([annealing_schedule,equilibrium],axis=0)).flatten()
        return annealing_schedule


# **Execution**

# In[38]:


#Variables
ti=30
tf=2
_type='step'
size=50
iteration_step=int(2000)
lattice = np.random.choice([-1,1], size=(size,size))
#random field
mu, sigma = 0, 0.2 # mean and standard deviation
#field = np.random.normal(mu, sigma, size=(size,size))

#execute
alg=Simulated_annealing()
energy_list, magnetisation_list, lattice=alg.execute(lattice, ti, tf, _type, iteration_step,field=False, progress_bar=True)


#Visualise
n=np.linspace(0,iteration_step+1,iteration_step+1)
annealing_schedule=alg._make_annealing_schedule(_type, ti, tf, iteration_step)

plt.plot(annealing_schedule)
plt.xlabel('n')
plt.ylabel('T(n)')
plt.title('Annealing Schedule')
plt.grid()
plt.show()



plt.subplot(1,2,1)
plt.plot(n,magnetisation_list)
plt.xlabel('n')
plt.ylabel('Magnetisation')
plt.title('Magnetisation')


plt.subplot(1,2,2)
plt.plot(n[int((7/8)*iteration_step):iteration_step],magnetisation_list[int((7/8)*iteration_step):iteration_step])
plt.xlabel('n')
plt.ylabel('Magnetisation')
plt.title('Magnetisation Near End of Cycle')
plt.subplots_adjust(wspace=0.5)
plt.show()



plt.subplot(1,2,1)
plt.plot(n,energy_list)
plt.xlabel('n')
plt.ylabel('Global Energy')
plt.title('Global Energy')

plt.subplot(1,2,2)
plt.plot(n[int(0.95*iteration_step):iteration_step],energy_list[int(0.95*iteration_step):iteration_step])
plt.xlabel('n')
plt.ylabel('Energy')
plt.title('Energy Near End of Cycle')
plt.subplots_adjust(wspace=0.5)
plt.show()


plt.imshow(lattice, cmap='binary', vmin=-1, vmax=1, extent=(0, size, 0, size))
plt.title(f'$T_i={ti}$,$T_f={tf}$,{iteration_step} iterations')
plt.show()


# In[ ]:




