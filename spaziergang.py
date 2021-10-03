#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gpxpy
import gpxpy.gpx
import matplotlib.dates
import matplotlib.pyplot as plt
import pandas as pd
import tilemapbase
from celluloid import Camera
from IPython.display import HTML


# In[2]:


with open("2020-11-29-12-11-00.gpx", "r") as f:
    data = gpxpy.parse(f)


# In[3]:


track = data.tracks[0]


# In[4]:


bounds = track.get_bounds()


# In[5]:


tilemapbase.init(create=True)


# In[6]:


t = tilemapbase.tiles.build_OSM()


# In[7]:


extent = tilemapbase.Extent.from_lonlat(
    bounds.min_longitude,
    bounds.max_longitude,
    bounds.min_latitude,
    bounds.max_latitude,
)


# In[8]:


points = track.segments[0].points


# In[11]:


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 8), dpi=100)
camera = Camera(fig)
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)
ax2.set_ylim(
    min(point.elevation for point in points),
    max(point.elevation for point in points),
)

times = []
elevs = []
x_coords = []
y_coords = []

plotter = tilemapbase.Plotter(extent, t, width=600)


for point in points:
    lat, lon = point.longitude, point.latitude
    x, y = tilemapbase.project(lat, lon)
    x_coords.append(x)
    y_coords.append(y)

    plotter.plot(ax1, t)
    ax1.plot(x_coords, y_coords, "b-", linewidth=3)
    ax1.scatter(x, y, marker="x", color="red", linewidth=3)

    time = matplotlib.dates.date2num(point.time)
    times.append(time)
    elevs.append(point.elevation)
    ax2.plot_date(times, elevs, fmt="b-")

    plt.show()
    camera.snap()


# In[12]:


anim = camera.animate()


# In[13]:


anim.save("hike.mp4")


# In[ ]:





# In[ ]:




