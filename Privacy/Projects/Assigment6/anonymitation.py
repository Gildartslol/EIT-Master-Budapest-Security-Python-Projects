import pandas as pd
import numpy as np


def get_spans(dataFrame, partition, scale=None):
    """
    :param        dataFrame: the dataframe for which to calculate the spans
    :param partition: the partition for which to calculate the spans
    :param     scale: if given, the spans of each column will be divided
                      by the value in `scale` for that column
    :        returns: The spans of all columns in the partition
    """
    spans = {}
    for column in dataFrame.columns:
        if column in categorical:
            span = len(dataFrame[column][partition].unique())
        else:
            span = dataFrame[column][partition].max() - dataFrame[column][partition].min()
        if scale is not None:
            span = span / scale[column]
        spans[column] = span
    return spans


def split(dataFrame, partition, column):
    """
    :param        dataFrame: The dataframe to split
    :param partition: The partition to split
    :param    column: The column along which to split
    :        returns: A tuple containing a split of the original partition
    """
    dfp = dataFrame[column][partition]
    if column in categorical:
        values = dfp.unique()
        lv = set(values[:len(values) // 2])
        rv = set(values[len(values) // 2:])
        return dfp.index[dfp.isin(lv)], dfp.index[dfp.isin(rv)]
    else:
        median = dfp.median()
        dfl = dfp.index[dfp < median]
        dfr = dfp.index[dfp >= median]
        return dfl, dfr


# try k-anonymity now

def is_k_anonymous(dataFrame, partition, sensitive_column, k=3):
    """
    :param               dataFrame: The dataframe on which to check the partition.
    :param        partition: The partition of the dataframe to check.
    :param sensitive_column: The name of the sensitive column
    :param                k: The desired k
    :returns               : True if the partition is valid according to our k-anonymity criteria, False otherwise.
    """
    if len(partition) < k:
        return False
    return True


def partition_dataset(dataFrame, feature_columns, sensitive_column, scale, is_valid):
    """
    :param               dataFrame: The dataframe to be partitioned.
    :param  feature_columns: A list of column names along which to partition the dataset.
    :param sensitive_column: The name of the sensitive column (to be passed on to the `is_valid` function)
    :param            scale: The column spans as generated before.
    :param         is_valid: A function that takes a dataframe and a partition and returns True if the partition is valid.
    :returns               : A list of valid partitions that cover the entire dataframe.
    """
    finished_partitions = []
    partitions = [dataFrame.index]
    while partitions:
        partition = partitions.pop(0)
        spans = get_spans(dataFrame[feature_columns], partition, scale)
        for column, span in sorted(spans.items(), key=lambda x: -x[1]):
            lp, rp = split(dataFrame, partition, column)
            if not is_valid(dataFrame, lp, sensitive_column) or not is_valid(dataFrame, rp, sensitive_column):
                continue
            partitions.extend((lp, rp))
            break
        else:
            finished_partitions.append(partition)
    return finished_partitions


categorical = {'sex', 'city', 'province', 'country', 'geo_resolution', 'date_onset_symptoms', 'date_admission_hospital',
               'date_confirmation', 'symptoms',
               'symptoms', 'lives_in_Wuhan', 'travel_history_dates', 'travel_history_location',
               'reported_market_exposure', 'additional_information', 'chronic_disease',
               'source', 'sequence_available', 'outcome', 'date_death_or_discharge', 'notes_for_discussion', 'location',
               'admin3', 'admin2', 'admin1', 'country_new',
               'admin_id', 'data_moderator_initials'}

if __name__ == '__main__':

    # Step2: Import the dataset from address or define a database by ourselves
    covid = pd.read_csv('./novel-corona-virus-2019-dataset/COVID19_open_line_list.csv')
    covid = covid.head(50)

    for name in categorical:
        covid[name] = covid[name].astype('category')

    covid["age"] = pd.to_numeric(covid["age"])

    # Step3: Assign it to a variable named covid19
    covid.dropna(subset=["age"], inplace=True)
    print(covid)
    #Play with some functuons. Implementing spans and partitions
    feature_columns = ['sex', 'country']
    sensitive_column = 'age'
    full_spans = get_spans(covid, covid.index)
    print(full_spans)
    finished_partitions = partition_dataset(covid, feature_columns, sensitive_column, full_spans, is_k_anonymous)
    print(finished_partitions)

