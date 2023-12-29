# Ecoroutes

![Ecoroutes](/GUI/static/assets/images/eco_icon.jpg)

## Table of Contents

* [Ecoroutes](#ecoroutes)
* [Getting Started](#getting-started)
    * [Requirements](#requirements)
    * [Installation](#installation)
        * [Installing using Pip](#installing-using-pip)
        * [Installing using Conda](#installing-using-conda)
* [Running the Application](#running-the-application)
* [Contributors](#contributors)
* [Credits](#credits)


## Ecoroutes

**EcoRoutes**  is a comprehensive routing application tailored for Singapore's transport system. Providing users with **real-time, eco-friendly travel options**, EcoRoutes aims to usher in a more sustainable transport culture. We firmly believe that EcoRoutes stands as a significant stride towards a greener future, enabling individuals to understand and minimize the environmental impact of their travel choices. 


## Getting Started

### Requirements
* Hardware Requirements
    * Modern Operating System:
        * Windows 7 or 10 or above.
        * Mac OS X 10.11 or higher, 64-bit or above.
        * Linux: RHEL 6/7, 64-bit (almost all libraries also work in Ubuntu) or above
    * x86 64-bit CPU (Intel / AMD architecture) or above.
    * 4 GB RAM or above.
    * 5 GB free disk space or above.
*  Software Requirements
    * [Python 3.6](https://www.python.org/downloads/) or above.

        After installation run the following command to upgrade pip: 

          python -m pip install --upgrade pip

    * Any web browser, preferbly [Google Chrome](https://www.google.com/chrome/).

    * Any Python IDE, preferbly [Visual Studio Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/).

### Installation

#### Installing using Pip
Dependencies required :
* [Osmnx](https://osmnx.readthedocs.io/en/stable/) - Python for street networks.
          
      pip install osmnx

    **Note : If you are having trouble installing osmnx using this method, install it via [conda](#installing-using-conda).**

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python web framework.

      pip install flask

* [Matplotlib](https://matplotlib.org/) - Python plotting library.

      pip install matplotlib

* [Networkx](https://networkx.github.io/) - Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

      pip install networkx

* [Pandas](https://pandas.pydata.org/) - Python data analysis library.

      pip install pandas

* [Geopy](https://geopy.readthedocs.io/en/stable/) - Python client for several popular geocoding web services.

      pip install geopy

* [Folium](https://python-visualization.github.io/folium/) - Python data, leaflet.js maps.

      pip install folium

* [Scikit-learn](https://scikit-learn.org/stable/) - Python machine learning library.

      pip install scikit-learn


#### Installing using Conda

1. Download and install [Anaconda](https://www.anaconda.com/distribution/).
2. Launch VSCode or PyCharm.
3. Import the project folder.
4. Install osmnx at terminal

    * To do that run the following command in terminal :

          conda install -c conda-forge osmnx
    
    * Refer to [osmnx](https://anaconda.org/conda-forge/osmnx) if above command fails.

5. Install the [other](#installing-using-pip) dependencies.


## Running the Application

### How to run the application

    Run the python file "app.py"
You will receive a local url which you can click on it to open the application in your prefered web browser.

![GUI](/GUI/static/assets/images/GUI.png)

Enter your **Starting Location** and **Destination** in the respective fields.

Choose your mode of transport from the dropdown menu.
-  If you choose **Car**, you may proceed to click on the  `Let's Go!` button to view the route.


- If you choose **Public Transport**, you have to choose your preference in the drop down box below. You may then proceed to click on the  `Let's Go!` button to view the route.


**Do take note that the application will take a few seconds to load the route.**

## Contributors

## CEO: [Munir](https://open.spotify.com/track/37xuoeOvBLK6zV9wkgRttR?si=58e287e51473457a)
### CTO: JJ  
#### Head Software Engineers: Travis & Shaoyu  
##### Janitor: Alan  
