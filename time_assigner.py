#!/usr/bin/env python3

from itertools import chain
from typing import Generator, Iterable, Iterator
from copy import deepcopy

import gpx

from pathlib import Path


def chunk_waypoints(
    all_points: Iterator[gpx.Waypoint],
) -> Generator[list[gpx.Waypoint], None, None]:

    chunk = [next(all_points)]
    for waypoint in all_points:
        chunk.append(waypoint)
        if waypoint.time:
            yield chunk
            # Reset chunk using the final item from previous as first item of new
            chunk = [waypoint]


for f in Path.cwd().glob("*_matched.gpx"):
    data = gpx.GPX.from_file(f)
    for track in data.tracks:
        all_points = chain.from_iterable(track.segments)

        for chunk in chunk_waypoints(all_points):
            og_chunk = deepcopy(chunk)
            total_interval = chunk[-1].time - chunk[0].time
            interpolated_interval = total_interval / len(chunk)
            last_time = chunk[0].time
            for waypoint in (element for element in chunk if not element.time):
                last_time += interpolated_interval
                waypoint.time = last_time

    data.routes = []

    data.to_file(f.with_stem(f"{f.stem}_interpolated"))
