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
# constants
P_0 = 0.58
P_W = 1.0
P_VEG = {'chaparral': 0.5, 'canyon': 1, 'forest': 0.2, 'lake': 0}
WIND_DIR = np.array([1,0])

def transition_func(grid, neighbourstates, neighbourcounts, fuel_grid, coeffs):
    # print(neighbourstates.shape)


    # TODO:
    # - include burning time of each terrain type in the model
    # - increase p_burn probability depending on the number of burning neighbours
    # - implement wind effect
    # - refactor the code (for loop to calculate p_burn? separate function?)
    # - pre define state colors, grid size, grid state in the setup function

    # not burning terrain types:
    # 0 - chaparral
    # 1 - canyon
    # 2 - forest
    # 3 - lake
    # 4 - town
    # other:
    # 5 - burning
    # 6 - dead

    # if a cell is burning (state 4), it will be completely burned down (state 5) in the next timestep
    burning_cells = (grid == 5)
    fuel_grid[burning_cells] -= 1

    #reshape from 8,40,40
    neighbours = np.reshape(neighbourstates,(40,40,8), order='A')

    ignite_grid = np.zeros((40,40))
    for y in range(40):
        for x in range(40):
            all_neighbours = neighbours[y][x]
            burning_neighbours = all_neighbours == 5
            p_0 = 0.1
            ignite_grid[y][x] = np.sum(burning_neighbours*coeffs*p_0)

    print(ignite_grid)
    # input("Press enter:")

    # if at least one nearest-neighbour of a cell is burning (state 4) then catch fire with probability Pburn,
    at_least_one_burning_neighbour = (neighbourcounts[5] > 0)

    # p_burn_chap = P_0 * (1 + P_VEG['chaparral']) * P_W
    # p_burn_canyon = P_0 * (1 + P_VEG['canyon']) * P_W
    # p_burn_forest = P_0 * (1 + P_VEG['forest']) * P_W
    # p_burn_lake = P_0 * (1 + P_VEG['lake']) * P_W

    # probability_arr_chap = np.random.rand(*grid.shape) < p_burn_chap
    # probability_arr_can = np.random.rand(*grid.shape) < p_burn_canyon
    # probability_arr_for = np.random.rand(*grid.shape) < p_burn_forest
    # probability_arr_lake = np.random.rand(*grid.shape) < p_burn_lake

    chaparral_cells = (grid == 0)
    canyon_cells = (grid == 1)
    forest_cells = (grid == 2)
    lake_cells = (grid == 3)

    ignite_grid[chaparral_cells] *= P_VEG['chaparral']
    ignite_grid[canyon_cells] *= P_VEG['canyon']
    ignite_grid[forest_cells] *= P_VEG['forest']
    ignite_grid[lake_cells] *= P_VEG['lake']

    random_grid = np.random.rand(*grid.shape)

    cells_to_ignite = random_grid < ignite_grid
    grid[cells_to_ignite] = 5

    # to_burning_state_chap = chaparral_cells & at_least_one_burning_neighbour & probability_arr_chap
    # to_burning_state_can = canyon_cells & at_least_one_burning_neighbour & probability_arr_can
    # to_burning_state_for = forest_cells & at_least_one_burning_neighbour & probability_arr_for
    # to_burning_state_lake = lake_cells & at_least_one_burning_neighbour & probability_arr_lake

    # grid[to_burning_state_chap] = 5
    # grid[to_burning_state_can] = 5
    # grid[to_burning_state_for] = 5
    # grid[to_burning_state_lake] = 5



    dead_cells = fuel_grid == 0
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
        "chapparal" : (1.0, 0.8, 0),
        "canyon" : (1.0, 0.5, 0.5),
        "forest" : (0.0, 1.0, 0.0),
        "lake" : (0.0, 0.0, 1.0),
        "town" : (0.7, 0.3, 0.0),
        "burning" : (1.0, 0.0, 0.0),
        "burned" : (0.0, 0.0, 0.0)
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
    chap = grid==0
    fuel_grid[chap] = 28

    canyon = grid==1
    fuel_grid[canyon] = 1

    forest = grid==2
    fuel_grid[forest] = 120

    lake = grid == 3
    fuel_grid[lake]= -1

    town = grid == 4
    fuel_grid[town]= -1
    return fuel_grid

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

def main():
    # Open the config object
    config = setup(sys.argv[1:])

    fuel_grid = setup_fuel_grid(config.initial_grid)

    config.initial_grid[0][0] = 5
    np.set_printoptions(threshold=sys.maxsize)


    wind = [1,0] #north wind
    dirs = np.array([[ 1, -1],[ 1,  0],[ 1,  1],[ 0, -1],[ 0,  1],[-1, -1],[-1,  0],[-1,  1]])
    normdirs = []
    for vec in dirs:
        normdirs.append(normalize(vec))

    coeffs = np.dot(normdirs,wind)+1
    print(coeffs)
    # Create grid object
    grid = Grid2D(config, (transition_func, fuel_grid,coeffs))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
