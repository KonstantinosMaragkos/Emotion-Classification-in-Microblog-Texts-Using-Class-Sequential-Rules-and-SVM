import pandas as pd

def test():
    train_path = "./train_data_red.csv"
    test_path = "./val_data_red.csv"

    tr_d = pd.read_csv(train_path, engine="python")
    #print(tr_d.head())
    ts_d = pd.read_csv(test_path, engine="python")
    
    un = tr_d.sentiment.unique()
    print("emos are", un, "and size of file is", len(tr_d))

    for sent in un:
        print(sent +":",(tr_d["sentiment"] == sent).sum())

    un2 = ts_d.sentiment.unique()
    print("emos are", un2, "and size of file is", len(ts_d))

    for sent in un2:
        print(sent +":",(ts_d["sentiment"] == sent).sum())
test()
