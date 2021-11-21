!/usr/bin/env python

import sys
import gpxpy
import gpxpy.gpx

import matplotlib.pyplot as plt

gpx_file = open(sys.argv[1], 'r')

gpx = gpxpy.parse(gpx_file)

speeds = []
heights = []

for track in gpx.tracks:
    for segment in track.segments:
        for point_idx, point in enumerate(segment.points):
            heights.append(point.elevation * 3.28084) # m -> ft
            if point.speed:
                speed = point.speed
            elif segment.get_speed(point_idx):
                speed = segment.get_speed(point_idx)
            else:
                speed = 0
            speeds.append(speed * 1.94384 + float(sys.argv[2])) # m/s -> kt

fraction = 10
length = len(speeds)

start = length/fraction
end = length-length/fraction

d_speeds = speeds[:start]
d_heights = heights[:start]
d_heights = [x-d_heights[0] for x in d_heights]
a_speeds = speeds[end:]
a_heights = heights[end:]
a_heights = [x-a_heights[-1] for x in a_heights]

avoid_lower_speeds = [50, 60, 80, 100]
avoid_lower_heights = [0, 20, 25, 30]

avoid_higher_speeds = [0, 25, 40, 45, 50, 53, 53, 0]
avoid_higher_heights = [10, 10, 25, 40, 70, 100, 200, 400]

plt.plot(d_speeds, d_heights, 'g^',
         a_speeds, a_heights, 'bs',
         )

plt.fill_between(avoid_lower_speeds, avoid_lower_heights)
plt.fill_between(avoid_higher_speeds, avoid_higher_heights)

plt.axis((0, 100, 0, 750))

plt.show()

