# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---
from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
import math

# constants
P_0 = 0.58
P_W = 1.0
P_VEG = {'chaparral': 0.3, 'canyon': 0.8, 'forest': -0.6, 'lake': -1.0, 'town': 1.0}
V = 0.0   # What if wind 0?
C_1 = 0.045
C_2 = 0.131
WIND_DIR = 'N'  # wind direction
COS_VALS = {'NW': [1.0, 0.707107, 0, 0.707107, -0.707107, 0, -0.707107, -1.0],
            'N': [0.707107, 1.0, 0.707107, 0, 0, -0.707107, -1.0, -0.707107],
            'NE': [0, 0.707107, 1.0, -0.707107, 0.707107, -1.0, -0.707107, 0],
            'W': [0.707107, 0, -0.707107, 1.0, -1.0, 0.707107, 0, -0.707107],
            'E': [-0.707107, 0, 0.707107, -1.0, 1.0, -0.707107, 0, 0.707107],
            'SW': [0, -0.707107, -1.0, 0.707107, -0.707107, 1.0, 0.707107, 0],
            'S': [-0.707107, -1.0, -0.707107, 0, 0, 0.707107, 1.0, 0.707107],
            'SE': [-1.0, -0.707107, 0, -0.707107, 0.707107, 0, 0.707107, 1.0]
           }


def transition_func(grid, neighbourstates, neighbourcounts, fuel_grid):
    # not burning terrain types:
    # 0 - chaparral
    # 1 - canyon
    # 2 - forest
    # 3 - lake
    # 4 - town
    # other:
    # 5 - burning
    # 6 - completely burned

    # if a cell is burning (state 5), it will be completely burned down (state 6)
    # after number of steps equal to the amount of fuel for the cell.
    burning_cells = (grid == 5)
    fuel_grid[burning_cells] -= 1
    dead_cells = (fuel_grid == 0)

    # if at least one nearest-neighbour of a cell is burning (state 5) then catch fire with probability Pburn,
    # at_least_one_burning_neighbour = (neighbourcounts[5] > 0)

    # calculate wind effect
    # NW, N, NE, W, E, SW, S, SE = neighbourstates
    wind_prob_grid = np.zeros(grid.shape)
    for (direction, cos_a) in zip(neighbourstates, COS_VALS[WIND_DIR]):
        curr_direction_burning = (direction == 5)

        # update wind probability grid
        # P_W = exp[V(c1 + c2(cos(a) - 1))]
        # where a is angle between wind direction and current burning direction
        wind_prob_grid[curr_direction_burning] += math.exp(V*(C_1 + C_2*(cos_a - 1)))

    # set up grid with base burn probabilities for each cell
    ignite_prob_grid = setup_ignite_probabilities_grid(grid)

    # Note: if a cell doesn't have any burning neighbours, then
    # it will have value zero in wind_prob_grid, so it will also zero its
    # value in ignite_prob_grid after the multiplication below, so we don't
    # need at_least_one_burning_neighbour array (NOT SURE VERIFY IT!!!)
    # multiply base burn probabilities by summed P_W from each direction
    ignite_prob_grid *= wind_prob_grid

    random_grid = np.random.rand(*grid.shape)
    cells_to_ignite = random_grid < ignite_prob_grid

    to_burning_state = cells_to_ignite #& at_least_one_burning_neighbour

    grid[to_burning_state] = 5
    grid[dead_cells] = 6

    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Wildfire simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6)
    config.grid_dims = (40, 40)
    config.initial_grid = np.genfromtxt('grid.csv', delimiter=',')
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    colors = {
        "chapparal": (1.0, 0.8, 0),
        "canyon": (1.0, 0.5, 0.5),
        "forest": (0.0, 1.0, 0.0),
        "lake": (0.0, 0.0, 1.0),
        "town": (0.7, 0.3, 0.0),
        "burning": (1.0, 0.0, 0.0),
        "burned": (0.0, 0.0, 0.0)
    }

    config.state_colors = list(colors.values())
    config.wrap = False
    # config.num_generations = 1
    # config.grid_dims = (100, 100)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def setup_fuel_grid(grid):

    fuel_grid = np.zeros(grid.shape)
    chap = (grid == 0)
    fuel_grid[chap] = 28

    canyon = (grid == 1)
    fuel_grid[canyon] = 1

    forest = (grid == 2)
    fuel_grid[forest] = 120

    lake = (grid == 3)
    fuel_grid[lake] = -1

    town = (grid == 4)
    fuel_grid[town] = 5
    return fuel_grid


def setup_ignite_probabilities_grid(grid):

    ignite_grid = np.zeros(grid.shape)
    chap = (grid == 0)
    ignite_grid[chap] = P_0 * (1 + P_VEG['chaparral'])

    canyon = (grid == 1)
    ignite_grid[canyon] = P_0 * (1 + P_VEG['canyon'])

    forest = (grid == 2)
    ignite_grid[forest] = P_0 * (1 + P_VEG['forest'])

    lake = (grid == 3)
    ignite_grid[lake] = P_0 * (1 + P_VEG['lake'])

    town = (grid == 4)
    ignite_grid[town] = P_0 * (1 + P_VEG['town'])
    return ignite_grid


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create fuel numpy array
    fuel_grid = setup_fuel_grid(config.initial_grid)

    # Set initial burning cell
    config.initial_grid[0][0] = 5

    # Create ignite probabilities array
    #ignite_prob_grid = setup_ignite_probabilities_grid(config.initial_grid)

    # Create grid object
    grid = Grid2D(config, (transition_func, fuel_grid))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
