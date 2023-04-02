import obspy as op
import numpy as np
import os

# Importer will import all seismic data in SAC format from the datasets directory
# Each event recording from a station will be imported as an obspy stream
# Each stream will contain the three components of the seismogram as traces

# The importer will also import data about each station including its name, coordinates, and elevation
# The data will be stored in a dictionary with the station name as the key

# The importer will also generate common depth points for all the events
# based on the locations of the stations. These will be useful for CDP stacking

# First we will scan the datasets directory for all the events
# Each folder inside the datasets directory is an event
dataset_choice = 'ecuador_1stat'
eventnames = np.array([])
stations = np.array([])
for ev in os.listdir('../datasets' + '/' + dataset_choice):
    # Make a list of events
    eventnames = np.append(eventnames, ev)
    # identify the stations in each event
    # the names of the stations are at the beginning of each trace file name
    stations = np.append(stations, os.listdir('../datasets' + '/' + dataset_choice + '/' + ev)[0][0:7])
stations = np.unique(stations)

# Just for user quality of life, we make some dictionaries that
# allow us to identify what event and station each index corresponds to
sta_dict = {}
for st in stations:
    i = 0
    sta_dict[i] = st
    i += 1
ev_dict = {}
for ev in eventnames:
    i = 0
    ev_dict[i] = ev
    i += 1

# We'll make a data array with as many rows as there are stations
data = []
st_data = []

# Now we'll create the list of lists called data
# You can get each event recording stream by calling data[station_index][event_index]
for st in stations:
    for ev in eventnames:
        ev_stream = op.Stream()
        for comp in ['r', 't', 'z']:
            streamfiles = [f for f in os.listdir('../datasets' + '/' + dataset_choice + '/' + ev) if
                           f.startswith(st) and f.endswith('.' + comp)]
            ev_stream += op.read('../datasets' + '/' + dataset_choice + '/' + ev + '/' + streamfiles[0])
        st_data.append(ev_stream)
    data.append(st_data)

