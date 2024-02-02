import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from category_encoders import OneHotEncoder

def parser_date_hum(valeur):
    formats = ['%d/%m/%Y %H:%M', '%d/%m/%y %H:%M']
    for format_date in formats:
        try:
            dates_datetime64 = pd.to_datetime(valeur, format=format_date)
            return np.datetime64(dates_datetime64, 's')
        except ValueError:
            pass
    return None

def convert_date(valeur):
    checkeur = ["/", ":","-"]
    if isinstance(valeur, pd.Timestamp):
        return np.datetime64(valeur,'s')
    if isinstance(valeur, str) and any(c in valeur for c in checkeur):
        return parser_date_hum(valeur)
    else:
        if isinstance(valeur, str):
            valeur = float(valeur.replace(',', '.'))
        date = np.datetime64('1899-12-30') + np.timedelta64(int(valeur), 'D') + np.timedelta64(int((valeur % 1) * 24 * 60 * 60 * 10**6), "us")
        return date

def extraire_le_cac(cac):
	match = re.search(r'\b(\d+)\b', cac)
	if match:
		return match.group(1)
	else:
		return 0

def convertir_have(df, have):
	for col in have:
		df[col] = df[col].replace({"oui": True, "non": False})
		df[col] = df[col].astype(bool)
	return df

def convertir_conduite(df, conduite):
	chru = df["conduite"].values[233]
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
	df['conduite'] = df['conduite'].apply(lambda x: 6 if not isinstance(x, int) else x)
	df[conduite] = df[conduite].astype(int)
	return df

def traiter_tmp(valeur):
    try:
        valeur = str(valeur).replace(',', '.')
        return float(valeur)
    except (TypeError, ValueError):
        return 37.0

def traiter_sat(valeur):
    try:
        valeur = str(valeur).replace(' AA', '')
        return int(valeur)
    except (TypeError, ValueError):
        return 100
"""def traiter_tmp(df, tmp):
    df[tmp] = df[tmp].fillna("37")
    df[tmp] = df[tmp].replace(',', '.')
    df[tmp] = df[tmp].astype(float)
    return df

def traiter_sat(df,sat):
	df[sat] = df[sat].fillna(100)
	df[sat] = df[sat].str.replace(' AA', '', regex=False)
	df[sat] = df[sat].astype(int)
	return df"""
def factorizer(dfpcat):
    print(type(dfpcat))
    dfp_encoded, dfp_cat = pd.factorize(dfpcat)
    return dfp_encoded, dfp_cat

def dummies_encode(dfp, categories):
    for i in categories:
        dumb = pd.get_dummies(dfp[i])
        dfp = pd.concat([dfp, dumb], axis = 1)
        dfp = dfp.drop([i], axis = 1)
    return dfp

def lstenc(dfp):
	listcat = ["conduite","m_venue","have_bio","have_radio","have_echo","have_scan","have_specia", "have_irm","intitule_diag", "cac_admi","cac_sejour","destination","cp_ville"]
	dfp = dummies_encode(dfp, listcat)
	return dfp


def lstencore(dfp):
    listcat = ["conduite","m_venue","have_bio","have_radio","have_echo","have_scan","have_specia", "have_irm","intitule_diag", "cac_admi","cac_sejour","destination","cp_ville"]
    encoder = OneHotEncoder(cols = listcat)
    dfp = encoder.fit_transform(dfp)
    return dfp


def lstdate(dfp):
	trslt = ["date_urg","date_box","date_prescri_bio","date_prelev_bio","date_sortie","date_deb_pec_med"]
	for x in trslt :
		dfp[x] = dfp[x].fillna(0)
		try :
			dfp[x] = dfp[x].apply(convert_date)
		except ValueError:
			print(f"erreur dans colonne { x }")
	return dfp

def ttt_destination(valeur):
    if valeur.startswith("RETOUR DOMICILE"):
        return 1
    elif valeur.startswith("PARTIE"):
        return 2
    elif valeur.startswith("Admis(e)"):
        return extraire_le_cac(valeur.split()[-1])
    elif valeur.startswith("CONTRE"):
        return 3
    else :
        return 4

def separer_pression_sanguine(df, colonne):
    df[['systo', 'diasto']] = df[colonne].str.split('/', expand=True)
    df['systo'] = pd.to_numeric(df['systo'], errors='coerce')
    df['diasto'] = pd.to_numeric(df['diasto'], errors='coerce')
    df = df.drop(colonne, axis = 1)
    return df

def pipelinett(dfp):
      dfp["tmp_ad"] = dfp["tmp_ad"].apply(traiter_tmp)
      dfp["saoxy_ad"] = dfp["saoxy_ad"].apply(traiter_sat)
      dfp["cac_admi"] = dfp["cac_admi"].apply(extraire_le_cac)
      dfp["destination"] = dfp["destination"].apply(ttt_destination)
      dfp = separer_pression_sanguine(dfp, "cst_paspad")
      return dfp

def pipeline_t_by_p(dfp):
    dfp = lstdate(dfp)
    dfp = dfp.drop(["m_entry",
                    "atcd_med",
					"atcd_chir",
					"cst_paspad",
					"fc_ad",
					"tmp_ad",
					"saoxy_ad",
					"fr_ad",
                    "salle",
					"date_box",
					"anamn",
					"obs",
					"have_bio",
					"have_radio",
					"have_echo",
					"have_scan",
					"have_irm",
					"have_specia",
					"date_prescri_bio",
					"date_prelev_bio",
					"code_diag",
					"intitule_diag",
					"cac_admi",
					"cac_sejour",
					"date_deb_pec_med",
					"dossier_hopit",
					"type_orient",
					"destination",
					"transfert_service",
					"transfert_hopit",
					"cp_ville",
					"ville"], axis = 1)
    return dfp

