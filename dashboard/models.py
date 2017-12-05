from django.db import models
from dashboard.stdbscan import *
import numpy as np
import pandas as pd

# Create your models here.
class Parameters(models.Model):
	IPM_file = models.FileField(upload_to='datasets/', default="")
	eps1 = models.FloatField()
	eps2 = models.FloatField()
	minPts = models.IntegerField()
	de = models.FloatField()

	def getKab(self, dataset):
		dataset_ipm_jawa = np.genfromtxt(dataset, delimiter=',', skip_header=1, dtype='U')
		kab_ipm = dataset_ipm_jawa[:,0]

		return kab_ipm

	def doSTDBSCAN(self):
		load_data = self.IPM_file
		dataset_ipm_jawa = np.genfromtxt(load_data, delimiter=',', skip_header=1)
		dataset_ipm_jawa = np.delete(dataset_ipm_jawa, 0, 1)

		result = ST_DBSCAN(dataset_ipm_jawa, self.eps1, self.eps2, self.minPts, self.de)

		return result

	def resultToJson(self):

		kab_ipm = self.getKab(self.IPM_file)
		result = self.doSTDBSCAN()

		df_kab = pd.DataFrame(kab_ipm, columns=['kabupaten'])
		df_result = pd.DataFrame(result, columns =['longitude', 'latitude', 'tahun', 'ipm', 'cluster'])

		df = pd.concat((df_kab, df_result), axis=1)

		return df.to_json(orient='split')