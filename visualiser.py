import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np
import traceback

DATA_DIR = "data"
grid = np.array([])
loaded_steps = 0
variable_max = 1


#norm = BoundaryNorm(
#    boundaries = np.arange(cmap.N + 1) - 0.5, # dynamically generated boundaries
#    ncolors=cmap.N,
#    clip=True
#)

def unpack(v):
    # Function is required to convert agent variable steps from array to scalars due to bug in RC3
    # I.e. [123] to 123
    return v[0] if isinstance(v, list) else v


def load_data(step_count, agent_name='agent', agent_variable='status', agent_variable_max=1):
    """Function loads FLAME GPU simulation output data (in json format) and stores it in the global grid array"""
    global grid
    global loaded_steps
    global variable_max

    variable_max = agent_variable_max
    try:
        for i in range(step_count+1):
            file_path = f"{DATA_DIR}/{i}.json"
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            agents = data.get("agents", {}).get(agent_name, {}).get("default", [])

            if not agents:
                print(f"No agent data found. step={i}")
                return

            # Determine grid size
            max_x = unpack(max(agent.get('x', 0) for agent in agents))
            max_y = unpack(max(agent.get('y', 0) for agent in agents))

            if not grid.any():
                grid = np.zeros((int(max_x) + 1, int(max_y) + 1, int(step_count)+1))

            for agent in agents:
                x, y = unpack(agent.get('x', 0)), unpack(agent.get('y', 0))
                status = unpack(agent.get(agent_variable, 0))

                if status != 0:
                    grid[int(x), int(y), i] = status  # Mark active agents with their status
        loaded_steps = step_count
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        print(traceback.format_exc())


def plot_step(step):
    """
    Plots a single agent step as a matplotlib plot.
    If the data is not loaded then it will be loaded first.
    """

    # if grid is empty force reload of data
    #if not grid.any() or loaded_steps < step:
    #    load_data(step)

    # Plotting
    plt.figure(figsize=(8, 6))
    cmap = plt.get_cmap('viridis')
    im = plt.imshow(grid[:,:,step].T, origin='lower', cmap=cmap, vmax=variable_max)

    #plot
    plt.title(f"")
    # plt.colorbar(im)
    plt.show()


def animate_steps(step_count):
    """
    Plots the simulation outputs as a looping animation.
    If the data is not loaded then it will be loaded first.
    """
    global ani

    # if grid is empty force reload of data
    #if not grid.any():
    #    load_data(step_count)

    fig, ax = plt.subplots()
    cmap = plt.get_cmap('viridis')

    ims = [] # ims is a list of lists, each row is a list of artists to draw in the
    for i in range(step_count):
        im = ax.imshow(grid[:,:,i].T, animated=True, cmap=cmap, vmax=variable_max, origin='lower')
        if i == 0:
            ax.imshow(grid[:,:,i].T, animated=True, cmap=cmap, vmax=variable_max, origin='lower')  # show an initial one first
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

    # Plotting
    # plt.colorbar(im, ax=ax)
    plt.show()



def display_steps(step_count):
    """
    Plots the simulation outputs as an interactive plot with a slider controlling the step number.
    If the data is not loaded then it will be loaded first.
    """
    global im
    global slider
    im = slider = None

    # if grid is empty force reload of data
    #if not grid.any():
    #    load_data(step_count)

    fig, ax = plt.subplots()
    cmap = plt.get_cmap('viridis')
    im = ax.imshow(grid[:,:,0].T, cmap=cmap, vmax=variable_max, origin='lower')
    ax_depth = plt.axes([0.23, 0.02, 0.56, 0.04])
    slider = Slider(ax_depth, 'step', 0, grid.shape[2]-1, valinit=0)
    update_slider = lambda v: im.set_data(grid[:, :, int(round(v))].T)
    slider.on_changed(update_slider)

    # Plotting
    # plt.colorbar(im, ax=ax)
    plt.show()