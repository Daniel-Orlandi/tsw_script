import xarray
import rioxarray
import numpy
import geopandas
import pandas
import matplotlib.pyplot as plt

def convet_180(data):
    lon_name = 'lon'
    data['_longitude_adjusted'] = xarray.where(data[lon_name]>180,
                                    data[lon_name]-360,
                                    data[lon_name])

    data = (data.swap_dims({lon_name: '_longitude_adjusted'}).sel(**{'_longitude_adjusted': sorted(data._longitude_adjusted)}).drop(lon_name))    
    data = data.rename({'_longitude_adjusted': lon_name})
    return data

data = xarray.open_dataset("/mnt/d/work/code_projects/complete/tsw_script/data/GRCTellus.JPL.200204_202012.GLO.RL06M.MSCNv02CRI.nc")
shp_file = geopandas.read_file('/mnt/d/work/code_projects/complete/tsw_script/SIN/Contorno_Bacias_rev2.shp', crs="epsg:4326")
data = convet_180(data)
data = data.lwe_thickness
climatology = data.groupby('time.month').mean('time')
anomalies = data.groupby('time.month') - climatology
anomalies.rio.set_spatial_dims(x_dim="lon", y_dim="lat", inplace=True)
anomalies.rio.write_crs("epsg:4326", inplace=True)
anomalies.rio.set_crs("epsg:4326", inplace=True)

bacias = shp_file["Nome_Bacia"].unique()
result_dict = {}

for bacia in bacias:
    shp = shp_file[shp_file["Nome_Bacia"] == bacia]
    result = anomalies.rio.clip(shp.geometry,shp.crs)
    anom_result = [[numpy.nanmean(result.isel(time=time_)), result.isel(time=time_).time.data] for time_ in range(len(result.time))]
    result_dict[bacia] = anom_result

for bacia in bacias:
    temp_df = pandas.DataFrame(result_dict[bacia])
    temp_df = temp_df.rename(columns = {0: "tsw_anomaly(cm)", 1: "date"})
    temp_df = temp_df[["date", "tsw_anomaly(cm)"]]
    temp_df.to_csv("/mnt/d/work/code_projects/complete/tsw_script/data/results/tsw_anom_"+bacia+".csv")
