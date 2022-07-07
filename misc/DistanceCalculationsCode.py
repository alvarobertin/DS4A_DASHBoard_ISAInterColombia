# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 17:32:25 2022 for ISA Colombia

@authors: Team 248 DS4A. Marcos Barrera, Alvaro Bertin, Harold Uribe, Elemir Arias, Diego Zapata, Sebastian Alfonso


"""

#LOAD REQUIREMENTS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from  lidar import *
import pkg_resources
import numpy as np
from scipy.spatial import cKDTree
import laspy as lp
import laspy

###
### CHANGE THIS FILE LOCATION TO THE USED ON THE COMPUTER THAT WILL RUN THIS.
###

#TXT Files containing the features. 
file1 = '/content/drive/Shareddrives/DS4A/ISAIntercolombia_Inspección_lineas_con_Lidar_FranciscoContreras/MDS-10.txt'
#TXT Files containing POINT COLORS. 
filez1 = '/content/drive/Shareddrives/DS4A/Data_las/LAS-10.csv'


#Feature dictionary of features according to Isas provider
feature = {200:'Terreno natural',
201:'Terreno MDT (GRILLADO)',
300:'Árboles mayores a 1m. de altura',
301:'Árboles menores a 1m. de altura',
400:'Vía principal (avenida)',
401:'Vía secundaría',
404:'Carreteable',
406:'Vías Férreas',
500:'Edificio, casa, construcción',
504:'Tuberías',
506:'Silo',
509:'Puentes',
515:'Señal de transito o valla publicitaria',
518:'Estanques de combustible ',
600:'Río o canal navegable',
601:'Río o canal no navegable',
603:'Lago o jagüey',
698:'Torre existente alta tensión 34.5 kV',
701:'Torre existente alta tensión 230 kV',
702:'Torre existente alta tensión 500 kV',
703:'Torre existente otras',
704:'Postes ',
705:'Conductor de alta tensión 34.5 kV',
708:'Conductor de alta tensión 230 kV',
709:'Conductor de alta tensión 500 kV',
710:'Cable Guardia línea Eléctrica',
711:'Conductor otros',
712:'Cable de comunicación',
715:'Subestación',
101:'Riesgo Terreno Alto',
104:'Riesgo Vegetación Alto',
105:'Riesgo Vegetación Medio',
106:'Riesgo Vegetación Bajo',
107:'Riesgo Conductores Alto',
111:'Riesgo Carretera Alto'} 



#########################
### DATA PREPARATION  ###
#########################

#Read file with feature codes. 
df = pd.read_csv(file1, sep=' ', header=None)
df = df.rename(columns={0:'feature_code', 1 : 'ortophoto_x', 2: "ortophoto_y", 3:'mds_z'}, errors="raise")

#Clasify codes to given descriptions. 
df['Description'] =df['feature_code'].map(feature)
df['file'] = 'MDS-01'

#read file with rgb columns processed by the lidar files.
dfz1 = pd.read_csv(filez1, sep=',')#, header=None)

#Round the coordinates to 3 decimals. This way both files will be the same. 
dfz1['x'] = dfz1['x'].round(decimals = 3)
dfz1['y'] = dfz1['y'].round(decimals = 3)
dfz1['z'] = dfz1['z'].round(decimals = 3)


#Rename column index. This will be used as the main ID between both files.
dfz1.rename(columns = {'Unnamed: 0':'dfz_index'}, inplace = True)


#############################
### DISTANCE CALCULATIONS ###
#############################

#df = df.sort_values(by=['ortophoto_y']) #Use this only if files are ordered different.

#Join both files. 
df_for_dist = df.join(dfz1)

#Select only columns to use.
df_for_dist = df_for_dist[['dfz_index', 'file', 'x', 'y', 'z', 'feature_code', 'Description', 'r', 'g', 'b']]

#Define list of points that are cables and will be the reference points for calculate the distances
cable_points =  df_for_dist.index[(df_for_dist['feature_code'] == 708) | (df_for_dist['feature_code'] == 710) | (df_for_dist['feature_code'] == 712) ].tolist()

#Calculate the model with the distances 
tree2 = cKDTree(df_for_dist[['x',  'y',  'z']])

#Loop to save each point calculation. Will look 150 nearest points from the cables.  
distancesarray = []  #Create empty arrays
neightborarray = []
nearest_df = pd.DataFrame()
for x in cable_points:#[0:100]:   #Will iterate only the first 100 cable records for test. Delete [0:100] to iterate in every line point.
  neighbors_distance, neighbors_indices = tree2.query(df_for_dist[['x',  'y',  'z']].iloc[[x]], k=150, n_jobs = -1, eps = 20)  #Iterate on evey cable point using the coordinates
  nearest_df = nearest_df.append({'Reference':x,'Distances':neighbors_distance,'Nearest_Index':neighbors_indices},ignore_index=True) 
  #myarray = np.concatenate(neighbors_distance, neighbors_indices)
  distancesarray.append(neighbors_distance) #Append each array. Will create a list of arrays with distance values.
  neightborarray.append(neighbors_indices) #Append each array. Will create a list of arrays with index of each neighbor.

#Take the list of index and transform it into a DF. 
np.vstack(neightborarray)
neightborarray = np.vstack(neightborarray)
neightborarray = pd.DataFrame(neightborarray)

#Unpivot a DataFrame from wide to long format,
neightborarray = neightborarray.melt(id_vars=0)
neightborarray = neightborarray[[0,'value']]

#Rename columns to understandable names
neightborarray.rename(columns = {0:'Reference', 'value':'Neighbour'}, inplace = True)

#Take the distances array and transform it into a DF. 
np.vstack(distancesarray)
distancesarray = np.vstack(distancesarray)
distancesarray = pd.DataFrame(distancesarray)

distancesarray = distancesarray.melt(id_vars=0)
distancesarray = distancesarray[[0,'value']]
distancesarray.rename(columns = {0:'Reference_dist', 'value':'Distance'}, inplace = True)

#Merge the two DF into one with the index and the distances
distances_df = neightborarray.join(distancesarray)
distances_df = distances_df[['Reference','Neighbour','Distance']]

#Drop the rows with cable neighbours. 
distances_df = distances_df[~distances_df.Neighbour.isin(cable_points)]

#Select Neighbour with lowest distance to put the color in it. 
distances_df = distances_df.sort_values('Distance').drop_duplicates(['Neighbour'], keep='first')

#Reset index so we can use it to merge
df = df.reset_index()
#select only feature codes and description to merge with the distances results
dffeatures = df[['index', 'feature_code','Description']]


###############################################
### Change RGB Colors and Risk Calculations ###
###############################################

#Define points codes to use in the Risk calculations
#NOTE: IF CODES CHANGE, THIS SHOULD BE CHANGED ACCORDINGLY
tension = [34.5, 230, 500] #voltaje de las tensiones de las lineas
terreno = [200, 201, 101]
vegetacion = [300, 301, 104, 105, 106]
carreteras = [400, 401, 404, 111]
otras_lineas = [698, 702, 703, 704, 705, 706, 707, 708, 709, 715, 107] # 701, 711, 712, 710
rios = [600, 601, 603]
objetos = [500, 505, 506, 509, 515, 518]

#Select only distances below 11 meters. Higher distances are not relevant to this calculations.
distances_df = distances_df[distances_df['Distance'] < 11]

#Merge the dataframe with the distances to the original dataframe. Select columns to use.
df_for_dist = df_for_dist.reset_index()
final_df = df_for_dist.merge(distances_df, how= 'left', left_on='index', right_on='Neighbour' )
final_df = final_df[['x','y','z','feature_code','r','g','b','Neighbour','Distance']]

#Risk type criteria definition. Change this accordingly.
filters = [
   (final_df.Distance.notnull()) & (final_df["feature_code"].isin(vegetacion)),
   (final_df.Distance.notnull()) & (final_df["feature_code"].isin(otras_lineas)),
   (final_df.Distance.notnull()) & (final_df["feature_code"].isin(terreno)),
   (final_df.Distance.notnull()) & (final_df["feature_code"].isin(carreteras)),
   (final_df.Distance.notnull()) & (final_df["feature_code"].isin(objetos))
]
values = ['Vegetation Risk','Other Lines Risks','Terrain Risk', 'Road Risk','Object Risk'] 

#Create the Risk type column
final_df['Risk Type'] = np.select(filters, values)

#Risk level definition according to the risk type. Change this if any change is made to the criteria.
filters2 = [
   (final_df.Distance <= 5)  & (final_df["feature_code"].isin(vegetacion)),
   (final_df.Distance > 5) & (final_df.Distance <= 7) & (final_df["feature_code"].isin(vegetacion)),
   (final_df.Distance > 7) & (final_df["feature_code"].isin(vegetacion)),
   (final_df.Distance <= 4) & (final_df["feature_code"].isin(terreno)),
   (final_df.Distance > 4) & (final_df.Distance <= 5)  & (final_df["feature_code"].isin(terreno)),
   (final_df.Distance > 5) & (final_df["feature_code"].isin(terreno)),
   (final_df.Distance <= 7) & (final_df["feature_code"].isin(carreteras)),
   (final_df.Distance > 7) & (final_df["feature_code"].isin(carreteras)),
   (final_df.Distance <= 3 ) & (final_df["feature_code"].isin(otras_lineas)),
   (final_df.Distance > 3 ) & (final_df["feature_code"].isin(otras_lineas)),
   (final_df.Distance <= 15 ) & (final_df["feature_code"].isin(objetos)),
   (final_df.Distance > 15 ) & (final_df.Distance <= 30 ) & (final_df["feature_code"].isin(objetos))
]
values2 = ['High Risk','Medium Risk','Low Risk',
           'High Risk','Medium Risk','Low Risk',
           'High Risk', 'Low Risk',
           'High Risk', 'Low Risk',
           'High Risk','Medium Risk']

#Apply risk level criteria.
final_df['Risk_Level'] = np.select(filters2, values2)

#Change RGB Colors columns according to the risk level.
#'High Risk'
final_df['r'] = np.where(final_df['Risk_Level'] == 'High Risk' , 245, final_df['r'])
final_df['g'] = np.where(final_df['Risk_Level'] == 'High Risk' , 24, final_df['g'])
final_df['b'] = np.where(final_df['Risk_Level'] == 'High Risk' , 24, final_df['b'])
#'Medium  Risk'
final_df['r'] = np.where(final_df['Risk_Level'] == 'Medium Risk' , 255, final_df['r'])
final_df['g'] = np.where(final_df['Risk_Level'] == 'Medium Risk' , 119, final_df['g'])
final_df['b'] = np.where(final_df['Risk_Level'] == 'Medium Risk' , 0, final_df['b'])
#'Low Risk'
final_df['r'] = np.where(final_df['Risk_Level'] == 'Low Risk' , 255, final_df['r'])
final_df['g'] = np.where(final_df['Risk_Level'] == 'Low Risk' , 255, final_df['g'])
final_df['b'] = np.where(final_df['Risk_Level'] == 'Low Risk' , 0, final_df['b'])

#Add color to the cables near points.
distances_df2 = distances_df.copy()
distances_df2 = distances_df2.rename(columns={'Reference':'Ref', 'Neighbour' : 'Nei', 'Distance': "Dis"}, errors="raise")
distances_df2 = distances_df2[['Ref','Dis']]


#Define the cable points that are near other points according to the distances.
cables_near_points_low = distances_df2[ (distances_df2['Dis'] >= 6) &  (distances_df2['Dis'] < 11) ]['Ref'].unique()
cables_near_points_medium = distances_df2[ (distances_df2['Dis'] > 5) &  (distances_df2['Dis'] < 6)]['Ref'].unique()
cables_near_points_high = distances_df2[distances_df2['Dis'] <= 4]['Ref'].unique()

#High Risk cable color
final_df['r'] = np.where(final_df['index'].isin(cables_near_points_high) , 245, final_df['r'])
final_df['g'] = np.where(final_df['index'].isin(cables_near_points_high) , 24, final_df['g'])
final_df['b'] = np.where(final_df['index'].isin(cables_near_points_high) , 24, final_df['b'])
#Medium Risk cable color
final_df['r'] = np.where(final_df['index'].isin(cables_near_points_medium) , 245, final_df['r'])
final_df['g'] = np.where(final_df['index'].isin(cables_near_points_medium) , 119, final_df['g'])
final_df['b'] = np.where(final_df['index'].isin(cables_near_points_medium) , 0, final_df['b'])
#Low Risk cable color
final_df['r'] = np.where(final_df['index'].isin(cables_near_points_low) , 245, final_df['r'])
final_df['g'] = np.where(final_df['index'].isin(cables_near_points_low) , 255, final_df['g'])
final_df['b'] = np.where(final_df['index'].isin(cables_near_points_low) , 24, final_df['b'])

#Select final columns to export
final_df = final_df[['x', 'y', 'z', 'feature_code', 'r', 'g', 'b', 'Neighbour', 'Distance', 'Risk Type', 'Risk_Level']]

#Save file to path.
final_df.to_csv('/content/drive/Shareddrives/DS4A/Data_las/With_Distances/Line10_w_distances.csv', encoding='utf-8', index=False)






