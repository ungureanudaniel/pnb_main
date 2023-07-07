from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
#import pandas and geopandas
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
#coordinates transformer
from pyproj import Transformer
#folium
import folium
from folium import plugins
from folium.features import DivIcon
from django.contrib import messages
#gee
import ee

ee.Initialize()


def map_view(request):
    template_name = 'geemap/map.html'
    #import geojson file for natura2000 site ROSCI0013
    park_limits = None
    try:
        #get the coordinates from geojson
        gdf_park = gpd.read_file('static\gis\pnb_3844_poly.geojson')
        gdf_n2ksite = gpd.read_file('static\gis\ROSCI_0013_3844_poly.geojson')
        gdf_ro = gpd.read_file(r'static\gis\RO_limits_3844_poly.geojson')
        gdf_uat = gpd.read_file(r'static\gis\UAT_limits_3844_poly.geojson')
        #convert coordinates to epsg4326 to work with folium which is 4326 by default
        gdf_park=gdf_park.to_crs("EPSG:4326")
        gdf_n2ksite=gdf_n2ksite.to_crs("EPSG:4326")
        gdf_ro=gdf_ro.to_crs("EPSG:4326")
        gdf_uat=gdf_uat.to_crs("EPSG:4326")

        messages.success(request, f"Această hartă este interactivă. Vă rugăm să îi încercați funcționalitățile. De exemplu, pictograma din dreapta cu straturi vă permite afișarea/ascunderea anumitor straturi. De asemenea, vom continua să adăugăm informații, așa că stați aproape!")
    except Exception as e:
         messages.error(request, f"Error!Error! Sorry for the inconvenience:{e}")
    #creation of map 
    try:
        m = folium.Map([45.38, 25.444], zoom_start=10, tiles ='Stamen Terrain', control_scale = True)
    except Exception as e:
        messages.error(request, f"Error! Sorry for the inconvenience:{e}")
    try:
        #add layers styles
        style1 = {'fillColor': 'transparent', 'color': '#FF8C00'}
        style2 = {'fillColor': 'transparent', 'color': '#FFD700'}
        style3 = {'fillColor': 'transparent', 'color': '#008080'}
        style4 = {'fillColor': 'transparent', 'color': '#708090'}

        #add build polygon using folium.GeoJson, from geojson files exported from qgis
        # it also work with folium.Polyline but by organizing the data by a list of tuples 
        folium.GeoJson(
            data=gdf_ro['geometry'], 
            name="Romanian Country Borders", 
            style_function=lambda x:style3,
            show=True).add_to(m)
        folium.GeoJson(
            data=gdf_n2ksite['geometry'], 
            name="Natura 2000 Site Bucegi", 
            style_function=lambda x:style2,
            show=True).add_to(m)
        folium.GeoJson(
            data=gdf_uat['geometry'], 
            name="Neighbouring U.A.T borders", 
            style_function=lambda x:style4,
            show=False).add_to(m)
        # folium.GeoJson(data=gdf_park['geometry'], name="Bucegi Natural Park", style_function=lambda x:style1).add_to(m)
        # Add a layer control panel to the map.
    except Exception as e:
        messages.error(request, f"Error! Sorry for the inconvenience:{e}")
    m.add_child(folium.LayerControl())
    #fullscreen
    plugins.Fullscreen().add_to(m)
    #GPS
    plugins.LocateControl().add_to(m)
    #mouse position
    fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(m)
    #add the draw
    plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(m)  
    #add lat long popup
    m.add_child(folium.LatLngPopup())
    #Add measure tool 
    # plugins.MeasureControl(
    #     position='topright', 
    #     primary_length_unit='meters', 
    #     secondary_length_unit='kilometers', 
    #     primary_area_unit='sqmeters', 
    #     secondary_area_unit='sqmeters').add_to(m)
    #add park visitor center location
    htmlcode1 = """<div><img src="https://bucegipark.ro/static/img/history/centru-vizitare.502b87af7fea.webp" alt="Park Visitor Center" width="230" height="172">
    <br /><span>Visitor Center</span>
    </div>"""
    tooltip1 = _("Visitor Center")
    folium.Marker([45.409356379968216, 25.52737196715158], popup=htmlcode1, tooltip=tooltip1, icon=folium.Icon(color="red", icon="fa-landmark", prefix='fa')).add_to(m)
    #add park headquarters location
    htmlcode2 = """<div><img src="https://bucegipark.ro/static/img/infrastructure/sediu-moroieni.d22b12974d50.webp" alt="Park Main Office" width="230" height="172">
    <br /><span>Main Office</span>
    </div>"""
    tooltip2 = _("Main Office")
    folium.Marker([45.23479894277473, 25.441066582484247], popup=htmlcode2, tooltip=tooltip2, icon=folium.Icon(color="red", icon="fa-building", prefix='fa')).add_to(m)
    #add park info point Pestera
    htmlcode3 = """<div><img src="https://bucegipark.ro/static/img/infrastructure/pct-info-pestera.0455012a0e8c.webp" alt="Park Info Point" width="230" height="172">
    <br /><span>Peștera Information Point</span>
    </div>"""
    tooltip3 = _("Info Point")
    folium.Marker([45.39814979266247, 25.44159584180792], popup=htmlcode3, tooltip=tooltip3, icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    m=m._repr_html_() #updated
    context = {'map': m}
    return render(request, template_name, context)