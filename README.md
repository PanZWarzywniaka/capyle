## Simulating Wild fires in CAPyLE

Added new cellular automata description `wildfire_2d.py` that simulates spread of wild fire.

<div display="flex" flex-direction="row" >
<img src="https://user-images.githubusercontent.com/38562250/213926036-304e2eed-466c-458a-91dd-854516da1c14.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/38562250/213926267-316b8127-7599-4080-a4b9-7477bae909ba.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/38562250/213926272-22c108da-c060-4a0c-9d26-f246c68ae311.png" width="300" height="300"/>
</div>

Fire spreading on a 2D grid

Our model defines terrain types with diffrent propabilities of catching a fire and diffrent the burn time.

- Dense forest (green colour), difficult to ignite but can burn for up to one month, 
- Chaparral (yellow colour), catches fire quite easily, can burn for a period of several days.
- Canyon (pink-ish colour), very easy to catch fire, but burns for only several hours
- Lake (blue colour), can't be ignited


Our model takes into acount wind direction and velocity affecting spread of fire.

Once the fire reaches the town, simulaton reports results in `results/` directory: 
- `.json` file with simulation parameters
- grid state when fire reached the town

Our model can be used to simulate firebrigade interventions. To simulate water drops specify time of intervention and bouding box coorinates in `wildfire_2d.py`. For example:

![wild_fire_water_drop](https://user-images.githubusercontent.com/38562250/213927046-4d687bd9-9a4a-4b3d-9906-b34a63a63afb.png)

Initial grid is defined by `grid.csv`.

# CAPyLE
CAPyLE is a cross-platform teaching tool designed and built as part of a final year computer science project. It aims to aid the teaching of cellular automata and how they can be used to model natural systems.

It is written completely in python with minimal dependencies.

![CAPyLE Screenshot on macOS](http://pjworsley.github.io/capyle/sample.png)

## Installation
The installation guide can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/installationguide.html)

## Usage
Detailed usage can be found on the [CAPyLE webpages](http://pjworsley.github.io/capyle/).

See below for a quickstart guide:

1. `git clone https://github.com/pjworsley/capyle.git [target-directory]`
2. `cd [target-directory]`
3. Execute main.py either by:
    * `run.bat` / `run.sh`
    * `python main.py`
2. Use the menu bar to select File -> Open. This will open in the folder `./ca_descriptions`.
3. Open one of the example files;
  - `wolframs_1d.py` is Wolfram's elementary 1D automata
  - `gol_2d.py` is Conway's 2D game of life
4. The main GUI elements will now load, feel free to customise the CA parameters on the left hand panel
5. Run the CA with your parameters by clicking the bottom left button 'Apply configuration & run CA'
6. The progress bar will appear as the CA is run
7. After the CA has been run, use the playback controls at the top and the slider at the bottom to run through the simulation.
8. You may save an image of the currently displayed output using the 'Take screenshot' button

## Acknowledgements
Special thanks to [Dr Dawn Walker](http://staffwww.dcs.shef.ac.uk/people/D.Walker/) for proposing and supervising this project.

Also thanks to the COM2005 2016/2017 cohort for being the guinea-pigs!

## Licence
CAPyLE is licensed under a BSD licence, the terms of which can be found in the LICENCE file.

Copyright 2017 Peter Worsley
