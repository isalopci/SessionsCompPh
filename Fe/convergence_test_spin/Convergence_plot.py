import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Configuration ---
# 1. Specify the name of your data file
DATA_FILE = 'Energy_ecut.dat' # Changed to .dat

# 2. Specify the delimiter (separator) used in your file:
DELIMITER = ' ' # Set for space-separated columns

# --- Data Loading and Plotting ---

def plot_3d_convergence(file_path, sep):
    """
    Loads data from a file, structures it for a 3D plot, and generates the plot.
    """
    try:
        # Load the data file, treating spaces as the separator and ignoring comment lines
        df = pd.read_csv(file_path, sep=sep, comment='#', header=None, skipinitialspace=True)
        
        # Ensure column names are standardized
        # Assumes the first three columns are kpoints, meshcutoff, energy
        # The comment='#' line should handle the header if it starts with #
        df.rename(columns={0: 'kpoints', 1: 'cutoff', 2: 'energy'}, inplace=True)
        
        # Use Total Energy as requested
        df['total_energy'] = df['energy']
        
    except FileNotFoundError:
        print(f"Error: Data file not found at '{file_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"Error reading the file or processing columns: {e}")
        print("Ensure your file has three columns named/ordered: kpoints, meshcutoff, energy.")
        return

    # --- Data Structuring for Surface Plot ---
    
    # Pivot the DataFrame to get a grid for the 3D surface plot
    data_pivot = df.pivot(index='kpoints', columns='cutoff', values='total_energy')
    
    # Get the X, Y, Z arrays for the plot
    X = data_pivot.columns.values  # MeshCutoff (Ry)
    Y = data_pivot.index.values    # k-points (i)
    Z = data_pivot.values          # Total Energy (eV)
    
    # Create a mesh grid from the X and Y arrays
    X_grid, Y_grid = np.meshgrid(X, Y)

    # --- Plotting ---
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the surface
    surf = ax.plot_surface(X_grid, Y_grid, Z, 
                           cmap='viridis', 
                           edgecolor='none',
                           rstride=1, cstride=1)
    
    # --- Labeling and Customization ---
    
    ax.set_xlabel('MeshCutoff (Ry)', fontsize=12, labelpad=15)
    ax.set_ylabel('k-point Grid Index ($i$)', fontsize=12, labelpad=15)
    ax.set_zlabel('Total Energy (eV)', fontsize=12, labelpad=15) 
    
    ax.set_title('3D Convergence Surface: BCC Fe Total Energy', fontsize=16)
    
    # Add a color bar
    fig.colorbar(surf, shrink=0.5, aspect=5, label='Total Energy (eV)')
    
    # Set the view angle for better visualization
    ax.view_init(elev=20, azim=-120) 
    
    plt.tight_layout()
    plt.show()
    
    print("\n--- Data Summary ---")
    print(f"Minimum Total Energy Found: {df['total_energy'].min():.4f} eV")
    print(f"Maximum Total Energy Found: {df['total_energy'].max():.4f} eV")
    
# --- Main Execution ---
if __name__ == "__main__":
    plot_3d_convergence(DATA_FILE, DELIMITER)