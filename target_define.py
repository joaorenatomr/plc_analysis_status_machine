"""
In  -> df (4 bits machine + n sequencer * n ABCD * 32), operator_list, idle_list
Out -> df dummies 5 categorie (machine, operator, idle, maintenance, scrap)

bits machine:
Machine_auto
AlarmActive
LC_interrupt
ScrapRequest

Categories:
machine_auto or AlarmActive -> maintenance
ScrapRequest -> scrap
idle_list -> idle
operator_list -> operator
Rest -> machine
"""


def contains_elements(list1, list2):
    #Verify elements in list2 is in list1
    for element in list2:
        if element in list1 or f"-{element}" in list1:
            return True
        else:
            return False


def target_define (df, n_seq, tab_list, operator_list, idle_list):
    #Initial
    for index in range(len(df)):
        seq_list = []
        row = df.loc[index]
        if row["ScrapRequest"] == 1:
            df.at[index, "target"] = "scrap"
        elif row["MachineAuto"] ==0 or row["AlarmActive"] == 1:
            df.at[index, "target"] = "maintenance"
        else:
            for seq in range(n_seq):
                for tab in tab_list:
                    for i in range(32):
                        cmd = row[f"CMD_{seq}{tab}_{i}_binary"]
                        sts = row[f"STS_{seq}{tab}_{i}_binary"]
                        msk = row[f"MSK_{seq}{tab}_{i}_binary"]
                        if cmd == 1:
                            if (sts + msk) == 0:
                                seq_list.append(f"{seq}{tab}{i}")
                        elif sts == 1 and msk == 0:
                            seq_list.append(f"-{seq}{tab}{i}")
            if contains_elements(seq_list, idle_list):
                df.at[index, "target"] = "idle"
            elif contains_elements(seq_list, operator_list) or row["LC_Interrupt"] == 1:
                df.at[index, "target"] = "operator"
            else:
                df.at[index, "target"] = "machine"
            df.at[index, "target_string"] = seq_list

    df_update = df
    
    return df_update

