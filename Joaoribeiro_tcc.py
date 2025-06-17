#Import libraries
import pandas as pd
import os
import random
import tensorflow as tf
import keras
import numpy as np
from keras import layers
from sklearn.model_selection import train_test_split
from plc_functions import int_to_binary_cmd_sts, int_to_binary_msk
from target_define import target_define


"""-------------"""
"""---Machine---"""
"""-------------"""
class machine:
    plant = "ABM"
    line = "AW"
    station = "010"
    n_seq = 1
    tab_list = ["A", "B", "C", "D"]
    operator_list = ["0A3"]
    idle_list = ["0D11"]
    add_scrap = True
    save_df = True


"""-------------"""
"""IA Initialize"""
"""-------------"""

#Seed definition
seed = 0
np.random.seed(seed)
tf.random.set_seed(seed)
random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

#Initializer seed
initializer = tf.keras.initializers.GlorotUniform(seed = seed)

#Config tf to determinism
tf.config.experimental.enable_op_determinism()

"""-------------"""
"""Data Wragling"""
"""-------------"""

#Columns List
column_list = ["MachineAuto", "AlarmActive", "LC_Interrupt", "ScrapRequest"]
column_list_cmd = []
column_list_sts = []
column_list_msk = []
column_list_str = []
column_list_binary = []

#Column list sequencer
for seq in range(machine.n_seq):
    for tab in machine.tab_list:
        column_list_cmd.append(f"CMD_{seq}{tab}")
        column_list_sts.append(f"STS_{seq}{tab}")
        column_list_msk.append(f"MSK_{seq}{tab}")

#Load data
df_dataset = pd.read_csv("ABM_AW_ST010.csv", sep= ";")

#Clean NA, DateTime and PN
df_clean = df_dataset.dropna()
df_clean = df_clean.drop(columns=["DateTime", "PN", "ActiveStep"])

#Change type to int
df_clean[column_list] = df_clean[column_list].astype(int)
df_clean[column_list_cmd] = df_clean[column_list_cmd].astype(int)
df_clean[column_list_sts] = df_clean[column_list_sts].astype(int)
df_clean[column_list_msk] = df_clean[column_list_msk].astype(int)

#Scrap part to IA training
if machine.add_scrap:
    row_to_add = int(len(df_clean) * 0.1) #10% scrap data
    df_to_add = df_clean.sample(frac=0.1, replace=True)
    df_to_add["ScrapRequest"] = 1
    df_clean = pd.concat([df_clean, df_to_add], ignore_index=True)

#Dataframe initial
df_initial = df_clean

#Column binary
#df with column binary PLC CMD
for column_name in column_list_cmd:
    df_initial[f"{column_name}_binary"] = df_initial[column_name].apply(int_to_binary_cmd_sts)
    column_list_str.append(f"{column_name}_binary")
    for i in range(32):
        df_initial[f"{column_name}_{i}_binary"] = df_initial[f"{column_name}_binary"].apply(lambda x: x[i]).astype(int)
        column_list_binary.append (f"{column_name}_{i}_binary")

#df with column binary PLC STS
for column_name in column_list_sts:
    df_initial[f"{column_name}_binary"] = df_initial[column_name].apply(int_to_binary_cmd_sts)
    column_list_str.append(f"{column_name}_binary")
    for i in range(32):
        df_initial[f"{column_name}_{i}_binary"] = df_initial[f"{column_name}_binary"].apply(lambda x: x[i]).astype(int)
        column_list_binary.append (f"{column_name}_{i}_binary")

#df with column binary PLC MSK
for column_name in column_list_msk:
    df_initial[f"{column_name}_binary"] = df_initial[column_name].apply(int_to_binary_msk)
    column_list_str.append(f"{column_name}_binary")
    for i in range(32):
        df_initial[f"{column_name}_{i}_binary"] = df_initial[f"{column_name}_binary"].apply(lambda x: x[i]).astype(int)
        column_list_binary.append (f"{column_name}_{i}_binary")

df_initial["target_string"] = ""
df_initial["target"] = ""

df_uptade = target_define(df_initial, machine.n_seq, machine.tab_list, machine.operator_list, machine.idle_list)
print(df_uptade)
print(df_uptade["target"].value_counts())

#breakpoint()

#Save dataframe updated
if machine.save_df:
    df_uptade.to_excel("df_update.xlsx", index=False)

# Conta as ocorrências de cada elemento na coluna
counts_elements = df_uptade['target'].value_counts()

#Train and Test
column_list_total = column_list + column_list_binary
df_X = df_clean[column_list_total]
df_y = pd.get_dummies(df_clean["target"])

df_X_train, df_X_test, df_y_train, df_y_test = train_test_split(df_X, df_y, test_size=0.2, random_state=42)

#Save dataframe updated
if machine.save_df:
    df_X_train.to_excel("df_X_train.xlsx", index=False)

print("df X train info: ")
print(df_X_train.info())

#Save dataframe updated
if machine.save_df:
    df_y_train.to_excel("df_y_train.xlsx", index=False)

print("df y train info: ")
print(df_y_train.info())

#Model define
model = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(388,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(5, activation="softmax")
    ])
print("modelo criado")

#Model Compile
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
print("modelo compilado")

#Model Training
history = model.fit(df_X_train, df_y_train, epochs=200, batch_size=1, verbose=1)
print("modelo treinado")

#Evaluete model
test_loss, test_mae = model.evaluate(df_X_test, df_y_test)

print(test_loss)
print(test_mae)

#Save model trained
model.save(f"model_{machine.plant}_{machine.line}_St.{machine.station}.h5")
