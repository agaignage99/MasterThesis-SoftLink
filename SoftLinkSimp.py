# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 11:55:28 2023

@author: Antoine Gaigngage 

UCLouvain-EPL

TFE23-631: Soft-link between a multi-energy optimization tool and an electrical adequacy assessment tool

Supervisor: Pr.Emmanuel De Jaeger
"""

import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt

# assets_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/assets.txt", delimiter="\t")
# layer_ELEC=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/hourly_data/layer_ELECTRICITY.txt", delimiter="\t")
# year_balance_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/year_balance.txt", delimiter="\t")
# resources_breakdown_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/resources_breakdown.txt", delimiter="\t")
# layer_H2=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/hourly_data/layer_H2.txt", delimiter="\t")
# cost_breakdown_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/case_studies/ref_run/output/cost_breakdown.txt",delimiter="\t")

##########################################################Scenario Basic
assets_df=pd.read_csv("DataES/Basic/output/assets.txt", delimiter="\t")
layer_ELEC=pd.read_csv("DataES/Basic/output/hourly_data/layer_ELECTRICITY.txt", delimiter="\t")
year_balance_df=pd.read_csv("DataES/Basic/output/year_balance.txt", delimiter="\t")
resources_breakdown_df=pd.read_csv("DataES/Basic/output/resources_breakdown.txt", delimiter="\t")
layer_H2=pd.read_csv("DataES/Basic/output/hourly_data/layer_H2.txt", delimiter="\t")
cost_breakdown_df=pd.read_csv("DataES/Basic/output/cost_breakdown.txt",delimiter="\t")
##############################TDtoD
TDtoD_df=pd.read_csv("DataES/Basic/TDtoD.txt", delimiter="\t")


# ##########################################################Scenario House
# assets_df=pd.read_csv("DataES/House/output/assets.txt", delimiter="\t")
# layer_ELEC=pd.read_csv("DataES/House/output/hourly_data/layer_ELECTRICITY.txt", delimiter="\t")
# year_balance_df=pd.read_csv("DataES/House/output/year_balance.txt", delimiter="\t")
# resources_breakdown_df=pd.read_csv("DataES/House/output/resources_breakdown.txt", delimiter="\t")
# layer_H2=pd.read_csv("DataES/House/output/hourly_data/layer_H2.txt", delimiter="\t")
# cost_breakdown_df=pd.read_csv("DataES/House/output/cost_breakdown.txt",delimiter="\t")
# ###############################TDtoD
# TDtoD_df=pd.read_csv("DataES/House/TDtoD.txt", delimiter="\t")

##################################################DATAinES##########################################################
Resources_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Resources.csv", delimiter=";")
Technologies_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Technologies.csv", delimiter=";")
Time_series_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Time_series.csv", delimiter=";")
layer_in_out_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Layers_in_out.csv", delimiter=";")

Resources_df.columns = ["Category", "Subcategory","parameter name","avail","gwp_op","c_op","CO2_op","Comment"]

##################################################PreDATA##########################################################

####################################BUSES######################################

BusesShare_df=pd.read_csv("PreData/BusesShare.txt", delimiter="\t")

###############################Lines###########################################

Lines_df=pd.read_csv("PreData/EarlyDataLines.csv", delimiter=";")


#H2Pipeline######################################################################

H2Pipeline_df=pd.read_csv("PreData/H2Pipeline.txt", delimiter="\t")

#H2Export######################################################################

H2Export_df=pd.read_csv("PreData/H2Export.txt", delimiter="\t")



###########################PARAMETRE##########################################

#Seuil de Puissane

powerSeuil = 1e-5 #GW

#Batt_Li

Share_LargeScaleP=0.62
Share_SmallScaleP=0.32

Share_LargeScaleC=0.35
Share_SmallScaleC=0.65

###############################Détermine le cout des fuels#####################

qty_GAZ=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'GAS')].iloc[0]['Used'])
qty_GAZ_RE=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'GAS_RE')].iloc[0]['Used'])

if qty_GAZ+qty_GAZ_RE != 0:
    
    cost_GAZ=float(Resources_df[ (Resources_df["parameter name"] == 'GAS')].iloc[0]['c_op'])*(qty_GAZ/(qty_GAZ+qty_GAZ_RE))  +   float(Resources_df[ (Resources_df["parameter name"] == 'GAS_RE')].iloc[0]['c_op'])*(qty_GAZ_RE/(qty_GAZ+qty_GAZ_RE)) 
else:
    cost_GAZ=0

    
qty_AMMONIA=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'AMMONIA')].iloc[0]['Used'])
qty_AMMONIA_RE=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'AMMONIA_RE')].iloc[0]['Used'])
    
if qty_AMMONIA+qty_AMMONIA_RE != 0:
    
    cost_AMMONIA=float(Resources_df[ (Resources_df["parameter name"] == 'AMMONIA')].iloc[0]['c_op'])*(qty_AMMONIA/(qty_AMMONIA+qty_AMMONIA_RE))  +   float(Resources_df[ (Resources_df["parameter name"] == 'AMMONIA_RE')].iloc[0]['c_op'])*(qty_AMMONIA_RE/(qty_AMMONIA+qty_AMMONIA_RE)) 
else:
    cost_AMMONIA=0    
    
qty_H2=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'H2')].iloc[0]['Used'])
qty_H2_RE=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'H2_RE')].iloc[0]['Used'])
    
if qty_H2+qty_H2_RE != 0:
    
    cost_H2=float(Resources_df[ (Resources_df["parameter name"] == 'H2')].iloc[0]['c_op'])*(qty_H2/(qty_H2+qty_H2_RE))  +   float(Resources_df[ (Resources_df["parameter name"] == 'H2_RE')].iloc[0]['c_op'])*(qty_H2_RE/(qty_H2+qty_H2_RE)) 
else:
    cost_H2=0      


################################TimeSeries#####################################
Time_series_Electricity=Time_series_df['Electricity (%_elec)']
Time_series_Space_Heating=Time_series_df['Space Heating (%_sh)']
Time_series_Passanger_mobility=Time_series_df['Passanger mobility (%_pass)']
Time_series_PV=Time_series_df['PV']
Time_series_Wind_onshore=Time_series_df['Wind_onshore']
Time_series_Wind_offshore=Time_series_df['Wind_offshore']				
Time_series_Hydro_river=Time_series_df['Hydro_river']



np.savetxt('Time_series_Electricity.txt',Time_series_Electricity , fmt='%.6f')
np.savetxt('Time_series_Space_Heating.txt',Time_series_Space_Heating , fmt='%.6f')
np.savetxt('Time_series_Passanger_mobility.txt',Time_series_Passanger_mobility , fmt='%.6f')
np.savetxt('Time_series_PV.txt',Time_series_PV , fmt='%.6f')

np.savetxt('Time_series_Wind_onshore.txt',Time_series_Wind_onshore , fmt='%.6f')
np.savetxt('Time_series_Wind_offshore.txt',Time_series_Wind_offshore , fmt='%.6f')
np.savetxt('Time_series_Hydro_river.txt',Time_series_Hydro_river , fmt='%.6f')


##############################General##########################################

General={#'VOLL_[€/MWh]':[1000],
         'VOLL_[M€/GWh]':[1],
         'Base_Voltage_of_HV_grid_[kV]':[380]}

General_df= pd.DataFrame(General)




#Buses_df=pd.read_csv("PreData/EarlyDataBuses.txt", delimiter="\t")

####################################Share######################################

#Share_df=pd.read_csv("PreData/ShareTot.txt", delimiter="\t")





###############################################################################
################################GEN############################################
###############################################################################


################################NUCLEAR########################################

Power_NUCLEAR=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'NUCLEAR')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='NUCLEAR'].iloc[0]['ELECTRICITY'])
cp_NUCLEAR=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'NUCLEAR')].iloc[0][' c_p'])




Energy_NUCLEAR=float(year_balance_df[ (year_balance_df["Tech"] == ' NUCLEAR ')].iloc[0]['ELECTRICITY'])
Energy_NUCLEAR=Energy_NUCLEAR#*1e3

NUCLEAR_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' NUCLEAR ')].iloc[0]['c_maint'])
#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'NUCLEAR')].iloc[0]['C_maint']))/Energy_NUCLEAR   
NUCLEAR_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'URANIUM')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='NUCLEAR'].iloc[0]['URANIUM'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='NUCLEAR'].iloc[0]['ELECTRICITY'])))
    
if Energy_NUCLEAR!=0:
    LF_NU=Energy_NUCLEAR/(Power_NUCLEAR*8760) 
else:
    LF_NU=None

if Power_NUCLEAR<powerSeuil:
    LF_NU=0
    Power_NUCLEAR=0
    NUCLEAR_C_maint=0
    NUCLEAR_C_op=0
    print('NUCLEAR OFF')
    
else:
    print('NUCLEAR ON')


Power_NUCLEAR=Power_NUCLEAR#*1e3
coefNU_DOEL=0.49
coefNU_TIHA=0.51

NU_DOEL=coefNU_DOEL*Power_NUCLEAR
NU_TIHA=coefNU_DOEL*Power_NUCLEAR
#cost_breakdown

#LF_NU=Energy_NUCLEAR/(8760*Power_NUCLEAR)

###################################CCGT########################################

Power_CCGT=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'CCGT')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT'].iloc[0]['ELECTRICITY'])
Power_CCGT_AMMONIA=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'CCGT_AMMONIA')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT_AMMONIA'].iloc[0]['ELECTRICITY'])


Energy_CCGT=float(year_balance_df[ (year_balance_df["Tech"] == ' CCGT ')].iloc[0]['ELECTRICITY'])

Energy_CCGT_AMMONIA=float(year_balance_df[ (year_balance_df["Tech"] == ' CCGT_AMMONIA ')].iloc[0]['ELECTRICITY'])


Power_GAZ_tot=Power_CCGT+Power_CCGT_AMMONIA
Energy_GAZ_tot=Energy_CCGT+Energy_CCGT_AMMONIA

if Energy_GAZ_tot!=0:
    LF_GAZ=Energy_GAZ_tot/(Power_GAZ_tot*8760) 
else:
    LF_GAZ=None



CCGT_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' CCGT ')].iloc[0]['c_maint'])

#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'CCGT')].iloc[0]['C_maint'])   
CCGT_C_op= cost_GAZ*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT'].iloc[0]['GAS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT'].iloc[0]['ELECTRICITY'])))
#print(CCGT_C_op)

CCGT_AMMONIA_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' CCGT_AMMONIA ')].iloc[0]['c_maint'])

#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'CCGT_AMMONIA')].iloc[0]['C_maint'])
CCGT_AMMONIA_C_op=cost_AMMONIA*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT_AMMONIA'].iloc[0]['AMMONIA'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='CCGT_AMMONIA'].iloc[0]['ELECTRICITY'])))
#print(CCGT_AMMONIA_C_op)

if Energy_CCGT+Energy_CCGT_AMMONIA !=0:
    
    GAZ_C_maint=(CCGT_C_maint*(Energy_CCGT/Energy_GAZ_tot) + CCGT_AMMONIA_C_maint*(Energy_CCGT_AMMONIA/Energy_GAZ_tot))
    GAZ_C_op=CCGT_C_op*(Energy_CCGT/Energy_GAZ_tot) + CCGT_AMMONIA_C_op*(Energy_CCGT_AMMONIA/Energy_GAZ_tot)
    
else:
    GAZ_C_maint=0
    GAZ_C_op=0

if Power_GAZ_tot<powerSeuil:
    Power_GAZ_tot=0
    LF_Gaz=0
    GAZ_C_maint=0
    GAZ_C_op=0
    print('GAZ OFF')
else:
    print('GAZ ON')
        


#LF_GAZ=Energy_GAZ_tot/(Power_GAZ_tot*8760)

# cp_CCGT=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'CCGT')].iloc[0][' c_p'])
# LF_CCGT=Energy_CCGT/(8760*Power_CCGT)

# Power_Gaz=(Power_CCGT+Power_CCGT_AMMONIA)#*1e3 


#######################
#Détermine le coeficient de répartition de la production en gaz voir MappingPop.xlsx
#######################

coefGAZ_GOUY=0.258
coefGAZ_SERAI=0.137
coefGAZ_MEKI=0.098
coefGAZ_RODE=0.179
coefGAZ_GEZEL=0.102
coefGAZ_MEERH=0.09
coefGAZ_VERBR=0.054
coefGAZ_ZANDV=0.082

#######################
#Déterminer la puissance installée en gaz à chaque noeuds
#######################

GAZ_GOUY=coefGAZ_GOUY*Power_GAZ_tot
GAZ_SERAI=coefGAZ_SERAI*Power_GAZ_tot
GAZ_MEKI=coefGAZ_MEKI*Power_GAZ_tot #node MEKI+
GAZ_RODE=coefGAZ_RODE*Power_GAZ_tot #node RODE+
GAZ_GEZEL=coefGAZ_GEZEL*Power_GAZ_tot
GAZ_MEERH=coefGAZ_MEERH*Power_GAZ_tot
GAZ_VERBR=coefGAZ_VERBR*Power_GAZ_tot
GAZ_ZANDV=coefGAZ_ZANDV*Power_GAZ_tot

##############################CHP##############################################
Power_IND_COGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'IND_COGEN_GAS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_GAS'].iloc[0]['ELECTRICITY'])
Power_IND_COGEN_WOOD=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'IND_COGEN_WOOD')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WOOD'].iloc[0]['ELECTRICITY'])
Power_IND_COGEN_WASTE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'IND_COGEN_WASTE')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WASTE'].iloc[0]['ELECTRICITY'])


Energy_IND_COGEN_GAS=float(year_balance_df[ (year_balance_df["Tech"] == ' IND_COGEN_GAS ')].iloc[0]['ELECTRICITY']) 
Energy_IND_COGEN_WOOD=float(year_balance_df[ (year_balance_df["Tech"] == ' IND_COGEN_WOOD ')].iloc[0]['ELECTRICITY']) 
Energy_IND_COGEN_WASTE=float(year_balance_df[ (year_balance_df["Tech"] == ' IND_COGEN_WASTE ')].iloc[0]['ELECTRICITY']) 

PowerCHP=(Power_IND_COGEN_GAS+Power_IND_COGEN_WOOD+Power_IND_COGEN_WASTE) #GW to MW
EnergyCHP=(Energy_IND_COGEN_GAS+Energy_IND_COGEN_WOOD+Power_IND_COGEN_WASTE)

if EnergyCHP!=0:
   LF_CHP=EnergyCHP/(PowerCHP*8760) 
else:
    LF_CHP=None
print('LF CHP')
print(LF_CHP)

#LF_CHP=EnergyCHP/(PowerCHP*8760)

IND_COGEN_GAS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' IND_COGEN_GAS ')].iloc[0]['c_maint'])

#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'IND_COGEN_GAS')].iloc[0]['C_maint'])   
IND_COGEN_GAS_C_op= cost_GAZ*abs(float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_GAS'].iloc[0]['GAS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_GAS'].iloc[0]['ELECTRICITY']))

IND_COGEN_WOOD_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' IND_COGEN_WOOD ')].iloc[0]['c_maint'])
#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'IND_COGEN_WOOD')].iloc[0]['C_maint'])   
IND_COGEN_WOOD_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WOOD')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WOOD'].iloc[0]['WOOD'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WOOD'].iloc[0]['ELECTRICITY'])))


IND_COGEN_WASTE_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' IND_COGEN_WASTE ')].iloc[0]['c_maint'])
#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'IND_COGEN_WASTE')].iloc[0]['C_maint'])   
IND_COGEN_WASTE_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WASTE')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WASTE'].iloc[0]['WASTE'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_COGEN_WASTE'].iloc[0]['ELECTRICITY'])))


if EnergyCHP !=0:
    
    CHP_C_maint=(IND_COGEN_GAS_C_maint*(Energy_IND_COGEN_GAS/EnergyCHP) + IND_COGEN_WOOD_C_maint*(Energy_IND_COGEN_WOOD/EnergyCHP) + IND_COGEN_WASTE_C_maint*(Energy_IND_COGEN_WASTE/EnergyCHP))/EnergyCHP
    CHP_C_op= IND_COGEN_GAS_C_op*(Energy_IND_COGEN_GAS/EnergyCHP) + IND_COGEN_WOOD_C_op*(Energy_IND_COGEN_WOOD/EnergyCHP) + IND_COGEN_WASTE_C_op*(Energy_IND_COGEN_WASTE/EnergyCHP)
    
else:
    CHP_C_maint=0
    CHP_C_op=0
    
    
if PowerCHP<powerSeuil:
    PowerCHP=0
    LF_CHP=0
    CHP_C_maint=0
    CHP_C_op=0
    print('CHP OFF')
else:
    print('CHP ON')    


coefCHP_BRUEG=0.047
coefCHP_MERCA=0.667
coefCHP_RODE=0.066 #RODE+
coefCHP_GEZEL=0.058
coefCHP_IZGEM=0.019
coefCHP_STAM=0.102 #STAM+
coefCHP_ZUTE=0.041 #ZUTE+

CHP_BRUEG=coefCHP_BRUEG*PowerCHP
CHP_MERCA=coefCHP_MERCA*PowerCHP
CHP_RODE=coefCHP_RODE*PowerCHP
CHP_GEZEL=coefCHP_GEZEL*PowerCHP
CHP_IZGEM=coefCHP_IZGEM*PowerCHP
CHP_STAM=coefCHP_STAM*PowerCHP
CHP_ZUTE=coefCHP_ZUTE*PowerCHP

##############################COAL#############################################

Power_COAL_US=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'COAL_US')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_US'].iloc[0]['ELECTRICITY'])
Power_COAL_IGCC=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'COAL_IGCC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_IGCC'].iloc[0]['ELECTRICITY'])


Power_COAL_tot=Power_COAL_US+Power_COAL_IGCC

Enery_COAL_US=float(year_balance_df[ (year_balance_df["Tech"] == ' COAL_US ')].iloc[0]['ELECTRICITY'])
Energy_COAL_IGCC=float(year_balance_df[ (year_balance_df["Tech"] == ' COAL_IGCC ')].iloc[0]['ELECTRICITY'])

Energy_COAL_tot=Enery_COAL_US+Energy_COAL_IGCC

if Energy_COAL_tot!=0:
   LF_COAL=Energy_COAL_tot/(Power_COAL_tot*8760) 
else:
    LF_COAL=None

COAL_RODE=Power_COAL_tot#*1e3 # GW to MW

COAL_US_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' COAL_US ')].iloc[0]['c_maint'])
#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'COAL_US')].iloc[0]['C_maint'])   
COAL_US_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'COAL')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_US'].iloc[0]['COAL'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_US'].iloc[0]['ELECTRICITY'])))

COAL_IGCC_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' COAL_IGCC ')].iloc[0]['c_maint'])
#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'COAL_IGCC')].iloc[0]['C_maint'])   
COAL_IGCC_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'COAL')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_IGCC'].iloc[0]['COAL'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='COAL_IGCC'].iloc[0]['ELECTRICITY'])))

if Power_COAL_tot !=0:
    
    COAL_C_maint=(COAL_US_C_maint*(Enery_COAL_US/Energy_COAL_tot) + COAL_IGCC_C_maint*(Energy_COAL_IGCC/Energy_COAL_tot))/Energy_COAL_tot
    COAL_C_op=COAL_US_C_op*(Enery_COAL_US/Energy_COAL_tot) + COAL_IGCC_C_op*(Energy_COAL_IGCC/Energy_COAL_tot)

else:
    COAL_C_maint=0
    COAL_C_op=0
    
    
if Power_COAL_tot<powerSeuil:
    Power_COAL_tot=0
    LF_COAL=0
    COAL_C_maint=0
    COAL_C_op=0
    print('COAL OFF')
else:
    print('COAL ON') 

    
#######################
#Remplir la dataframe GEN
#######################

Gen={'Generator':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
      'Name':['NU_DOEL','NU_TIHA','GAZ_GOUY','GAZ_SERAI','GAZ_MEKI','GAZ_RODE','GAZ_GEZEL','GAZ_MEERH','GAZ_VERBR','GAZ_ZANDV','COAL_RODE','CHP_BRUEG','CHP_MERCA','CHP_RODE','CHP_GEZEL','CHP_IZGEM','CHP_STAM','CHP_ZUTE'],
      'Node':['DOEL','TIHA1','GOUY','SERAI','MEKI+','RODE+','GEZEL','MEERH','VERBR','ZANDV','RODE+','BRUEG','MERCA','RODE+','GEZEL','IZGEM','STAM+','ZUTE+'],
      'Pmax_GWe':[NU_DOEL,NU_TIHA,GAZ_GOUY,GAZ_SERAI,GAZ_MEKI,GAZ_RODE,GAZ_GEZEL,GAZ_MEERH,GAZ_VERBR,GAZ_ZANDV,COAL_RODE,CHP_BRUEG,CHP_MERCA,CHP_RODE,CHP_GEZEL,CHP_IZGEM,CHP_STAM,CHP_ZUTE],
      #'MargCost_europerMWh':[10,10,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
      'Cost_maint_M€/GW/y':[NUCLEAR_C_maint,NUCLEAR_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,GAZ_C_maint,COAL_C_maint,CHP_C_maint,CHP_C_maint,CHP_C_maint,CHP_C_maint,CHP_C_maint,CHP_C_maint,CHP_C_maint],
      'Cost_op_M€/GWhe':[NUCLEAR_C_op,NUCLEAR_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,GAZ_C_op,COAL_C_op,CHP_C_op,CHP_C_op,CHP_C_op,CHP_C_op,CHP_C_op,CHP_C_op,CHP_C_op],
      'Type':['NU','NU','GAZ','GAZ','GAZ','GAZ','GAZ','GAZ','GAZ','GAZ','COAL','CHP','CHP','CHP','CHP','CHP','CHP','CHP'],
      'MTTF':[4976.941176,4976.941176,1530.73,1530.73,1530.73,1530.73,1530.73,1530.73,1530.73,1530.73,1530.73,2139.153846,2139.153846,2139.153846,2139.153846,2139.153846,2139.153846,2139.153846],
      'MTTR':[176,176,62,62,62,62,62,62,62,62,62,107,107,107,107,107,107,107],
      #'c_p':[],
      'LF':[LF_NU,LF_NU,LF_GAZ,LF_GAZ,LF_GAZ,LF_GAZ,LF_GAZ,LF_GAZ,LF_GAZ,LF_GAZ,LF_COAL,LF_CHP,LF_CHP,LF_CHP,LF_CHP,LF_CHP,LF_CHP,LF_CHP]  
      }

Gen_df=pd.DataFrame(Gen)


###############################################################################
################################DIST###########################################
###############################################################################

################################DistRes########################################

################################PV############################################# Pv_share
Power_PV=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'PV')].iloc[0][' f'])#*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='PV'].iloc[0]['ELECTRICITY'])*1e3 #GW to MW

#################################ONSHORE####################################### Onshore_share
Power_WIND_ONSHORE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'WIND_ONSHORE')].iloc[0][' f'])#*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='WIND_ONSHORE'].iloc[0]['ELECTRICITY'])*1e3 #GW to MW

###################################HYDRO####################################### Hydro_share_percent

Power_HYDRO_RIVER=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'HYDRO_RIVER')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='HYDRO_RIVER'].iloc[0]['ELECTRICITY'])
# Energy_HYDRO_RIVER=float(year_balance_df[ (year_balance_df["Tech"] == ' HYDRO_RIVER ')].iloc[0]['ELECTRICITY'])

# if Energy_HYDRO_RIVER != 0:
#     LF_HYDRO_RIVER=Energy_HYDRO_RIVER/(8760*Power_HYDRO_RIVER)
# else:
#     LF_HYDRO_RIVER=0


#######################
#Remplir la dataframe Dist Res
#######################

DistRes ={'Psolar_GWe':[Power_PV],
          'Ponshore_GWe':[Power_WIND_ONSHORE],
          'Power_HYDRO_RIVER_GWe':[Power_HYDRO_RIVER]
          }

DistRes_df = pd.DataFrame(DistRes)

#################################Geothermal####################################Share_Geothermal

# Power_Geothermal=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'GEOTHERMAL')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='HYDRO_RIVER'].iloc[0]['ELECTRICITY'])
# Energy_Geothermal=float(year_balance_df[ (year_balance_df["Tech"] == ' GEOTHERMAL ')].iloc[0]['ELECTRICITY'])

# Geothermal={'Power_Geothermal':[Power_Geothermal],
#             'Energy_Geothermal':[Energy_Geothermal]
#             }

# Geothermal_df= pd.DataFrame(Geothermal)


############################Dist_gen###########################################

##############################COGEN############################################SharePop

###########Power

Power_DHN_COGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_GAS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_GAS'].iloc[0]['ELECTRICITY'])
Power_DHN_COGEN_WOOD=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WOOD')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WOOD'].iloc[0]['ELECTRICITY'])
Power_DHN_COGEN_WASTE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WASTE')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WASTE'].iloc[0]['ELECTRICITY'])
Power_DHN_COGEN_WET_BIOMASS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WET_BIOMASS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WET_BIOMASS'].iloc[0]['ELECTRICITY'])
Power_DHN_COGEN_BIO_HYDROLYSIS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_BIO_HYDROLYSIS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_BIO_HYDROLYSIS'].iloc[0]['ELECTRICITY'])

Power_DEC_COGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_COGEN_GAS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_GAS'].iloc[0]['ELECTRICITY'])
Power_DEC_COGEN_OIL=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_COGEN_OIL')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_OIL'].iloc[0]['ELECTRICITY'])
Power_DEC_ADVCOGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_ADVCOGEN_GAS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_GAS'].iloc[0]['ELECTRICITY'])
Power_DEC_ADVCOGEN_H2=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_ADVCOGEN_H2')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['ELECTRICITY'])

##########Energy

Energy_DHN_COGEN_GAS=float(year_balance_df[ (year_balance_df["Tech"] == ' DHN_COGEN_GAS ')].iloc[0]['ELECTRICITY'])
Energy_DHN_COGEN_WOOD=float(year_balance_df[ (year_balance_df["Tech"] == ' DHN_COGEN_WOOD ')].iloc[0]['ELECTRICITY'])
Energy_DHN_COGEN_WASTE=float(year_balance_df[ (year_balance_df["Tech"] == ' DHN_COGEN_WASTE ')].iloc[0]['ELECTRICITY'])
Energy_DHN_COGEN_WET_BIOMASS=float(year_balance_df[ (year_balance_df["Tech"] == ' DHN_COGEN_WET_BIOMASS ')].iloc[0]['ELECTRICITY'])
Energy_DHN_COGEN_BIO_HYDROLYSIS=float(year_balance_df[ (year_balance_df["Tech"] == ' DHN_COGEN_BIO_HYDROLYSIS ')].iloc[0]['ELECTRICITY'])

#Energy_DHN_tot=Energy_DHN_COGEN_GAS+Energy_DHN_COGEN_WOOD+Energy_DHN_COGEN_WASTE+Energy_DHN_COGEN_WET_BIOMASS+Energy_DHN_COGEN_BIO_HYDROLYSIS

Energy_DEC_COGEN_GAS=float(year_balance_df[ (year_balance_df["Tech"] == ' DEC_COGEN_GAS ')].iloc[0]['ELECTRICITY'])
Energy_DEC_COGEN_OIL=float(year_balance_df[ (year_balance_df["Tech"] == ' DEC_COGEN_OIL ')].iloc[0]['ELECTRICITY'])
Energy_DEC_ADVCOGEN_GAS=float(year_balance_df[ (year_balance_df["Tech"] == ' DEC_ADVCOGEN_GAS ')].iloc[0]['ELECTRICITY'])
Energy_DEC_ADVCOGEN_H2=float(year_balance_df[ (year_balance_df["Tech"] == ' DEC_ADVCOGEN_H2 ')].iloc[0]['ELECTRICITY'])

#Energy_DEC_tot=Energy_DEC_COGEN_GAS+Energy_DEC_COGEN_OIL+Energy_DEC_ADVCOGEN_GAS+Energy_DEC_ADVCOGEN_H2

##########Cost_maint

DHN_COGEN_GAS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DHN_COGEN_GAS ')].iloc[0]['c_maint'])
    #(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DHN_COGEN_GAS')].iloc[0]['C_maint']))/Energy_DHN_COGEN_GAS   
DHN_COGEN_WOOD_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DHN_COGEN_WOOD ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DHN_COGEN_WOOD')].iloc[0]['C_maint']))/Energy_DHN_COGEN_WOOD 
DHN_COGEN_WASTE_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DHN_COGEN_WASTE ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DHN_COGEN_WASTE')].iloc[0]['C_maint']))/Energy_DHN_COGEN_WASTE 
DHN_COGEN_WET_BIOMASS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DHN_COGEN_WET_BIOMASS ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DHN_COGEN_WET_BIOMASS')].iloc[0]['C_maint']))/Energy_DHN_COGEN_WET_BIOMASS
DHN_COGEN_BIO_HYDROLYSIS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DHN_COGEN_BIO_HYDROLYSIS ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DHN_COGEN_BIO_HYDROLYSIS')].iloc[0]['C_maint']))/Energy_DHN_COGEN_BIO_HYDROLYSIS 
 
##############################################################################################   
DEC_COGEN_GAS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DEC_COGEN_GAS ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DEC_COGEN_GAS')].iloc[0]['C_maint']))/Energy_DEC_COGEN_GAS 
DEC_COGEN_OIL_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DEC_COGEN_OIL ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DEC_COGEN_OIL')].iloc[0]['C_maint']))/Energy_DEC_COGEN_OIL 
DEC_ADVCOGEN_GAS_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DEC_ADVCOGEN_GAS ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DEC_ADVCOGEN_GAS')].iloc[0]['C_maint']))/Energy_DEC_ADVCOGEN_GAS 
DEC_ADVCOGEN_H2_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' DEC_ADVCOGEN_H2 ')].iloc[0]['c_maint'])#(float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'DEC_ADVCOGEN_H2')].iloc[0]['C_maint']))/Energy_DEC_ADVCOGEN_H2 

##########Cost_op
DHN_COGEN_GAS_C_op= cost_GAZ*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_GAS'].iloc[0]['GAS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_GAS'].iloc[0]['ELECTRICITY'])))
DHN_COGEN_WOOD_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WOOD')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WOOD'].iloc[0]['WOOD'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WOOD'].iloc[0]['ELECTRICITY'])))
DHN_COGEN_WASTE_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WASTE')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WASTE'].iloc[0]['WASTE'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WASTE'].iloc[0]['ELECTRICITY'])))
DHN_COGEN_WET_BIOMASS_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WET_BIOMASS')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WET_BIOMASS'].iloc[0]['WET_BIOMASS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_WET_BIOMASS'].iloc[0]['ELECTRICITY'])))
DHN_COGEN_BIO_HYDROLYSIS_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'WET_BIOMASS')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_BIO_HYDROLYSIS'].iloc[0]['WET_BIOMASS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_COGEN_BIO_HYDROLYSIS'].iloc[0]['ELECTRICITY'])))

DEC_COGEN_GAS_C_op= cost_GAZ*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_GAS'].iloc[0]['GAS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_GAS'].iloc[0]['ELECTRICITY'])))
DEC_COGEN_OIL_C_op= float(Resources_df[ (Resources_df["parameter name"] == 'LFO')].iloc[0]['c_op'])*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_OIL'].iloc[0]['LFO'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_COGEN_OIL'].iloc[0]['ELECTRICITY'])))
DEC_ADVCOGEN_GAS_C_op= cost_GAZ*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_GAS'].iloc[0]['GAS'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_GAS'].iloc[0]['ELECTRICITY'])))
DEC_ADVCOGEN_H2_C_op= cost_H2*abs((float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['H2'])/float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['ELECTRICITY'])))


##########LF

LF_DHN_COGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_GAS')].iloc[0][' c_p'])
LF_DHN_COGEN_WOOD=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WOOD')].iloc[0][' c_p'])
LF_DHN_COGEN_WASTE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WASTE')].iloc[0][' c_p'])
LF_DHN_COGEN_WET_BIOMASS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_WET_BIOMASS')].iloc[0][' c_p'])
LF_DHN_COGEN_BIO_HYDROLYSIS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_COGEN_BIO_HYDROLYSIS')].iloc[0][' c_p'])

if Power_DHN_COGEN_GAS<powerSeuil:
    Power_DHN_COGEN_GAS=0
    Energy_DHN_COGEN_GAS=0
    LF_DHN_COGEN_GAS=0
    DHN_COGEN_GAS_C_maint=0
    DHN_COGEN_GAS_C_op=0
    print('DHN_COGEN_GAS OFF') 
else:
    print('DHN_COGEN_GAS ON') 
    
if Power_DHN_COGEN_WOOD<powerSeuil:
    Power_DHN_COGEN_WOOD=0
    Energy_DHN_COGEN_WOOD=0
    LF_DHN_COGEN_WOOD=0
    DHN_COGEN_WOOD_C_maint=0
    DHN_COGEN_WOOD_C_op=0
    print('DHN_COGEN_WOOD OFF')
else:
    print('DHN_COGEN_WOOD ON')     
    
if Power_DHN_COGEN_WASTE<powerSeuil:
    Power_DHN_COGEN_WASTE=0
    Energy_DHN_COGEN_WASTE=0
    LF_DHN_COGEN_WASTE=0
    DHN_COGEN_WASTE_C_maint=0
    DHN_COGEN_WASTE_C_op=0
    print('DHN_COGEN_WASTE OFF') 
else:
    print('DHN_COGEN_WASTE ON') 

if Power_DHN_COGEN_WET_BIOMASS<powerSeuil:
    Power_DHN_COGEN_WET_BIOMASS=0
    Energy_DHN_COGEN_WET_BIOMASS=0
    LF_DHN_COGEN_WET_BIOMASS=0
    DHN_COGEN_WET_BIOMASS_C_maint=0
    DHN_COGEN_WET_BIOMASS_C_op=0
    print('DHN_COGEN_WET_BIOMASS OFF')
else:
    print('DHN_COGEN_WET_BIOMASS ON') 

if Power_DHN_COGEN_BIO_HYDROLYSIS<powerSeuil:
    Power_DHN_COGEN_BIO_HYDROLYSIS=0
    Energy_DHN_COGEN_BIO_HYDROLYSIS=0
    LF_DHN_COGEN_BIO_HYDROLYSIS=0
    DHN_COGEN_BIO_HYDROLYSIS_C_maint=0
    DHN_COGEN_BIO_HYDROLYSIS_C_op=0
    print('DHN_COGEN_BIO_HYDROLYSIS OFF')
else:
    print('DHN_COGEN_BIO_HYDROLYSIS ON') 

LF_DEC_COGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_COGEN_GAS')].iloc[0][' c_p'])
LF_DEC_COGEN_OIL=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_COGEN_OIL')].iloc[0][' c_p'])
LF_DEC_ADVCOGEN_GAS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_ADVCOGEN_GAS')].iloc[0][' c_p'])
LF_DEC_ADVCOGEN_H2=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_ADVCOGEN_H2')].iloc[0][' c_p'])


if Power_DEC_COGEN_GAS<powerSeuil:
    Power_DEC_COGEN_GAS=0
    Energy_DEC_COGEN_GAS=0
    LF_DEC_COGEN_GAS=0
    DEC_COGEN_GAS_C_maint=0
    DEC_COGEN_GAS_C_op=0
    print('DEC_COGEN_GAS OFF')
else:
    print('DEC_COGEN_GAS ON') 
    
if Power_DEC_COGEN_OIL<powerSeuil:
    Power_DEC_COGEN_OIL=0
    Energy_DEC_COGEN_OIL=0
    LF_DEC_COGEN_OIL=0
    DEC_COGEN_OIL_C_maint=0
    DEC_COGEN_OIL_C_op=0
    print('DEC_COGEN_OIL OFF')
else:
    print('DEC_COGEN_OIL ON')     

if Power_DEC_ADVCOGEN_GAS<powerSeuil:
    Power_DEC_ADVCOGEN_GAS=0
    Energy_DEC_ADVCOGEN_GAS=0
    LF_DEC_ADVCOGEN_GAS=0
    DEC_ADVCOGEN_GAS_C_maint=0
    DEC_ADVCOGEN_GAS_C_op=0
    print('DEC_ADVCOGEN_GAS OFF')
else:
    print('DEC_ADVCOGEN_GAS ON')     
 
if Power_DEC_ADVCOGEN_H2<powerSeuil:
    Power_DEC_ADVCOGEN_H2=0
    Energy_DEC_ADVCOGEN_H2=0
    LF_DEC_ADVCOGEN_H2=0
    DEC_ADVCOGEN_H2_C_maint=0
    DEC_ADVCOGEN_H2_C_op=0
    print('DEC_ADVCOGEN_H2 OFF')
else:
    print('DEC_ADVCOGEN_H2 ON') 

  
#################################Geothermal####################################Share_Geothermal

Power_Geothermal=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'GEOTHERMAL')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='GEOTHERMAL'].iloc[0]['ELECTRICITY'])
Energy_Geothermal=float(year_balance_df[ (year_balance_df["Tech"] == ' GEOTHERMAL ')].iloc[0]['ELECTRICITY'])

if Energy_Geothermal != 0:
    LF_Geothermal=Energy_Geothermal/(8760*Power_Geothermal)
else:
    LF_Geothermal=0

GEOTHERMAL_C_maint=float(Technologies_df[ (Technologies_df["Technologies param"] == ' GEOTHERMAL ')].iloc[0]['c_maint'])#float(cost_breakdown_df[ (cost_breakdown_df["Name"] == 'GEOTHERMAL')].iloc[0]['C_maint']) 
GEOTHERMAL_C_op=0

if Power_Geothermal<powerSeuil:
    Power_Geothermal=0
    LF_Geothermal=0
    GEOTHERMAL_C_maint=0
    GEOTHERMAL_C_op=0
    print('Geothermal OFF')
else:
    print('Geothermal ON') 

###############################################################################



DistGen ={'Type':['DHN_COGEN_GAS','DHN_COGEN_WOOD','DHN_COGEN_WASTE','DHN_COGEN_WET_BIOMASS','DHN_COGEN_BIO_HYDROLYSIS','DEC_COGEN_GAS','DEC_COGEN_OIL','DEC_ADVCOGEN_GAS','DEC_ADVCOGEN_H2','GEOTHERMAL'],
          'Power_GWe':[Power_DHN_COGEN_GAS,Power_DHN_COGEN_WOOD,Power_DHN_COGEN_WASTE,Power_DHN_COGEN_WET_BIOMASS,Power_DHN_COGEN_BIO_HYDROLYSIS,Power_DEC_COGEN_GAS,Power_DEC_COGEN_OIL,Power_DEC_ADVCOGEN_GAS,Power_DEC_ADVCOGEN_H2,Power_Geothermal],
          'Energy_GWhe':[Energy_DHN_COGEN_GAS,Energy_DHN_COGEN_WOOD,Energy_DHN_COGEN_WASTE,Energy_DHN_COGEN_WET_BIOMASS,Energy_DHN_COGEN_BIO_HYDROLYSIS,Energy_DEC_COGEN_GAS,Energy_DEC_COGEN_OIL,Energy_DEC_ADVCOGEN_GAS,Energy_DEC_ADVCOGEN_H2,Energy_Geothermal],
          'LF':[LF_DHN_COGEN_GAS,LF_DHN_COGEN_WOOD,LF_DHN_COGEN_WASTE,LF_DHN_COGEN_WET_BIOMASS,LF_DHN_COGEN_BIO_HYDROLYSIS,LF_DEC_COGEN_GAS,LF_DEC_COGEN_OIL,LF_DEC_ADVCOGEN_GAS,LF_DEC_ADVCOGEN_H2,LF_Geothermal],
          'Cost_maint_M€/GW/y':[DHN_COGEN_GAS_C_maint,DHN_COGEN_WOOD_C_maint,DHN_COGEN_WASTE_C_maint,DHN_COGEN_WET_BIOMASS_C_maint,DHN_COGEN_BIO_HYDROLYSIS_C_maint,DEC_COGEN_GAS_C_maint,DEC_COGEN_OIL_C_maint,DEC_ADVCOGEN_GAS_C_maint,DEC_ADVCOGEN_H2_C_maint,GEOTHERMAL_C_maint],
          'Cost_op_M€/GWhe':[DHN_COGEN_GAS_C_op,DHN_COGEN_WOOD_C_op,DHN_COGEN_WASTE_C_op,DHN_COGEN_WET_BIOMASS_C_op,DHN_COGEN_BIO_HYDROLYSIS_C_op,DEC_COGEN_GAS_C_op,DEC_COGEN_OIL_C_op,DEC_ADVCOGEN_GAS_C_op,DEC_ADVCOGEN_H2_C_op,GEOTHERMAL_C_op],
          # 'MTTF':[],
          # 'MTTR':[]
          }


# 'PowerHydro_GWe':[Power_HYDRO_RIVER],
# 'LF_HYDRO_RIVER':[LF_HYDRO_RIVER],
# 'Power_Geothermal_GWe':[Power_Geothermal],
# 'LF_Geothermal':[LF_Geothermal]

DistGen_df = pd.DataFrame(DistGen)

######################################RES######################################

Power_WIND_OFFSHORE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'WIND_OFFSHORE')].iloc[0][' f'])#*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='WIND_OFFSHORE'].iloc[0]['ELECTRICITY'])*1e3 #GW to MW

Res = {'RES':[1],
       'Node':['STEVN'],
       'Pmax_GWe':[Power_WIND_OFFSHORE]}

Res_df= pd.DataFrame(Res)

################################IMPORT############################################

Imp_Emax_year=float(resources_breakdown_df[ (resources_breakdown_df["Name"] == 'ELECTRICITY')].iloc[0]['Used'])#*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='WIND_OFFSHORE'].iloc[0]['ELECTRICITY'])
Imp_Pmax_year=float(layer_ELEC['ELECTRICITY'].max())
Imp_Elec_Cost=float(Resources_df[ (Resources_df["parameter name"] == 'ELECTRICITY')].iloc[0]['c_op'])

Imp_Data={'Imp_Emax_GWhe':[Imp_Emax_year],
              'Imp_Pmax_GWe':[Imp_Pmax_year],
              'Price_Meuro/GWh':[Imp_Elec_Cost]
              }

Imp_Data_df = pd.DataFrame(Imp_Data)
ImportLines_df=pd.read_csv("PreData/ImportLines.txt", delimiter="\t")

##################################PHS##########################################


PHS_Capacity=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'PHS')].iloc[0][' f']) #kWh
 #GW #Ajouter 

if layer_ELEC['PHS_Pout'].max()>=layer_ELEC['PHS_Pin'].max():
    PHS_PowerMax=layer_ELEC['PHS_Pout'].max()
else:
    PHS_PowerMax=layer_ELEC['PHS_Pin'].max()

if type(PHS_PowerMax)==str: 

    if PHS_PowerMax[0]=='0':
        PHS_PowerMax=float(PHS_PowerMax)
        
    else:
        PHS_PowerMax=float(PHS_PowerMax.replace(".", ""))

else:
    
    PHS_PowerMax=float(PHS_PowerMax)


coefPHS_P_COO=0.89
coefPHS_P_GOUY=0.11

coefPHS_C_COO=0.9
coefPHS_C_GOUY=0.1


PHS_P_COO=coefPHS_P_COO*PHS_PowerMax
PHS_P_GOUY=coefPHS_P_GOUY*PHS_PowerMax

PHS_C_COO=coefPHS_C_COO*PHS_Capacity
PHS_C_GOUY=coefPHS_C_GOUY*PHS_Capacity

eff_in_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Storage_eff_in.csv", delimiter=";")
eff_out_df=pd.read_csv("C:/Users/antoi/2023_EnergyScope-ES_MECA2675/Data/2030/Storage_eff_out.csv", delimiter=";")

eff_pump=float(eff_in_df[ (eff_in_df["param storage_eff_in :"] == 'PHS')].iloc[0]['ELECTRICITY'])
eff_turb=float(eff_out_df[ (eff_out_df["param storage_eff_out:"] == 'PHS')].iloc[0]['ELECTRICITY'])

Phs= {'PHS':[1,2],
      'Node':['COO','GOUY'],
      'Pmax_GWe':[PHS_P_COO,PHS_P_GOUY],
      'Emax_GWhe':[PHS_C_COO,PHS_C_GOUY],
      'eff_pump':[eff_pump,eff_pump],
      'eff_turb':[eff_turb,eff_turb]} #voir note

Phs_df= pd.DataFrame(Phs)


##################################Batt#########################################Share_Batt_Li_Large, Share_Batt_Li_Small


Batt_LI_Capacity=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'BATT_LI')].iloc[0][' f'])#*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='BATT_LI'].iloc[0]['ELECTRICITY'])

Batt_LI_PowerMax=layer_ELEC['BATT_LI_Pout'].max()

if layer_ELEC['BATT_LI_Pout'].max()>=layer_ELEC['BATT_LI_Pin'].max():
    PHS_PowerMax=layer_ELEC['BATT_LI_Pout'].max()
else:
    PHS_PowerMax=layer_ELEC['BATT_LI_Pin'].max()


if type(Batt_LI_PowerMax)== str:
 
   if Batt_LI_PowerMax[0]=='0':
        Batt_LI_PowerMax=float(Batt_LI_PowerMax)
        
   else:
        Batt_LI_PowerMax=float(Batt_LI_PowerMax.replace(".", ""))
        
else:
    
    Batt_LI_PowerMax=float(Batt_LI_PowerMax)


Batt_LI_PowerMaxLarge=Share_LargeScaleP*Batt_LI_PowerMax
Batt_LI_CapacityLarge=Share_LargeScaleC*Batt_LI_Capacity

Batt_LI_PowerMaxSmall=Share_SmallScaleP*Batt_LI_PowerMax
Batt_LI_CapacitySmall=Share_SmallScaleC*Batt_LI_Capacity


eff_batt_in=float(eff_in_df[ (eff_in_df["param storage_eff_in :"] == 'BATT_LI')].iloc[0]['ELECTRICITY'])
eff_batt_out=float(eff_out_df[ (eff_out_df["param storage_eff_out:"] == 'BATT_LI')].iloc[0]['ELECTRICITY'])

if abs(Batt_LI_PowerMax)<powerSeuil:
    Batt_LI_PowerMaxLarge=0
    Batt_LI_CapacityLarge=0
    Batt_LI_PowerMaxSmall=0
    Batt_LI_CapacitySmall=0
    print('Batt_LI OFF')
else:
    print('Batt_LI ON') 

Batt={#'Batt':[],
      #'Node':[],
      'Pmax_Large_GWe':[Batt_LI_PowerMaxLarge],
      'Emax_Large_GWhe':[Batt_LI_CapacityLarge],
      'Pmax_Small_GWe':[Batt_LI_PowerMaxSmall],
      'Emax_Small_GWhe':[Batt_LI_CapacitySmall],
      'eff_batt_in':[eff_batt_in],
      'eff_batt_out':[eff_batt_out]
      } #Voir note

Batt_df=pd.DataFrame(Batt)


###############################################################################
###################################LOAD########################################
###############################################################################


#################################HUB Indu######################################

Pow_ATM_CCS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'ATM_CCS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='ATM_CCS'].iloc[0]['ELECTRICITY'])
Pow_INDUSTRY_CCS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'INDUSTRY_CCS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='INDUSTRY_CCS'].iloc[0]['ELECTRICITY'])

Energy_ATM_CCS=float(year_balance_df[ (year_balance_df["Tech"] == ' ATM_CCS ')].iloc[0]['ELECTRICITY'])
Energy_INDUSTRY_CCS=float(year_balance_df[ (year_balance_df["Tech"] == ' INDUSTRY_CCS ')].iloc[0]['ELECTRICITY'])

if abs(Pow_ATM_CCS)<powerSeuil:
    Pow_ATM_CCS=0
    Energy_ATM_CCS=0
    print('ATM_CCS OFF')   
else:
    print('ATM_CCS ON') 
    
if abs(Pow_INDUSTRY_CCS)<powerSeuil:
    Pow_INDUSTRY_CCS=0
    Energy_INDUSTRY_CCS=0
    print('INDUSTRY_CCS OFF')
        
else:
    print('INDUSTRY_CCS ON')    

CCS={'Pow_ATM_CCS_GWe':[abs(Pow_ATM_CCS)], #Share_Hub
     'Pow_INDUSTRY_CCS_GWe':[abs(Pow_INDUSTRY_CCS)], #Share_CCS_Industry
     'Energy_ATM_CCS_GWhe':[abs(Energy_ATM_CCS)],
     'Energy_INDUSTRY_CCS_GWhe':[abs(Energy_INDUSTRY_CCS)]
     } # /!\ Vérifier les unités


CCS_df=pd.DataFrame(CCS)


###############################Profile TRAM####################################

TRAM=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'TRAMWAY_TROLLEY')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='TRAMWAY_TROLLEY'].iloc[0]['ELECTRICITY'])
#layer_ELEC['TRAMWAY_TROLLEY'].to_csv('ProfileTRAM.txt','\t', index=False)

ProfileTRAM=np.zeros(24)



for i in range(0,24):
    ProfileTRAM[i]=abs(layer_ELEC['TRAMWAY_TROLLEY'][i])
 
    
# ProfileTRAM_df=pd.DataFrame(ProfileTRAM)
# ProfileTRAM_df.columns = ["Profile"]
# ProfileTRAM_df.to_csv('ProfileTRAM.txt','\t', index=False)  

np.savetxt('ProfileTRAM.txt', ProfileTRAM, fmt='%.6f')


################################ProfileBEV#####################################ShareCar

ProfileCAR_BEV=np.zeros(24)

for i in range(0,24):
    ProfileCAR_BEV[i]=abs(layer_ELEC['CAR_BEV'][i])
     
# ProfileCAR_BEV_df=pd.DataFrame(ProfileCAR_BEV)
# ProfileCAR_BEV_df.columns = ["Profile"]
# ProfileCAR_BEV_df.to_csv('ProfileCAR_BEV.txt','\t', index=False)  

np.savetxt('ProfileCAR_BEV.txt', ProfileCAR_BEV, fmt='%.6f')

###############################ProfilePHEV#####################################ShareCar

ProfileCAR_PHEV=np.zeros(24)

for i in range(0,24):
    ProfileCAR_PHEV[i]=abs(layer_ELEC['CAR_PHEV'][i])
     
# ProfileCAR_PHEV_df=pd.DataFrame(ProfileCAR_PHEV)
# ProfileCAR_PHEV_df.columns = ["Profile"]
# ProfileCAR_PHEV_df.to_csv('ProfileCAR_PHEV.txt','\t', index=False)

np.savetxt('ProfileCAR_PHEV.txt', ProfileCAR_PHEV, fmt='%.6f')
#################################Freight#######################################

Day_TRUCK_ELEC=layer_ELEC['TRUCK_ELEC'].iloc[2] #ShareTruck
Day_TRAIN_FREIGHT=layer_ELEC['TRAIN_FREIGHT'].iloc[2] #Share_TrainFreight

if abs(Day_TRUCK_ELEC)<powerSeuil:
    Day_TRUCK_ELEC=0
    print('TRUCK_ELEC OFF')
else:
    print('TRUCK_ELEC ON')
    
if abs(Day_TRAIN_FREIGHT)<powerSeuil:
    Day_TRAIN_FREIGHT=0
    print('TRAIN_FREIGHT OFF')
else:
    print('TRAIN_FREIGHT ON')

FreightELEC={'Demand_TRUCK_ELEC_ELEC_GWe':[abs(Day_TRUCK_ELEC)],
       'Demand_TRAIN_FREIGHT_ELEC_GWe':[abs(Day_TRAIN_FREIGHT)]
       }

Freight_df=pd.DataFrame(FreightELEC)

############################Profile TRAIN_PUB################################## Share_TrainPass

ProfileTRAIN_PUB=np.zeros(24)

for i in range(0,24):
    ProfileTRAIN_PUB[i]=abs(layer_ELEC['TRAIN_PUB'][i])
 
    
# ProfileTRAIN_PUB_df=pd.DataFrame(ProfileTRAM)
# ProfileTRAIN_PUB_df.columns = ["Profile"]
# ProfileTRAIN_PUB_df.to_csv('ProfileTRAIN_PUB.txt','\t', index=False) 

np.savetxt('ProfileTRAIN_PUB.txt', ProfileTRAIN_PUB, fmt='%.6f')

##########################IndustrialProcess#################################### Share_HubELEC

Power_BIO_HYDROLYSIS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'BIO_HYDROLYSIS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='BIO_HYDROLYSIS'].iloc[0]['ELECTRICITY'])
Power_PYROLYSIS_TO_LFO=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'PYROLYSIS_TO_LFO')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='PYROLYSIS_TO_LFO'].iloc[0]['ELECTRICITY'])
Power_PYROLYSIS_TO_FUELS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'PYROLYSIS_TO_FUELS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='PYROLYSIS_TO_FUELS'].iloc[0]['ELECTRICITY'])

Power_SYN_METHANOLATION=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'SYN_METHANOLATION')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='SYN_METHANOLATION'].iloc[0]['ELECTRICITY'])
Power_METHANE_TO_METHANOL=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'METHANE_TO_METHANOL')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='METHANE_TO_METHANOL'].iloc[0]['ELECTRICITY'])
Power_BIOMASS_TO_METHANOL=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'BIOMASS_TO_METHANOL')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='BIOMASS_TO_METHANOL'].iloc[0]['ELECTRICITY'])
Power_HABER_BOSCH=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'HABER_BOSCH')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='HABER_BOSCH'].iloc[0]['ELECTRICITY'])
Power_OIL_TO_HVC=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'OIL_TO_HVC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='OIL_TO_HVC'].iloc[0]['ELECTRICITY'])
Power_GAS_TO_HVC=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'GAS_TO_HVC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='GAS_TO_HVC'].iloc[0]['ELECTRICITY'])
Power_BIOMASS_TO_HVC=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'BIOMASS_TO_HVC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='BIOMASS_TO_HVC'].iloc[0]['ELECTRICITY'])

Energy_BIO_HYDROLYSIS=float(year_balance_df[ (year_balance_df["Tech"] == ' BIO_HYDROLYSIS ')].iloc[0]['ELECTRICITY'])
Energy_PYROLYSIS_TO_LFO=float(year_balance_df[ (year_balance_df["Tech"] == ' PYROLYSIS_TO_LFO ')].iloc[0]['ELECTRICITY'])
Energy_PYROLYSIS_TO_FUELS=float(year_balance_df[ (year_balance_df["Tech"] == ' PYROLYSIS_TO_FUELS ')].iloc[0]['ELECTRICITY'])

Energy_SYN_METHANOLATION=float(year_balance_df[ (year_balance_df["Tech"] == ' SYN_METHANOLATION ')].iloc[0]['ELECTRICITY'])
Energy_METHANE_TO_METHANOL=float(year_balance_df[ (year_balance_df["Tech"] == ' METHANE_TO_METHANOL ')].iloc[0]['ELECTRICITY'])
Energy_BIOMASS_TO_METHANOL=float(year_balance_df[ (year_balance_df["Tech"] == ' BIOMASS_TO_METHANOL ')].iloc[0]['ELECTRICITY'])
Energy_HABER_BOSCH=float(year_balance_df[ (year_balance_df["Tech"] == ' HABER_BOSCH ')].iloc[0]['ELECTRICITY'])
Energy_OIL_TO_HVC=float(year_balance_df[ (year_balance_df["Tech"] == ' OIL_TO_HVC ')].iloc[0]['ELECTRICITY'])
Energy_GAS_TO_HVC=float(year_balance_df[ (year_balance_df["Tech"] == ' GAS_TO_HVC ')].iloc[0]['ELECTRICITY'])
Energy_BIOMASS_TO_HVC=float(year_balance_df[ (year_balance_df["Tech"] == ' BIOMASS_TO_HVC ')].iloc[0]['ELECTRICITY'])



Power_Process=Power_BIO_HYDROLYSIS+Power_PYROLYSIS_TO_LFO+Power_PYROLYSIS_TO_FUELS
Load_Process=Power_SYN_METHANOLATION+Power_METHANE_TO_METHANOL+Power_BIOMASS_TO_METHANOL+Power_HABER_BOSCH+Power_OIL_TO_HVC+Power_GAS_TO_HVC+Power_BIOMASS_TO_HVC

Year_Power_Process=Energy_BIO_HYDROLYSIS+Energy_PYROLYSIS_TO_LFO+Energy_PYROLYSIS_TO_FUELS
Year_Load_Process=Energy_SYN_METHANOLATION+Energy_METHANE_TO_METHANOL+Energy_BIOMASS_TO_METHANOL+Energy_HABER_BOSCH+Energy_OIL_TO_HVC+Energy_GAS_TO_HVC+Energy_BIOMASS_TO_HVC


if abs(Power_Process)<powerSeuil:
    Power_Process=0
    Year_Power_Process=0
    print('Power_Process OFF')
        
else:
    print('Power_Process ON')
    
if abs(Load_Process)<powerSeuil:
    Load_Process=0
    Year_Load_Process=0
    print('Load_Process OFF')    
else:
    print('Load_Process ON')    

IndustrialProcess_ELEC={'Power_Process_GWe':[abs(Power_Process)],
                   'Load_Process_GWe':[abs(Load_Process)],
                   'Year_Power_Process_GWhe':[abs(Year_Power_Process)],
                   'Year_Load_Process_GWhe':[abs(Year_Load_Process)]
                   }

IndustrialProcess_ELEC_df=pd.DataFrame(IndustrialProcess_ELEC)

###############################Electrolyzer#################################### /!\ FAIRE SHARE !!!!

PowerElectrolyzer=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'H2_ELECTROLYSIS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='H2_ELECTROLYSIS'].iloc[0]['ELECTRICITY']))
#layer_ELEC['H2_ELECTROLYSIS'].min()
Yearly_EnergyElectrolyzer=float(year_balance_df[ (year_balance_df["Tech"] == ' H2_ELECTROLYSIS ')].iloc[0]['ELECTRICITY'])

if abs(PowerElectrolyzer)<powerSeuil:
    PowerElectrolyzer=0
    Yearly_EnergyElectrolyzer=0
    print('Electrolyzer OFF')
        
else:
    print('Electrolyzer ON') 

Electrolyzer_ELEC={'PowerElectrolyzer_GWe':[abs(PowerElectrolyzer)],
                   'Yearly_EnergyElectrolyzer_GWhe':[abs(Yearly_EnergyElectrolyzer)]
                    }

Electrolyzer_ELEC_df=pd.DataFrame(Electrolyzer_ELEC)



############################IndustrialHeat##################################### Share_HubELEC 

Power_IND_DIRECT_ELEC=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'IND_DIRECT_ELEC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='IND_DIRECT_ELEC'].iloc[0]['ELECTRICITY']))
#layer_ELEC['IND_DIRECT_ELEC'].min()
Yearly_Energy_IND_DIRECT_ELEC=float(year_balance_df[ (year_balance_df["Tech"] == ' IND_DIRECT_ELEC ')].iloc[0]['ELECTRICITY'])

if abs(Power_IND_DIRECT_ELEC)<powerSeuil:
    Power_IND_DIRECT_ELEC=0
    Yearly_Energy_IND_DIRECT_ELEC=0
    print('IND_DIRECT_ELEC OFF')   
else:
    print('IND_DIRECT_ELEC ON') 

IndustrialHeat={'Power_IND_DIRECT_ELEC_GWe':[abs(Power_IND_DIRECT_ELEC)],
                'Yearly_Energy_IND_DIRECT_ELEC_GWhe':[abs(Yearly_Energy_IND_DIRECT_ELEC)]}

IndustrialHeat_df=pd.DataFrame(IndustrialHeat)



#############################ResidentialHeat###################################

Power_DEC_HP_ELEC=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_HP_ELEC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_HP_ELEC'].iloc[0]['ELECTRICITY']))
#layer_ELEC['DEC_HP_ELEC'].min()
Power_DHN_HP_ELEC=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DHN_HP_ELEC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DHN_HP_ELEC'].iloc[0]['ELECTRICITY']))
#layer_ELEC['DHN_HP_ELEC'].min()
Power_DEC_DIRECT_ELEC=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_DIRECT_ELEC')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_DIRECT_ELEC'].iloc[0]['ELECTRICITY']))
#layer_ELEC['DEC_DIRECT_ELEC'].min()

##################################Profile######################################

Profile_END_USE_ELEC=np.zeros(8760)
Profile_DEC_HP_ELEC=np.zeros(8760)
Profile_DHN_HP_ELEC=np.zeros(8760)
Profile_DEC_DIRECT_ELEC=np.zeros(8760)
Profile_HYDRO_RIVER=np.zeros(8760)

##########################################################################
Profile_IND_COGEN_GAS=np.zeros(8760)
Profile_IND_COGEN_WOOD=np.zeros(8760)
Profile_IND_COGEN_WASTE=np.zeros(8760)
Profile_CHP=np.zeros(8760)
# Profile_CHP_jan=np.zeros(744)

# Profile_CHP_aug=np.zeros(744)

DEC_HP_ELEC_jan=np.zeros(744)
DEC_HP_ELEC_fev=np.zeros(672)
DEC_HP_ELEC_mar=np.zeros(744)
DEC_HP_ELEC_apr=np.zeros(720)
DEC_HP_ELEC_may=np.zeros(744)
DEC_HP_ELEC_jun=np.zeros(720)
DEC_HP_ELEC_jul=np.zeros(744)
DEC_HP_ELEC_aug=np.zeros(744)
DEC_HP_ELEC_sep=np.zeros(720)
DEC_HP_ELEC_oct=np.zeros(744)
DEC_HP_ELEC_nov=np.zeros(720)
DEC_HP_ELEC_dec=np.zeros(744)

CHP_jan=np.zeros(744)
CHP_fev=np.zeros(672)
CHP_mar=np.zeros(744)
CHP_apr=np.zeros(720)
CHP_may=np.zeros(744)
CHP_jun=np.zeros(720)
CHP_jul=np.zeros(744)
CHP_aug=np.zeros(744)
CHP_sep=np.zeros(720)
CHP_oct=np.zeros(744)
CHP_nov=np.zeros(720)
CHP_dec=np.zeros(744)

DHN_HP_ELEC_jan=np.zeros(744)
DHN_HP_ELEC_fev=np.zeros(672)
DHN_HP_ELEC_mar=np.zeros(744)
DHN_HP_ELEC_apr=np.zeros(720)
DHN_HP_ELEC_may=np.zeros(744)
DHN_HP_ELEC_jun=np.zeros(720)
DHN_HP_ELEC_jul=np.zeros(744)
DHN_HP_ELEC_aug=np.zeros(744)
DHN_HP_ELEC_sep=np.zeros(720)
DHN_HP_ELEC_oct=np.zeros(744)
DHN_HP_ELEC_nov=np.zeros(720)
DHN_HP_ELEC_dec=np.zeros(744)

DEC_DIRECT_ELEC_jan=np.zeros(744)
DEC_DIRECT_ELEC_fev=np.zeros(672)
DEC_DIRECT_ELEC_mar=np.zeros(744)
DEC_DIRECT_ELEC_apr=np.zeros(720)
DEC_DIRECT_ELEC_may=np.zeros(744)
DEC_DIRECT_ELEC_jun=np.zeros(720)
DEC_DIRECT_ELEC_jul=np.zeros(744)
DEC_DIRECT_ELEC_aug=np.zeros(744)
DEC_DIRECT_ELEC_sep=np.zeros(720)
DEC_DIRECT_ELEC_oct=np.zeros(744)
DEC_DIRECT_ELEC_nov=np.zeros(720)
DEC_DIRECT_ELEC_dec=np.zeros(744)





print(Profile_END_USE_ELEC[0])
#for i in range(1,8761):
for i in range(0,8760): 
#for i in range(0,500):
    #print(i)
    
    #a=TDtoD_df[(TDtoD_df["Hour"]==i)].iloc[0]['Td'] # 
    
    a=TDtoD_df['Td'].iloc[i] #
    #print(a)
    #b=TDtoD_df[(TDtoD_df["Hour"]==i)].iloc[0]['Time']
    b=TDtoD_df['Time'].iloc[i]
    
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'])
    Profile_END_USE_ELEC[i]=abs(x)
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'])
    Profile_DEC_HP_ELEC[i]=abs(x)
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'])
    Profile_DHN_HP_ELEC[i]=abs(x)
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'])
    Profile_DEC_DIRECT_ELEC[i]=abs(x)  
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'])
    Profile_HYDRO_RIVER[i]=abs(x)  
    ##################################################################################################
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['IND_COGEN_GAS'])
    Profile_IND_COGEN_GAS[i]=x
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['IND_COGEN_WOOD'])
    Profile_IND_COGEN_WOOD[i]=x
    x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['IND_COGEN_WASTE'])
    Profile_IND_COGEN_WASTE[i]=x

    Profile_CHP[i]=Profile_IND_COGEN_GAS[i]+Profile_IND_COGEN_WOOD[i]+Profile_IND_COGEN_WASTE[i]
    

DEC_HP_ELEC_jan=sum(Profile_DEC_HP_ELEC[0:745])
DEC_HP_ELEC_feb=sum(Profile_DEC_HP_ELEC[745:1417])
DEC_HP_ELEC_mar=sum(Profile_DEC_HP_ELEC[1417:2161])
DEC_HP_ELEC_apr=sum(Profile_DEC_HP_ELEC[2161:2881])
DEC_HP_ELEC_may=sum(Profile_DEC_HP_ELEC[2881:3625])
DEC_HP_ELEC_jun=sum(Profile_DEC_HP_ELEC[3625:4345])
DEC_HP_ELEC_jul=sum(Profile_DEC_HP_ELEC[4345:5089])
DEC_HP_ELEC_aug=sum(Profile_DEC_HP_ELEC[5089:5833])
DEC_HP_ELEC_sep=sum(Profile_DEC_HP_ELEC[5833:6553])
DEC_HP_ELEC_oct=sum(Profile_DEC_HP_ELEC[6553:7297])
DEC_HP_ELEC_nov=sum(Profile_DEC_HP_ELEC[7297:8017])
DEC_HP_ELEC_dec=sum(Profile_DEC_HP_ELEC[8017:8761])


DHN_HP_ELEC_jan=sum(Profile_DHN_HP_ELEC[0:745])
DHN_HP_ELEC_feb=sum(Profile_DHN_HP_ELEC[745:1417])
DHN_HP_ELEC_mar=sum(Profile_DHN_HP_ELEC[1417:2161])
DHN_HP_ELEC_apr=sum(Profile_DHN_HP_ELEC[2161:2881])
DHN_HP_ELEC_may=sum(Profile_DHN_HP_ELEC[2881:3625])
DHN_HP_ELEC_jun=sum(Profile_DHN_HP_ELEC[3625:4345])
DHN_HP_ELEC_jul=sum(Profile_DHN_HP_ELEC[4345:5089])
DHN_HP_ELEC_aug=sum(Profile_DHN_HP_ELEC[5089:5833])
DHN_HP_ELEC_sep=sum(Profile_DHN_HP_ELEC[5833:6553])
DHN_HP_ELEC_oct=sum(Profile_DHN_HP_ELEC[6553:7297])
DHN_HP_ELEC_nov=sum(Profile_DHN_HP_ELEC[7297:8017])
DHN_HP_ELEC_dec=sum(Profile_DHN_HP_ELEC[8017:8761])


DEC_DIRECT_ELEC_jan=sum(Profile_DEC_DIRECT_ELEC[0:745])
DEC_DIRECT_ELEC_feb=sum(Profile_DEC_DIRECT_ELEC[745:1417])
DEC_DIRECT_ELEC_mar=sum(Profile_DEC_DIRECT_ELEC[1417:2161])
DEC_DIRECT_ELEC_apr=sum(Profile_DEC_DIRECT_ELEC[2161:2881])
DEC_DIRECT_ELEC_may=sum(Profile_DEC_DIRECT_ELEC[2881:3625])
DEC_DIRECT_ELEC_jun=sum(Profile_DEC_DIRECT_ELEC[3625:4345])
DEC_DIRECT_ELEC_jul=sum(Profile_DEC_DIRECT_ELEC[4345:5089])
DEC_DIRECT_ELEC_aug=sum(Profile_DEC_DIRECT_ELEC[5089:5833])
DEC_DIRECT_ELEC_sep=sum(Profile_DEC_DIRECT_ELEC[5833:6553])
DEC_DIRECT_ELEC_oct=sum(Profile_DEC_DIRECT_ELEC[6553:7297])
DEC_DIRECT_ELEC_nov=sum(Profile_DEC_DIRECT_ELEC[7297:8017])
DEC_DIRECT_ELEC_dec=sum(Profile_DEC_DIRECT_ELEC[8017:8761])



CHP_jan=sum(Profile_CHP[0:745])
CHP_feb=sum(Profile_CHP[745:1417])
CHP_mar=sum(Profile_CHP[1417:2161])
CHP_apr=sum(Profile_CHP[2161:2881])
CHP_may=sum(Profile_CHP[2881:3625])
CHP_jun=sum(Profile_CHP[3625:4345])
CHP_jul=sum(Profile_CHP[4345:5089])
CHP_aug=sum(Profile_CHP[5089:5833])
CHP_sep=sum(Profile_CHP[5833:6553])
CHP_oct=sum(Profile_CHP[6553:7297])
CHP_nov=sum(Profile_CHP[7297:8017])
CHP_dec=sum(Profile_CHP[8017:8761])





#     if i<744:
#         Profile_CHP_jan[i]=Profile_CHP[i]
        
#     if i>5088 and i<5832:
#         Profile_CHP_aug[i-5088]=Profile_CHP[i]


# LF_CHP_jan=sum(Profile_CHP_jan)/(PowerCHP*744)
# LF_CHP_aug=sum(Profile_CHP_aug)/(PowerCHP*744)

# print('LF_CHP_jan')
# print(LF_CHP_jan)
# print('LF_CHP_aug')
# print(LF_CHP_aug)
    
# plt.plot(rofile_CHP)
# #plt.figure().set_figwidth(15)
# #plt.plot(DHN_HP_ELEC)
# plt.rcParams["figure.figsize"] = (75,25)
# plt.xlabel('Hour [h]')
# plt.ylabel('Power [GW] ')
# plt.show()    
#     if type(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'])== str:


#         if layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'][1]== '0' :
#             print('str')
#             #z=0
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'])
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_END_USE_ELEC[i-1]=abs(x)
#         else:
        
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'].replace(".", ""))
            
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_END_USE_ELEC[i-1]=abs(x)
            
            
#     else:
        
#         x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['END_USE'])
#         Profile_END_USE_ELEC[i-1]=abs(x)
#     #print(Profile_END_USE_ELEC[i])    
# #########################################################################################################################################    
    
#     if type(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'])== str:
#         print('str')

#         if layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'][1]== '0' :
#             #z=0
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'])
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DEC_HP_ELEC[i-1]=abs(x)
#         else:
        
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'].replace(".", ""))
            
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DEC_HP_ELEC[i-1]=abs(x)
            
            
#     else:
        
#         x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_HP_ELEC'])
#         Profile_DEC_HP_ELEC[i-1]=abs(x)

# ######################################################################################################################################### 
    
#     if type(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'])== str:
#         print('str')

#         if layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'][1]== '0' :
#             #z=0
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'])
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DHN_HP_ELEC[i-1]=abs(x)
#         else:
        
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'].replace(".", ""))
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DHN_HP_ELEC[i-1]=abs(x)
            
            
#     else:
        
#         x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DHN_HP_ELEC'])
#         Profile_DHN_HP_ELEC[i-1]=abs(x)    
    
    
# ######################################################################################################################################### 
    
#     if type(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'])== str:
#         print('str')

#         if layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'][1]== '0' :
#             #z=0
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'])
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DEC_DIRECT_ELEC[i-1]=abs(x)
#         else:
        
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'].replace(".", ""))
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_DEC_DIRECT_ELEC[i-1]=abs(x)
            
            
#     else:
        
#         x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['DEC_DIRECT_ELEC'])
#         Profile_DEC_DIRECT_ELEC[i-1]=abs(x)    
    
# ######################################################################################################################################### 


#     if type(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'])== str:
#         print('str')

#         if layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'][1]== '0' :
#             #z=0
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'])
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_HYDRO_RIVER[i-1]=abs(x)
#         else:
        
#             x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'].replace(".", ""))
#             #Elec_Heat_DEC_jan.append(x)
#             Profile_HYDRO_RIVER[i-1]=abs(x)
            
            
#     else:
        
#         x=float(layer_ELEC[ (layer_ELEC["Td "] == a) & (layer_ELEC[" Time"] == b)].iloc[0]['HYDRO_RIVER'])
#         Profile_HYDRO_RIVER[i-1]=abs(x)
#########################################################################################################################################

# E_year_hydro= sum(Profile_HYDRO_RIVER)
# print('E_year_hydro:')
# print(E_year_hydro)
######################################################################################################################################### 


np.savetxt('Profile_END_USE_ELEC.txt', Profile_END_USE_ELEC, fmt='%.6f')
 
# np.savetxt('Profile_HYDRO_RIVER.txt', Profile_HYDRO_RIVER, fmt='%.6f')    
   
if abs(Power_DEC_HP_ELEC)<powerSeuil:
    Power_DEC_HP_ELEC=0
    print('DEC_HP_ELEC OFF')
    DEC_HP_ELEC_jan=0
    DEC_HP_ELEC_feb=0
    DEC_HP_ELEC_mar=0
    DEC_HP_ELEC_apr=0
    DEC_HP_ELEC_may=0
    DEC_HP_ELEC_jun=0
    DEC_HP_ELEC_jul=0
    DEC_HP_ELEC_aug=0
    DEC_HP_ELEC_sep=0
    DEC_HP_ELEC_oct=0
    DEC_HP_ELEC_nov=0
    DEC_HP_ELEC_dec=0

else:
    print('DEC_HP_ELEC ON')
    
if abs(Power_DHN_HP_ELEC)<powerSeuil:
    Power_DHN_HP_ELEC=0
    print('DHN_HP_ELEC OFF')
    DHN_HP_ELEC_jan=0
    DHN_HP_ELEC_feb=0
    DHN_HP_ELEC_mar=0
    DHN_HP_ELEC_apr=0
    DHN_HP_ELEC_may=0
    DHN_HP_ELEC_jun=0
    DHN_HP_ELEC_jul=0
    DHN_HP_ELEC_aug=0
    DHN_HP_ELEC_sep=0
    DHN_HP_ELEC_oct=0
    DHN_HP_ELEC_nov=0
    DHN_HP_ELEC_dec=0
else:
    print('DHN_HP_ELEC ON')
    
if abs(Power_DEC_DIRECT_ELEC)<powerSeuil:
    Power_DEC_DIRECT_ELEC=0
    print('DEC_DIRECT_ELEC OFF')
    DEC_DIRECT_ELEC_jan=0
    DEC_DIRECT_ELEC_feb=0
    DEC_DIRECT_ELEC_mar=0
    DEC_DIRECT_ELEC_apr=0
    DEC_DIRECT_ELEC_may=0
    DEC_DIRECT_ELEC_jun=0
    DEC_DIRECT_ELEC_jul=0
    DEC_DIRECT_ELEC_aug=0
    DEC_DIRECT_ELEC_sep=0
    DEC_DIRECT_ELEC_oct=0
    DEC_DIRECT_ELEC_nov=0
    DEC_DIRECT_ELEC_dec=0
else:
    print('DEC_DIRECT_ELEC ON')    

ResidentialHeat={'Technology':['DEC_HP_ELEC','DHN_HP_ELEC','DEC_DIRECT_ELEC'],
                 'Power_GWe':[abs(Power_DEC_HP_ELEC),abs(Power_DHN_HP_ELEC),abs(Power_DEC_DIRECT_ELEC)],
                 'E_jan_GWhe':[DEC_HP_ELEC_jan,DHN_HP_ELEC_jan,DEC_DIRECT_ELEC_jan],
                 'E_feb_GWhe':[DEC_HP_ELEC_feb,DHN_HP_ELEC_feb,DEC_DIRECT_ELEC_feb],
                 'E_mar_GWhe':[DEC_HP_ELEC_mar,DHN_HP_ELEC_mar,DEC_DIRECT_ELEC_mar],
                 'E_apr_GWhe':[DEC_HP_ELEC_apr,DHN_HP_ELEC_apr,DEC_DIRECT_ELEC_apr],
                 'E_may_GWhe':[DEC_HP_ELEC_may,DHN_HP_ELEC_may,DEC_DIRECT_ELEC_may],
                 'E_jun_GWhe':[DEC_HP_ELEC_jun,DHN_HP_ELEC_jun,DEC_DIRECT_ELEC_jun],
                 'E_jul_GWhe':[DEC_HP_ELEC_jul,DHN_HP_ELEC_jul,DEC_DIRECT_ELEC_jul],
                 'E_aug_GWhe':[DEC_HP_ELEC_aug,DHN_HP_ELEC_aug,DEC_DIRECT_ELEC_aug],
                 'E_sep_GWhe':[DEC_HP_ELEC_sep,DHN_HP_ELEC_sep,DEC_DIRECT_ELEC_sep],
                 'E_oct_GWhe':[DEC_HP_ELEC_oct,DHN_HP_ELEC_oct,DEC_DIRECT_ELEC_oct],
                 'E_nov_GWhe':[DEC_HP_ELEC_nov,DHN_HP_ELEC_nov,DEC_DIRECT_ELEC_nov],
                 'E_dec_GWhe':[DEC_HP_ELEC_dec,DHN_HP_ELEC_dec,DEC_DIRECT_ELEC_dec]
                 
                 }

ResidentialHeat_df=pd.DataFrame(ResidentialHeat)


if PowerCHP<powerSeuil:
    LF_CHP_jan=0
    LF_CHP_feb=0
    LF_CHP_mar=0
    LF_CHP_apr=0
    LF_CHP_may=0
    LF_CHP_jun=0
    LF_CHP_jul=0
    LF_CHP_aug=0
    LF_CHP_sep=0
    LF_CHP_oct=0
    LF_CHP_nov=0
    LF_CHP_dec=0
else:
    LF_CHP_jan=CHP_jan/(PowerCHP*744)
    LF_CHP_feb=CHP_feb/(PowerCHP*672)
    LF_CHP_mar=CHP_mar/(PowerCHP*744)
    LF_CHP_apr=CHP_apr/(PowerCHP*720)
    LF_CHP_may=CHP_may/(PowerCHP*744)
    LF_CHP_jun=CHP_jun/(PowerCHP*720)
    LF_CHP_jul=CHP_jul/(PowerCHP*744)
    LF_CHP_aug=CHP_aug/(PowerCHP*744)
    LF_CHP_sep=CHP_sep/(PowerCHP*720)
    LF_CHP_oct=CHP_oct/(PowerCHP*744)
    LF_CHP_nov=CHP_nov/(PowerCHP*720)
    LF_CHP_dec=CHP_dec/(PowerCHP*744)
    
 
DEC_HP_ELEC_month=[DEC_HP_ELEC_jan,DEC_HP_ELEC_feb,DEC_HP_ELEC_mar,DEC_HP_ELEC_apr,DEC_HP_ELEC_may,DEC_HP_ELEC_jun,DEC_HP_ELEC_jul,DEC_HP_ELEC_aug,DEC_HP_ELEC_sep,DEC_HP_ELEC_oct,DEC_HP_ELEC_nov,DEC_HP_ELEC_dec]
DHN_HP_ELEC_month=[DHN_HP_ELEC_jan,DHN_HP_ELEC_feb,DHN_HP_ELEC_mar,DHN_HP_ELEC_apr,DHN_HP_ELEC_may,DHN_HP_ELEC_jun,DHN_HP_ELEC_jul,DHN_HP_ELEC_aug,DHN_HP_ELEC_sep,DHN_HP_ELEC_oct,DHN_HP_ELEC_nov,DHN_HP_ELEC_dec]
DEC_DIRECT_ELEC_month=[DEC_DIRECT_ELEC_jan,DEC_DIRECT_ELEC_feb,DEC_DIRECT_ELEC_mar,DEC_DIRECT_ELEC_apr,DEC_DIRECT_ELEC_may,DEC_DIRECT_ELEC_jun,DEC_DIRECT_ELEC_jul,DEC_DIRECT_ELEC_aug,DEC_DIRECT_ELEC_sep,DEC_DIRECT_ELEC_oct,DEC_DIRECT_ELEC_nov,DEC_DIRECT_ELEC_dec]
LF_CHP_month=[LF_CHP_jan,LF_CHP_feb,LF_CHP_mar,LF_CHP_apr,LF_CHP_may,LF_CHP_jun,LF_CHP_jul,LF_CHP_aug,LF_CHP_sep,LF_CHP_oct,LF_CHP_nov,LF_CHP_dec]

np.savetxt('DEC_HP_ELEC.txt', DEC_HP_ELEC_month, fmt='%.6f')
np.savetxt('DHN_HP_ELEC.txt', DHN_HP_ELEC_month, fmt='%.6f')
np.savetxt('DEC_DIRECT_ELEC.txt', DEC_DIRECT_ELEC_month, fmt='%.6f') 
np.savetxt('LF_CHP.txt', LF_CHP_month, fmt='%.6f')  
       
Energy_CHP={'Month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            #'E_GWhe':[CHP_jan,CHP_feb,CHP_mar,CHP_apr,CHP_may,CHP_jun,CHP_jul,CHP_aug,CHP_sep,CHP_oct,CHP_nov,CHP_dec]
            'LF_GWhe':[LF_CHP_jan,LF_CHP_feb,LF_CHP_mar,LF_CHP_apr,LF_CHP_may,LF_CHP_jun,LF_CHP_jul,LF_CHP_aug,LF_CHP_sep,LF_CHP_oct,LF_CHP_nov,LF_CHP_dec]
            }
Energy_CHP_df=pd.DataFrame(Energy_CHP)
###############################################################################
#################################HYDROGEN######################################
###############################################################################


#H2Buses#######################################################################

#H2Buses_df=pd.read_csv("PreData/H2Buses.txt", delimiter="\t")

#H2Import######################################################################


PImportH2=layer_H2[ (layer_H2["Td "] == 1) & (layer_H2[" Time"] == 1)].iloc[0]['H2']
PImportH2RE=layer_H2[ (layer_H2["Td "] == 1) & (layer_H2[" Time"] == 1)].iloc[0]['H2_RE']

cost_imp_H2=float(Resources_df[ (Resources_df["parameter name"] == 'H2')].iloc[0]['c_op'])
cost_imp_h2_RE=float(Resources_df[ (Resources_df["parameter name"] == 'H2_RE')].iloc[0]['c_op'])
cost_imp_h2_mean=cost_H2


if abs(PImportH2)<powerSeuil:
    PImportH2=0
    cost_imp_H2=0
    print('PImportH2 OFF')
            
else:
    print('PImportH2 ON') 
    
if abs(PImportH2RE)<powerSeuil:
    PImportH2RE=0
    cost_imp_h2_RE=0
    print('PImportH2RE OFF')
            
else:
    print('PImportH2RE ON')     

if cost_imp_h2_RE+cost_imp_H2==0:
    cost_imp_h2_mean=0
    
else:
    print('ImportH2 ON')

H2Import={'FluxImportH2_GW_H2':[PImportH2],
          'FluxImportH2RE_GW_H2':[PImportH2RE],
          'Cost_H2_Meuro/GWh':[cost_imp_H2],
          'Cost_H2_RE_Meuro/GWh':[cost_imp_h2_RE],
          'Cost_H2_Mean_Meuro/GWh':[cost_imp_h2_mean]
          } #cst

H2Import_df= pd.DataFrame(H2Import)




#H2AMMONIA_TO_H2###############################################################

FluxH2AMMONIA_TO_H2=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'AMMONIA_TO_H2')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='AMMONIA_TO_H2'].iloc[0]['H2'])#layer_H2['H2_ELECTROLYSIS'].max()
#layer_H2['AMMONIA_TO_H2'].max()
TotalH2AMMONIA_TO_H2=float(year_balance_df[ (year_balance_df["Tech"] == ' AMMONIA_TO_H2 ')].iloc[0]['H2'])

# H2AMMONIA_TO_H2={'MaxFluxH2_GW_H2':[FluxH2AMMONIA_TO_H2],
#                  'TotalH2_GWh_H2':[TotalH2AMMONIA_TO_H2]}

#H2AMMONIA_TO_H2_df= pd.DataFrame(H2AMMONIA_TO_H2)

if abs(FluxH2AMMONIA_TO_H2)<powerSeuil:
    FluxH2AMMONIA_TO_H2=0
    TotalH2AMMONIA_TO_H2=0
    print('H2AMMONIA_TO_H2 OFF')        
else:
    print('H2AMMONIA_TO_H2 ON')

#H2Production##################################################################

FluxH2H2_ELECTROLYSIS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'H2_ELECTROLYSIS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='H2_ELECTROLYSIS'].iloc[0]['H2'])#layer_H2['H2_ELECTROLYSIS'].max()
FluxH2SMR=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'SMR')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='SMR'].iloc[0]['H2'])
#layer_H2['SMR'].max()
FluxH2H2_BIOMASS=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'H2_BIOMASS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='H2_BIOMASS'].iloc[0]['H2'])
#layer_H2['H2_BIOMASS'].max()

#*float(assets_df[ (assets_df["TECHNOLOGIES"] == 'H2_BIOMASS')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='H2_BIOMASS'].iloc[0]['H2'])


TotalH2H2_ELECTROLYSIS=float(year_balance_df[ (year_balance_df["Tech"] == ' H2_ELECTROLYSIS ')].iloc[0]['H2'])
TotalH2SMR=float(year_balance_df[ (year_balance_df["Tech"] == ' SMR ')].iloc[0]['H2'])
TotalH2H2_BIOMASS=float(year_balance_df[ (year_balance_df["Tech"] == ' H2_BIOMASS ')].iloc[0]['H2'])

if abs(FluxH2H2_ELECTROLYSIS)<powerSeuil:
    FluxH2H2_ELECTROLYSIS=0
    TotalH2H2_ELECTROLYSIS=0
    print('H2_ELECTROLYSIS OFF')
            
else:
    print('H2_ELECTROLYSIS ON')
    
if abs(FluxH2SMR)<powerSeuil:
    FluxH2SMR=0
    TotalH2SMR=0
    print('H2SMR OFF')        
else:
    print('H2SMR ON')    

if abs(FluxH2H2_BIOMASS)<powerSeuil:
    FluxH2H2_BIOMASS=0
    TotalH2H2_BIOMASS=0
    print('H2_BIOMASS OFF')        
else:
    print('H2_BIOMASS ON')

H2Production={'TechnologyH2':['H2_ELECTROLYSIS','SMR','H2_BIOMASS','AMMONIA_TO_H2'],
              'MaxFluxH2_GW_H2':[FluxH2H2_ELECTROLYSIS,FluxH2SMR,FluxH2H2_BIOMASS,FluxH2AMMONIA_TO_H2],
              'TotalH2_GWh_H2':[TotalH2H2_ELECTROLYSIS,TotalH2SMR,TotalH2H2_BIOMASS,TotalH2AMMONIA_TO_H2],
              'MTTF':[2000,2000,2000,2000],
              'MTTR':[50,50,50,50]
              }


H2Production_df=pd.DataFrame(H2Production)

#H2Mobility####################################################################

#H2Mobility={}

ProfileBUS_COACH_FC_HYBRIDH2=np.zeros(24)
ProfileCAR_FUEL_CELL=np.zeros(24)

for i in range(0,24):
    ProfileBUS_COACH_FC_HYBRIDH2[i]=abs(layer_H2['BUS_COACH_FC_HYBRIDH2'][i])
    ProfileCAR_FUEL_CELL[i]=abs(layer_H2['CAR_FUEL_CELL'][i])
    
# ProfileBUS_COACH_FC_HYBRIDH2_df=pd.DataFrame(ProfileBUS_COACH_FC_HYBRIDH2)
# ProfileBUS_COACH_FC_HYBRIDH2_df.columns = ["Profile"]
# ProfileBUS_COACH_FC_HYBRIDH2_df.to_csv('ProfileBUS_COACH_FC_HYBRIDH2.txt','\t', index=False) 

np.savetxt('ProfileBUS_COACH_FC_HYBRIDH2.txt', ProfileBUS_COACH_FC_HYBRIDH2, fmt='%.6f')
    
# ProfileCAR_FUEL_CELL_df=pd.DataFrame(ProfileCAR_FUEL_CELL)
# ProfileCAR_FUEL_CELL_df.columns = ["Profile"]
# ProfileCAR_FUEL_CELL_df.to_csv('ProfileCAR_FUEL_CELL.txt','\t', index=False)   

np.savetxt('ProfileCAR_FUEL_CELL.txt', ProfileCAR_FUEL_CELL, fmt='%.6f')



#H2Freight#####################################################################

PowerTRUCK_FUEL_CELL=layer_H2[ (layer_H2["Td "] == 1) & (layer_H2[" Time"] == 1)].iloc[0]['TRUCK_FUEL_CELL']

if abs(PowerTRUCK_FUEL_CELL)<powerSeuil:
    PowerTRUCK_FUEL_CELL=0
    print('TRUCK_FUEL_CELL OFF')           
else:
    print('TRUCK_FUEL_CELL ON') 

H2Freight={'FluxH2TRUCK_FUEL_CELL_GW':[abs(PowerTRUCK_FUEL_CELL)]}

H2Freight_df=pd.DataFrame(H2Freight)

#H2Industrial##################################################################

FluxH2SYN_METHANATION=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'SYN_METHANATION')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='SYN_METHANATION'].iloc[0]['H2']))
#abs(layer_H2['SYN_METHANATION'].min())

FluxH2SYN_METHANOLATION=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'SYN_METHANOLATION')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='SYN_METHANOLATION'].iloc[0]['H2']))
#abs(layer_H2['SYN_METHANOLATION'].min())
FluxH2HABER_BOSCH=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'HABER_BOSCH')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='HABER_BOSCH'].iloc[0]['H2']))
#abs(layer_H2['HABER_BOSCH'].min())

TotalH2SYN_METHANATION=abs(float(year_balance_df[ (year_balance_df["Tech"] == ' SYN_METHANATION ')].iloc[0]['H2']))
TotalH2SYN_METHANOLATION=abs(float(year_balance_df[ (year_balance_df["Tech"] == ' SYN_METHANOLATION ')].iloc[0]['H2']))
TotalH2HABER_BOSCH=abs(float(year_balance_df[ (year_balance_df["Tech"] == ' HABER_BOSCH ')].iloc[0]['H2']))

if abs(FluxH2SYN_METHANATION)<powerSeuil:
    FluxH2SYN_METHANATION=0
    TotalH2SYN_METHANATION=0
    print('H2SYN_METHANATION OFF')        
else:
    print('H2SYN_METHANATION ON')
    
if abs(FluxH2SYN_METHANOLATION)<powerSeuil:
    FluxH2SYN_METHANOLATION=0
    TotalH2SYN_METHANOLATION=0
    print('H2SYN_METHANOLATION OFF')        
else:
    print('H2SYN_METHANOLATION ON')

if abs(FluxH2HABER_BOSCH)<powerSeuil:
    FluxH2HABER_BOSCH=0
    TotalH2HABER_BOSCH=0
    print('H2HABER_BOSCH OFF')        
else:
    print('H2HABER_BOSCH ON')    


H2Industrial={'TechnologyH2':['SYN_METHANATION','SYN_METHANOLATION','HABER_BOSCH'],
              'FluxH2_GW_H2':[FluxH2SYN_METHANATION,FluxH2SYN_METHANOLATION,FluxH2HABER_BOSCH],
              'TotalH2_GWh_H2':[TotalH2SYN_METHANATION,TotalH2SYN_METHANOLATION,TotalH2HABER_BOSCH]}

H2Industrial_df=pd.DataFrame(H2Industrial)

#H2toP#########################################################################

FluxH2DEC_ADVCOGEN_H2=abs(float(assets_df[ (assets_df["TECHNOLOGIES"] == 'DEC_ADVCOGEN_H2')].iloc[0][' f'])*float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['H2']))
#abs(layer_H2['DEC_ADVCOGEN_H2'].min())

TotalH2DEC_ADVCOGEN_H2=abs(float(year_balance_df[ (year_balance_df["Tech"] == ' DEC_ADVCOGEN_H2 ')].iloc[0]['H2']))

eta_DEC_ADVCOGEN_H2=abs(float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['ELECTRICITY'])/(float(layer_in_out_df[layer_in_out_df["param layers_in_out:"]=='DEC_ADVCOGEN_H2'].iloc[0]['H2'])))

if abs(FluxH2DEC_ADVCOGEN_H2)<powerSeuil:
    FluxH2DEC_ADVCOGEN_H2=0
    TotalH2DEC_ADVCOGEN_H2=0
    eta_DEC_ADVCOGEN_H2=0
    print('DEC_ADVCOGEN_H2 OFF')
            
else:
    print('DEC_ADVCOGEN_H2 OFF') 
    
    

H2toP={'TechnologyH2':['DEC_ADVCOGEN_H2'],
       'FluxH2_GW_H2':[FluxH2DEC_ADVCOGEN_H2],
       'TotalH2_GWh_H2':[TotalH2DEC_ADVCOGEN_H2],
       'eff':[eta_DEC_ADVCOGEN_H2],
       'MTTF':[2000],
       'MTTR':[50]
       }

H2toP_df= pd.DataFrame(H2toP)

#H2Storage#####################################################################

H2_STORAGE_Pin=abs(layer_H2['H2_STORAGE_Pin'].min())
H2_STORAGE_Pout=layer_H2['H2_STORAGE_Pout'].max()

H2_STORAGE=float(assets_df[ (assets_df["TECHNOLOGIES"] == 'H2_STORAGE')].iloc[0][' f'])

if abs(H2_STORAGE_Pout)<powerSeuil:
    H2_STORAGE_Pin=0
    H2_STORAGE_Pout=0
    H2_STORAGE=0
    print('H2_STORAGE OFF')
            
else:
    print('H2_STORAGE ON') 

H2Storage={'H2_STORAGE_Pin_GW_H2':[H2_STORAGE_Pin],
           'H2_STORAGE_Pout_GW_H2':[H2_STORAGE_Pout],
           'EmaxStorageH2_GWh_H2':[H2_STORAGE]
           } 

H2Storage_df= pd.DataFrame(H2Storage)




####################################Shift######################################

# Shift={'Max_shiftable_power_[MW]':[0],
#        'Max_daily_shiftable_energy_[MWh/day]':[0],
#        'Shift_cost_[€/MWh]':[1]}


# Shift_df=pd.DataFrame(Shift)

#####################################Shed######################################

# Shed={'Max_shed_power_[MW]':[0],
#       'Max_daily_shed_energy_[MWh/day]':[0],
#       'Shed_cost_[€/MWh]':[150]
      
#       }

# Shed_df=pd.DataFrame(Shed)


###############################################################################

writer = pd.ExcelWriter('my_data.xlsx', engine='xlsxwriter')

General_df.to_excel(writer, sheet_name='General', index=False)
BusesShare_df.to_excel(writer, sheet_name='Nodes', index=False)
#Buses_df.to_excel(writer, sheet_name='Buses', index=False)
Lines_df.to_excel(writer, sheet_name='Lines', index=False)
#Share_df.to_excel(writer, sheet_name='Share', index=False)

Gen_df.to_excel(writer, sheet_name='Gen', index=False)
Energy_CHP_df.to_excel(writer, sheet_name='LF_month_CHP', index=False)
DistRes_df.to_excel(writer, sheet_name='DistRes', index=False)
#Geothermal_df.to_excel(writer, sheet_name='Geothermal', index=False)
DistGen_df.to_excel(writer, sheet_name='DistGen', index=False)
Res_df.to_excel(writer, sheet_name='Res', index=False)
Imp_Data_df.to_excel(writer, sheet_name='Imp_Data', index=False)
ImportLines_df.to_excel(writer, sheet_name='Imp_Line', index=False)
Phs_df.to_excel(writer, sheet_name='Phs', index=False)
Batt_df.to_excel(writer, sheet_name='Batt_LI', index=False)
CCS_df.to_excel(writer, sheet_name='CCS', index=False)
Freight_df.to_excel(writer, sheet_name='FreightELEC', index=False)
IndustrialProcess_ELEC_df.to_excel(writer, sheet_name='IndustrialProcess_ELEC', index=False)
Electrolyzer_ELEC_df.to_excel(writer, sheet_name='Electrolyzer_ELEC', index=False)
IndustrialHeat_df.to_excel(writer, sheet_name='IndustrialHeat', index=False)
ResidentialHeat_df.to_excel(writer, sheet_name='ResidentialHeat', index=False)

#H2Buses_df.to_excel(writer, sheet_name='H2Buses', index=False)
H2Import_df.to_excel(writer, sheet_name='H2Import', index=False)
H2Pipeline_df.to_excel(writer, sheet_name='H2PipeLines', index=False)
H2Export_df.to_excel(writer, sheet_name='H2Export', index=False)
#H2AMMONIA_TO_H2_df.to_excel(writer, sheet_name='H2AMMONIA_TO_H2', index=False)
H2Production_df.to_excel(writer, sheet_name='H2Production', index=False)
H2Freight_df.to_excel(writer, sheet_name='H2Freight', index=False)
H2Industrial_df.to_excel(writer, sheet_name='H2Industrial', index=False)
H2toP_df.to_excel(writer, sheet_name='H2toP', index=False)
H2Storage_df.to_excel(writer, sheet_name='H2Storage', index=False)

# Shift_df.to_excel(writer, sheet_name='Shift', index=False)
# Shed_df.to_excel(writer, sheet_name='Shed', index=False)

writer.save()