import pandas as pd
import os
import json

# read in population data
df = pd.read_csv('/home/kinew/doggomap/dogs.csv')

df['EstimatedDogPopulation'] = df['EstimatedDogPopulation'].map(lambda x: x.replace(',',''))
df.astype({'EstimatedDogPopulation': float})
df['EstimatedDogPopulation'] = pd.to_numeric(df['EstimatedDogPopulation'], errors='coerce')
import folium
from branca.utilities import split_six
import shapefile
# read the shapefile
reader = shapefile.Reader("/home/kinew/doggomap/Districts.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
     geometry=geom, properties=atr)) 

# write the GeoJSON file
from json import dumps
geojson = open("/home/kinew/doggomap/postcode_geo.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
 "features": buffer}, indent=2) + "\n")
geojson.close()

postcode_geo = '/home/kinew/doggomap/postcode_geo.json'

m = folium.Map(location=[55, 4], zoom_start=5)
m.choropleth(
        geo_data=postcode_geo,
        data=df,
        columns=['PostcodeDistrict','EstimatedDogPopulation'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Estimated number of Dogs',
        highlight=True
    )

m

delay = 5
fn='/home/kinew/doggomap/doggomap.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
m.save(fn)
