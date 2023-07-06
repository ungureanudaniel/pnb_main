from django.shortcuts import render
# generic base view
from django.views.generic import TemplateView 
#folium
import folium
from folium import plugins
#gee
import ee

ee.Initialize()


#============map page view============================================
class map_bk(TemplateView):
    template_name = 'geemap/map.html'

    # Define a method for displaying Earth Engine image tiles on a folium map.
    def get_context_data(self, **kwargs):

        figure = folium.Figure()
        
        #create Folium Object
        m = folium.Map(
            location=[25.4273518, 45.45495724],
            zoom_start=8
        )

        #add map to figure
        m.add_to(figure)

        
        #select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                  .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
                  .first())
        modisndvi = dataset.select('NDVI')

        #Styling 
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        
        #add the map to the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
       
        #GEE raster data to TileLayer
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = True,
                    control = True
                    ).add_to(m)

        
        #add Layer control
        m.add_child(folium.LayerControl())
       
        #figure 
        figure.render()
         
        #return map
        return {"map": figure}

def map_view(request):
    template_name = 'geemap/map.html'
    
    #creation of map comes here + business logic
    m = folium.Map([45.45, 25.42], zoom_start=10, tiles ='Stamen Terrain', control_scale = True)
    # Add a layer control panel to the map.
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
    #Add measure tool 
    plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
    test = folium.Html('<b>Hello world</b>', script=True)
    popup = folium.Popup(test, max_width=4050)
    folium.RegularPolygonMarker(location=[44.45, 25.42], popup=popup).add_to(m)
    m=m._repr_html_() #updated
    context = {'map': m}

    return render(request, template_name, context)