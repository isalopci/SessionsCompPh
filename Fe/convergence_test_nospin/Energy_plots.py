import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os # Import os for path handling

# --- Configuration ---
DATA_FILE = 'Energy_ecut.dat'
DELIMITER = ' ' 

# --- Data Loading Function ---
def load_and_preprocess_data(file_path, sep):
    """Loads data, assigns columns, and calculates total energy."""
    try:
        # Load the data file, setting 'header=None' and using the specified separator
        df = pd.read_csv(file_path, sep=sep, comment='#', header=None, skipinitialspace=True)
        
        # Explicitly rename columns: 0=kpoints, 1=meshcutoff, 2=energy
        df.rename(columns={0: 'kpoints', 1: 'cutoff', 2: 'energy'}, inplace=True)
        
        # Use Total Energy as the base (in eV)
        df['total_energy'] = df['energy']
        
        return df
        
    except FileNotFoundError:
        print(f"Error: Data file not found at '{file_path}'. Please check the path.")
        return None
    except Exception as e:
        print(f"Error reading the file or processing columns: {e}")
        print("Ensure your file has three columns separated by a space and contains only data rows or comment rows starting with '#'.")
        return None

# --- Plotting Function ---
def plot_convergence(df, x_column, title_prefix):
    """
    Plots the relative total energy (Delta E) vs a single variable (kpoints or cutoff)
    and saves the result as an SVG file.
    """
    if df.empty:
        print(f"No data to plot for {title_prefix}.")
        return

    # Sort the data by the variable being tested
    df = df.sort_values(by=x_column).reset_index(drop=True)
    
    # Calculate the energy difference relative to the last (most converged) point
    last_energy = df['total_energy'].iloc[-1]
    # Convert to meV by multiplying by 1000
    df['Energy_Delta_meV'] = (df['total_energy'] - last_energy) * 1000 
    
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot the relative energy
    ax.plot(df[x_column], df['Energy_Delta_meV'], marker='o', linestyle='-', color='tab:blue')
    
    # Add a convergence tolerance line (standard is +/- 1 meV)
    ax.axhline(y=1.0, color='r', linestyle='--', linewidth=1, label=r'$\pm 1 \text{ meV}$ Tolerance')
    ax.axhline(y=-1.0, color='r', linestyle='--', linewidth=1)
    ax.axhline(y=0.0, color='k', linestyle='-', linewidth=0.5)

    # --- Find Convergence Point ---
    converged_df = df[df['Energy_Delta_meV'].abs() <= 1.0]
    
    if not converged_df.empty:
        converged_value = converged_df[x_column].iloc[0]
        ax.axvline(x=converged_value, color='k', linestyle=':', linewidth=1.5, label=f'Converged at: {converged_value}')
        print(f"\n--- {title_prefix} Converged ---")
        print(f"Converged value (within 1 meV): {converged_value}")
    else:
        print(f"\nWarning: Convergence (1 meV) not reached in the tested range for {title_prefix}.")
        
    # --- Labels and Title ---
    if x_column == 'kpoints':
        x_label = r'k-point Grid Index ($i$)'
        fixed_val = df['cutoff'].iloc[0]
        title = f'{title_prefix} Convergence Test (Fixed MeshCutoff: {fixed_val} Ry)'
        filename = f'convergence_kpoint_{fixed_val}Ry.svg'
    else: # x_column == 'cutoff'
        x_label = 'MeshCutoff (Ry)'
        fixed_val = df['kpoints'].iloc[0]
        title = f'{title_prefix} Convergence Test (Fixed k-point grid: {fixed_val}x{fixed_val}x{fixed_val})'
        filename = f'convergence_cutoff_{fixed_val}k.svg'
    
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(r'Relative Total Energy $\Delta E$ (meV)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()

    # --- SAVE AS SVG ---
    plt.savefig(filename, format='svg')
    print(f"\nSuccessfully saved plot as {filename}")
    
    # Show the plot window interactively
    plt.show() 

# --- Main Execution ---
if __name__ == "__main__":
    df_raw = load_and_preprocess_data(DATA_FILE, DELIMITER)
    
    if df_raw is not None and not df_raw.empty:
        # 1. Determine the highest tested k-point and MeshCutoff
        max_kpoints = df_raw['kpoints'].max()
        max_cutoff = df_raw['cutoff'].max()
        
        # 2. Filter for K-point Convergence Plot (Fix cutoff at max_cutoff)
        df_kpoint = df_raw[df_raw['cutoff'] == max_cutoff].copy()
        
        # 3. Filter for MeshCutoff Convergence Plot (Fix k-point at max_kpoints)
        df_cutoff = df_raw[df_raw['kpoints'] == max_kpoints].copy()

        # 4. Generate Plots (K-point vs. Energy)
        if not df_kpoint.empty and df_kpoint['kpoints'].nunique() > 1:
            plot_convergence(df_kpoint, 'kpoints', 'k-point')
        else:
            print(f"\nSkipping k-point plot: Not enough unique k-point values at the highest MeshCutoff ({max_cutoff} Ry).")

        # 5. Generate Plots (MeshCutoff vs. Energy)
        if not df_cutoff.empty and df_cutoff['cutoff'].nunique() > 1:
            plot_convergence(df_cutoff, 'cutoff', 'MeshCutoff')
        else:
            print(f"\nSkipping MeshCutoff plot: Not enough unique cutoff values at the highest k-point ({max_kpoints}).")
    elif df_raw is not None:
         print("The loaded DataFrame is empty.")