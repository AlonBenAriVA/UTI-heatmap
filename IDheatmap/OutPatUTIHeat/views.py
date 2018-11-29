from django.shortcuts import render
import pandas as pd
import pyodbc
from  geojson import Point, Feature, FeatureCollection, dumps, dump
import os
import numpy as np
import random

# Create your views here.



def default_map(request):
    points = get_points()
    fc = points.get_geojson()
    
    return render(request, 'default.html', {'fc':fc,'access_token':'pk.eyJ1IjoiYWxvbmJlbmFyaSIsImEiOiJjam3NzE0dHQwMGY1M2tvNWFpYjF6YXJ4In0.tnvBEwJAYfqUtTRWy94veQ'})


class get_points:
    def __init__(self):
            sql = 'select * from LSV.MAC_UTI'
            self.SQLsubmit(sql)
            # self.data['value'] = np.ones((self.data.shape[0]))
            # self.ssn_dict = {self.data.iloc[p,:]['PatientSSN']:self.data.iloc[p,:]['PatientName']  for p in self.data.index}
            # print(self.ssn_dict)
            # self.data['HealthFactorDate'] =  self.data.HealthFactorDateTime.apply(pd.to_datetime).dt.date  # get only the month out.

            # self.data.DischargeDateTime = self.data.DischargeDateTime.fillna(pd.Timestamp.today().strftime('%m-%d-%Y %H:%M:%S')) # fix NAN in discharge dates (death, still inpat etc.)

            # self.patient_ssn = self.data.PatientSSN.unique() # get unique SSNs

            # self.patient_history = {p:self.data[self.data.PatientSSN == p] for p in self.patient_ssn } # get the relevant patient chunk of data from table

            # self.patient_admit = { p: self.patient_history[p].AdmitDateTime.unique() for p in self.patient_ssn } #dictionary of patient admits
            # self.patient_discharge = { p: self.patient_history[p].DischargeDateTime.unique() for p in self.patient_ssn } # dictionary of patient discharge

            # self.data.columns = ['PatientSSN', 'PatientName', 'Age', 'Gender', 'WardLocationName',
            #                 'RoomBed', 'HealthFactorType', 'AdmitDateTime', 'HealthFactorDateTime',
            #                 'SpecimenTakenDateTime', 'DischargeDateTime', 'RequestingWard',
            #                 'SpecimenComment', 'CollectionSample', 'OrganismQuantity',
            #                 'AntibioticSensitivityValue', 'AntibioticSensitivityComments',
            #                 'Antibiotic', 'DrugNodeIEN', 'AntibioticDisplayComment', 'LabProcedure'
            #                 'Organism', 'OrganismCategory', 'GramStain', 'PatientCity',
            #                 'PatientCounty', 'PatientState', 'PatientZip', 'PatientZip4',
            #                 'PatientLON', 'PatientLAT', 'PatientFIPS', 'PatientMarket',
            #                 'PatientSubmarket', 'Growth', 'Inpatient', 'Sta3n', 'LineNew',
            #                 'LineStatus', 'LineLoc', 'LineRemoved', 'PatientSID']

    def SQLsubmit(self,sql, params =[],server='vhacdwdwhsql33.vha.med.va.gov', db='D05_VISN21Sites'):
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';Trusted_Connection=yes;Integrated Security=SSPI')
        self.data = pd.read_sql_query(sql = sql, con = conn, params = params)
        conn.close()

    def get_geojson(self):
        """
        A method to return a geojson object
        """
        obj = []
        for p in [Feature(geometry = Point((d['PatientLON'],d['PatientLAT'])), properties = {'value':100.0}) for d in self.data[['PatientLAT','PatientLON']].drop_duplicates().to_dict('records')]:
            obj.append(p)
       
        return FeatureCollection(obj)




