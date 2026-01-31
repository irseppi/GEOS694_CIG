import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def get_t(v0,l,c,tprime0,tpr):
    t_array = []	
    for tprime in tpr:
        t = ((tprime - tprime0 + l/c) - np.sqrt((tprime - tprime0 + l/c)**2 - 
            (1 - v0**2 / c**2)*((tprime - tprime0 + l/c)**2 - l**2/c**2))) / (1 
            - v0**2 / c**2)
        t_array.append(t)
    return t_array

def get_f(v0,l,c,t_array,f0):
    ft = []
    for t in t_array:
        ft0p = f0 / (1 + (v0/c) * (v0*t) / (np.sqrt(l**2 + (v0*t)**2)))	
        ft.append(ft0p)
    return ft

varrying_variables = {
    'base': np.arange(0, 241, 1),  # Placeholder for time array
    'v0':  np.arange(0, 200, 20),
    'l':   np.arange(0, 5000, 200),
    'c':   np.arange(200, 500, 5),
    "t0'": np.arange(0, 240, 20),
    'f0':  np.arange(0, 250, 20)
}

cm = plt.cm.rainbow #set colormap

fig, axs = plt.subplots(2, 3, figsize=(14, 10))
axs      = axs.flatten()

for n, (var_name, var_values) in enumerate(varrying_variables.items()):

    f0      = 150 # Default frequancy of aircraft source (Hz)
    tprime0 = 120 # Default time .... (s)
    c       =  320 # Default speed of sound (m/s)
    v0      = 80 # Default speed of aircraft (m/s)
    l       = 4000 # Default closest approach between aircraft and sensor (m)
    tpr     = varrying_variables['base'] # Time array at sensor (s)

    tprime  = get_t(v0,l,c,tprime0,tpr)
    ft      = get_f(v0, l, c, tprime, f0)

    axs[n].plot(tpr, ft, 'k', linewidth=0.5, zorder=10)
    axs[n].axvline(tprime0, c='k', linewidth=0.5, zorder=10)

    axs[n].set_title('Varying ' + var_name)
    axs[n].set_ylim(50, 250)
    axs[n].set_xlim(0, 240)

    if n in [0, 3]:
        axs[n].set_ylabel('Frequency (Hz)')
    if n in [3, 4, 5]:
        axs[n].set_xlabel('Time (s)')

    if n == 0:
        continue

    norm = plt.Normalize(np.min(varrying_variables[var_name]), 
                         np.max(varrying_variables[var_name]))
    sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=axs[n], orientation='vertical', pad=0.02)

    for val in var_values:
        if n == 1:
            v0      = val
        elif n == 2:
            l       = val
        elif n == 3:
            c       = val
        elif n == 4:
            tprime0 = val
        elif n == 5:
            f0      = val
        
        tprime = get_t(v0, l, c, tprime0, tpr)
        ft     = get_f(v0, l, c, tprime, f0)

        axs[n].plot(tpr, ft, color=cm(norm(val)), linewidth=0.5)

plt.tight_layout()
plt.show()