import pandas as pd
import itertools

def transform():
    train_path = "./train_data.csv"
    test_path = "./test_data.csv"
    val_path = "./sample_submission.csv"

    #Create new datasets only with
    emos = ["empty", "sadness", "surprise", "happiness", "anger"]

    train_data = pd.read_csv(train_path, engine="python")
    #print(train_data.head())

    test_data = pd.read_csv(test_path, engine="python")
    print(test_data.head())

    val_data = pd.read_csv(val_path, engine="python")
    print(val_data.head())

    tmp_sent = []
    tmp_cont = []
    for row in train_data.itertuples():
        if row.sentiment in emos:
            tmp_sent.append(row.sentiment)
            tmp_cont.append(row.content)

    new_train = { "sentiment": tmp_sent,
                  "content": tmp_cont}
    new_train = pd.DataFrame(new_train)
    new_train.to_csv('train_data_red.csv')

    tmp_sent = []
    tmp_cont = []
    for row in val_data.itertuples():
        if row.sentiment in emos:
            tmp_sent.append(row.sentiment)
            tmp_cont.append(test_data.content[row.id-1])

    new_test = {"content": tmp_cont}
    new_test = pd.DataFrame(new_test)
    new_test.to_csv('test_data_red.csv')

    new_val = {"sentiment": tmp_sent}
    new_val = pd.DataFrame(new_val)
    new_val.to_csv('val_data_red.csv')


transform()
