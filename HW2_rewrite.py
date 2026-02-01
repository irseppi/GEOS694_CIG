import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def get_t(v0, l, c, tprime0, tpr):
    """Calculate time in source frame."""
    beta = v0 / c
    arg = tpr - tprime0 + l / c
    discriminant = arg**2 - (1 - beta**2) * (arg**2 - (l / c)**2)
    return (arg - np.sqrt(discriminant)) / (1 - beta**2)


def get_f(v0, l, c, t_array, f0):
    """Calculate observed frequency (Doppler effect)."""
    base = np.sqrt(l**2 + (v0 * t_array)**2)
    base_checked = np.where(base != 0, base, 1e-10)
    return f0 / (1 + (v0 / c) * (v0 * t_array) / base_checked)


# Default parameters
DEFAULTS = {
    'f0': 150,
    'tprime0': 120,
    'c': 320,
    'v0': 80,
    'l': 4000
}

# Variable ranges for plotting
VAR_RANGES = {
    'base': np.arange(0, 241, 1),
    'v0': np.arange(0, 200, 20),
    'l': np.arange(0, 5000, 200),
    'c': np.arange(200, 500, 5),
    'tprime0': np.arange(0, 240, 20),
    'f0': np.arange(0, 250, 20)
}

# Create subplots
fig, axs = plt.subplots(2, 3, figsize=(11, 7), sharex=True, sharey=True)
axs = axs.flatten()
cm = plt.cm.rainbow
tpr = VAR_RANGES['base']

# Plot for each variable
var_names = list(VAR_RANGES.keys())
for n, var_name in enumerate(var_names):
    params = DEFAULTS.copy()
    
    # Base plot with default parameters
    tprime = get_t(params['v0'], params['l'], params['c'], 
                   params['tprime0'], tpr)
    ft = get_f(params['v0'], params['l'], params['c'], tprime, params['f0'])
    
    axs[n].plot(tpr, ft, c='k', linewidth=0.5, zorder=10)
    axs[n].axvline(params['tprime0'], c='k', linewidth=0.5, zorder=10)
    axs[n].set_title(f'Varying {var_name}')
    axs[n].set_ylim(100, 225)
    axs[n].set_xlim(0, 240)
    
    # Set labels
    if n in [0, 3]:
        axs[n].set_ylabel('Frequency (Hz)')
    if n in [3, 4, 5]:
        axs[n].set_xlabel('Time (s)')
    
    # Skip colorbar for first plot
    if n == 0:
        continue
    
    # Add colorbar and varied plots
    var_values = VAR_RANGES[var_name]
    norm = plt.Normalize(var_values.min(), var_values.max())
    sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
    plt.colorbar(sm, ax=axs[n], orientation='vertical', pad=0.01, aspect=30)
    
    for val in var_values:
        params[var_name] = val
        tprime = get_t(params['v0'], params['l'], params['c'], 
                       params['tprime0'], tpr)
        ft = get_f(params['v0'], params['l'], params['c'], tprime, 
                   params['f0'])
        axs[n].plot(tpr, ft, color=cm(norm(val)), linewidth=0.5)

plt.tight_layout()
plt.show()
