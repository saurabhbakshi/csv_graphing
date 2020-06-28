import os
import pandas as pd


def listFiles(abs_output_dir):
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(abs_output_dir):
        path = os.path.join(abs_output_dir, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def remove_file(abs_oputput_dir, filename):
    os.remove(os.path.join(abs_oputput_dir, filename))


def sanitize_data(data):
    data = data.dropna()
    return data


def loadDataFrame(file_path, delimiter, data_from=None, data_to=None):
    with open(file_path, 'r') as fp:
        line = fp.readline()
        if delimiter not in line:
            return None, "Error loading file! The delimiter specified can't be found in file."
    data = pd.read_csv(file_path, delimiter=delimiter, error_bad_lines=False)
    max_range = len(data)
    data = sanitize_data(data)
    return data[data_from:data_to], max_range, None


def split_dataFrame_column(data_frame, source_columns, column_splitter, target_columns):
    s_col = None
    t_col = None
    if "," in source_columns:
        s_col = source_columns.split(',')
    else:
        s_col = [source_columns]
    if "," in target_columns:
        t_col = target_columns.split(',')
    for col_index, col_value in enumerate(s_col):
        target_index_start = col_index*2
        target_index_end = target_index_start+2
        data_frame[t_col[target_index_start:target_index_end]
                   ] = data_frame[col_value].str.split(column_splitter, expand=True)
    for col in t_col:
        data_frame[col] = data_frame[col].apply(lambda x: str(x).strip())
    return data_frame


def listToDataFrame(lst):
    dataFrame = pd.DataFrame(lst)
    return dataFrame
