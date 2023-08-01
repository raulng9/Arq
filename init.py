from flask import Flask
import csv
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from pyproj import Transformer

app = Flask(__name__)


DEFAULT_MAP_COORDS = [43.533, -6.583]


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map()
    #Coordinates in CSV are in ETRS89 - UTM zone 30N, we need to convert them to standard GPS ones (4326)
    transformer = Transformer.from_crs("25830", "EPSG:4326")

    with open('places.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        arch_map = folium.Map(location = DEFAULT_MAP_COORDS, zoom_start = 13)
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                row[1] = row[1].replace(',','.')
                row[2] = row[2].replace(',','.')
                if line_count == 1:
                    initial_coord = list(transformer.transform(row[1], row[2]))
                folium.Marker(list(transformer.transform(row[1], row[2])), popup = row[0]).add_to(arch_map)
                line_count += 1
        print(f'processed {line_count} items')

    #Display the map
    return arch_map.get_root().render()




if __name__ == "__main__":
    app.run(debug=True)