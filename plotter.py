import argparse
import logging

import gpxpy
import gpxpy.gpx
import matplotlib.dates
import matplotlib.pyplot as plt
import tilemapbase
from celluloid import Camera
from tqdm import tqdm


def read_track(filename):
    logging.info("Reading coordinates from %s", filename)
    with open(filename, "r") as f:
        data = gpxpy.parse(f)
    track = data.tracks[0]
    return track


def animate(track, output_filename):
    bounds = track.get_bounds()

    tilemapbase.init(create=True)

    t = tilemapbase.tiles.build_OSM()

    extent = tilemapbase.Extent.from_lonlat(
        bounds.min_longitude,
        bounds.max_longitude,
        bounds.min_latitude,
        bounds.max_latitude,
    )

    points = track.segments[0].points

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(5, 5), dpi=100)
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

    logging.info("Creating animation")
    for point in tqdm(points):
        lat, lon = point.longitude, point.latitude
        x, y = tilemapbase.project(lat, lon)
        x_coords.append(x)
        y_coords.append(y)

        plotter.plot(ax1, t)
        ax1.plot(x_coords, y_coords, "b-", linewidth=2)
        ax1.scatter(x, y, marker="x", color="red", linewidth=3)

        time = matplotlib.dates.date2num(point.time)
        times.append(time)
        elevs.append(point.elevation)
        ax2.plot_date(times, elevs, fmt="b-")

        # plt.show()
        camera.snap()

    anim = camera.animate()

    logging.info("Saving to file %s", output_filename)
    anim.save(output_filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gpx_filename", help="File containing the GPX coordinates")
    parser.add_argument("output_filename", help="Filename of the movie output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    track = read_track(args.gpx_filename)
    animate(track, args.output_filename)


if __name__ == "__main__":
    main()
