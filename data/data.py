import pandas as pd


def save_data(data, data_name = 'Waqar'):
    path = './data/' + data_name + '.csv'
    pd.DataFrame(data).to_csv(path)
    print("Saved data into file named - " + "file " + data_name)
