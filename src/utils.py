import numpy as np
import pandas as pd
import re
import types

def convert_date(valeur):
	if isinstance(valeur, str):
		valeur = float(valeur.replace(',', '.'))
	date = np.datetime64('1899-12-30') + np.timedelta64(int(valeur), 'D') + np.timedelta64(int((valeur % 1) * 24 * 60 * 60 * 10**6), 'us')
	return date

def extraire_le_cac(cac):
	match = re.search(r'\b(\d+)\b', cac)
	if match:
		return match.group(1)
	else:
		return None

def convertir_have(df, have):
	for col in have:
		df[col] = df[col].replace({"oui": True, "non": False})
		df[col] = df[col].astype(bool)
	return df

def convertir_conduite(df, conduite):
	chru = df["conduite"].values[233].str.strip()
	df[conduite] = df[conduite].replace({"MOYENS PERSONNELS": 1,
										"AMBULANCE PRIVEE": 2,
										"POMPIERS": 3,
										"AUTRES" : 4,
										"SAMU-SMUR" : 5,
										chru: 6,
										"AMB PUBLIQUE (VSAB)" : 7,
										"TAXI": 8,
										"HELICOPTERE": 9,
										"VSL": 10})
	df[conduite] = df[conduite].astype(int)
	return df

def traiter_tmp(df, tmp):
	df[tmp] = df[tmp].fillna(37)
	df[tmp] = df[tmp].astype(float)
	return df

def traiter_sat(df,sat):
	df[sat] = df[sat].fillna(100)
	df[sat] = df[sat].str.replace(' AA', '', regex=False)
	df[sat] = df[sat].astype(int)
	return df
