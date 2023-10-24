import csv
import json

def check_if_in_list(l_item, l_list):
    i = 0
    for i in range(len(l_list)):
        if l_item == l_list[i][0:len(l_item)]:
            return i
        i += 1
    return -1


def find_ind(col_names, col_of_int):
    ind = []
    for i in range(len(col_names)):
        if col_names[i] in col_of_int:
            ind.append(i)
    return ind


def write_to_csv(file, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)


def add_crime_gravity(data, age_path="DATA//dict_partecipant_age.json", status_path="DATA//dict_partecipant_status.json", type_path="DATA//dict_partecipant_type.json"):
    # load json file content as a dictionary
    with open(age_path) as f:
        dic_p_age = json.load(f)

    with open(status_path) as f:
        dic_p_status = json.load(f)

    with open(type_path) as f:
        dic_p_type = json.load(f)

    col_of_int = ['participant_age_group', 'participant_status', 'participant_type']
    col_id = find_ind(data[0], col_of_int)

    crime_gravity = []

    data[0].append('crime_gravity')

    # for each row of the dataset minus the header
    for obs in data[1:]:
        obs.append(dic_p_age[obs[col_id[0]]] * dic_p_status[obs[col_id[1]]] * dic_p_type[obs[col_id[2]]])

    return data



def add_unique_ids(data, colums, id_name='id', path = 'DATA//NEW_TAB//NEW_TAB.csv'):
    new_table = []
    id_count = 0

    col_in = find_ind(data[0], colums)

    data[0].append(id_name)
    for i in sorted(col_in, reverse=True):
        data[0].pop(i)
        
    new_table.append(colums + [id_name])

    for row in data[1:]:
        new_row = [row[i] for i in col_in]
        ind = check_if_in_list(new_row, new_table)

        if ind == -1:
            id_count += 1
            new_row.append(id_count)
            new_table.append(new_row)
        else:
            id = new_table[ind][-1]
            new_row.append(id)

        row.append(new_row[-1])

        for i in sorted(col_in, reverse=True):
            row.pop(i)

    
    write_to_csv(new_table, path)


    return data, new_table


def add_unique_ids_2(data, columns, id_name='id', path = 'DATA//NEW_TAB//NEW_TAB.csv'):
    new_table = []
    id_count = 0

    col_in = find_ind(data[0], columns)

    data[0].append(id_name)
    for i in sorted(col_in, reverse=True):
        data[0].pop(i)
        
    new_table.append(columns + [id_name])
    id_dict = {}

    for row in data[1:]:
        new_row = tuple(row[i] for i in col_in)

        if new_row not in id_dict:
            id_dict[new_row] = id_count
            new_table.append(list(new_row) + [id_count])
            id_count += 1
        
        row.append(id_dict[new_row])

        for i in sorted(col_in, reverse=True):
            row.pop(i)

    write_to_csv(new_table, path)
    
    return data, new_table