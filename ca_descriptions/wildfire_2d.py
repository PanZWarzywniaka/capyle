# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
import random
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
P_VEG = {'chaparral': 0.2, 'canyon': 0.4, 'forest': -0.3, 'lake': -1.0}

p_burn_chap = P_0 * (1 + P_VEG['chaparral']) * P_W
p_burn_canyon = P_0 * (1 + P_VEG['canyon']) * P_W
p_burn_forest = P_0 * (1 + P_VEG['forest']) * P_W
p_burn_lake = P_0 * (1 + P_VEG['lake']) * P_W

#This function does not currently account for fuel and burn time
def transition_func(grid, neighbourstates, neighbourcounts):
    burning_cells = (grid == 5)
    nw, n, ne, w, e, sw, s, se = neighbourstates

    nw_wind_prob = np.cos(np.deg2rad(45))
    ne_wind_prob = np.cos(np.deg2rad(45))
    w_wind_prob = np.cos(np.deg2rad(90))
    e_wind_prob = np.cos(np.deg2rad(90))
    sw_wind_prob = np.cos(np.deg2rad(135))
    se_wind_prob = np.cos(np.deg2rad(135))
    s_wind_prob = -1
    n_wind_prob = 1

    chaparral_cells = (grid == 0)
    canyon_cells = (grid == 1)
    forest_cells = (grid == 2)

    #2d arrays of probability with wind accounted for, some randomness implemented
    nw_burn_prob = (nw == 5) * (np.random.rand(*grid.shape) * (nw_wind_prob + 1))
    n_burn_prob = (n == 5) * (np.random.rand(*grid.shape) * (n_wind_prob + 1))
    ne_burn_prob = (ne == 5) * (np.random.rand(*grid.shape) * (ne_wind_prob + 1))
    w_burn_prob = (w == 5) * (np.random.rand(*grid.shape) * (w_wind_prob + 1))
    e_burn_prob = (e == 5) * (np.random.rand(*grid.shape) * (e_wind_prob + 1))
    sw_burn_prob = (sw == 5) * (np.random.rand(*grid.shape) * (sw_wind_prob + 1))
    s_burn_prob = (s == 5) * (np.random.rand(*grid.shape) * (s_wind_prob + 1))
    se_burn_prob = (se == 5) * (np.random.rand(*grid.shape) * (se_wind_prob + 1))

    burn_probs = (nw_burn_prob, n_burn_prob, ne_burn_prob, w_burn_prob, 
        e_burn_prob, sw_burn_prob, s_burn_prob, se_burn_prob)
    
    grid[get_to_burning_state(grid, burn_probs, forest_cells, p_burn_forest)] = 5
    grid[get_to_burning_state(grid, burn_probs, chaparral_cells, p_burn_chap)] = 5
    grid[get_to_burning_state(grid, burn_probs, canyon_cells, p_burn_canyon)] = 5
    grid[burning_cells] = 6

    return grid

def get_to_burning_state(grid, burn_probs, terr_cells, terr_p_burn):
    (nw_burn_prob, n_burn_prob, ne_burn_prob, w_burn_prob, e_burn_prob, 
        sw_burn_prob, s_burn_prob, se_burn_prob) = burn_probs
    nw_terr_burn_prob = nw_burn_prob * terr_p_burn
    n_terr_burn_prob = n_burn_prob * terr_p_burn
    ne_terr_burn_prob = ne_burn_prob * terr_p_burn
    w_terr_burn_prob = w_burn_prob * terr_p_burn
    e_terr_burn_prob = e_burn_prob * terr_p_burn
    sw_terr_burn_prob = sw_burn_prob * terr_p_burn
    s_terr_burn_prob = s_burn_prob * terr_p_burn
    se_terr_burn_prob = se_burn_prob * terr_p_burn

    sum_terr_burn_prob = nw_terr_burn_prob + n_terr_burn_prob + ne_terr_burn_prob
    sum_terr_burn_prob = sum_terr_burn_prob + w_terr_burn_prob + e_terr_burn_prob + sw_terr_burn_prob
    sum_terr_burn_prob = sum_terr_burn_prob + s_terr_burn_prob + se_terr_burn_prob

    probability_arr_tf = np.random.rand(*grid.shape) < sum_terr_burn_prob

    return probability_arr_tf & terr_cells



def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Wildfire simulation"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6)
    config.grid_dims = (40, 40)
    # ------------------------------------------------------------------------


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
    # config.num_generations = 150
    # config.grid_dims = (100, 100)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
