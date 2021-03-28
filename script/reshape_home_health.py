# 在宅医療支援のオープンデータを整形・マージする

import numpy as np
import pandas as pd
import re


def erase_unnecessary(facility_data):
    facility_data_cut = facility_data[list(facility_data.columns)[4:facility_data.shape[1]]]
    return facility_data_cut


hospital = pd.read_csv("../raw_data/home_health/122173_homehealthcareh_1.csv")  # 病院のデータ
hospital = hospital.rename(columns={"病院名":"施設名"})
header_use13 = hospital.columns
header_use12 = header_use13.delete(8)
hospital.insert(4, "種別", "病院")

oushin = pd.read_csv("../raw_data/home_health/122173_homehealthcareo_1.csv", names=header_use13, skiprows=1)  # 往診可能診療所
drug_store = pd.read_csv("../raw_data/home_health/122173_homehealthcarep_1.csv", names=header_use12, skiprows=1)  # 薬局
dental = pd.read_csv("../raw_data/home_health/122173_homehealthcaret_1.csv", names=header_use12, skiprows=1)  # 歯科
zaitaku = pd.read_csv("../raw_data/home_health/122173_homehealthcarez_1.csv", names=header_use13,
                      skiprows=1)  # 在宅医療支援診療所

oushin.insert(4, "種別", "往診可能診療所")
drug_store.insert(4, "種別", "薬局")
dental.insert(4, "種別", "歯科")
zaitaku.insert(4, "種別", "在宅医療支援診療所")


export_data = pd.concat([hospital, oushin, drug_store, dental, zaitaku])
export_data = erase_unnecessary(export_data)

header_fin = export_data.columns
header_fin = [header_fin[9]] + header_fin[0:8]

# export_data = export_data.loc[:, ['種別', '施設名', '住所', '電話番号', 'URL']]

for i in range(export_data.shape[0]):
    export_data.iloc[i, 2] = re.sub('^柏市', "千葉県柏市", export_data.iloc[i, 2])

export_data.to_csv("../reshaped_data/home_health.csv", index=False)
