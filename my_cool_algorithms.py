import numpy as np
import pandas as pd
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth


def turn_to_list(datas):
    # print(data[0])
    return_dataset = []
    per_tran = []
    data_count = 0
    for data in datas:
        if int(data[0]) != data_count:
            # print(f"data: {data[0]} count: {data_count}")
            data_count += 1
            return_dataset.append(per_tran)
            per_tran = []
            per_tran.append(data[2])
        else:
            per_tran.append(data[2])
    return_dataset.append(per_tran)
    return_dataset.pop(0)
    
    print(return_dataset[:5])
    return return_dataset
    
            

def apriori(input_data, a):
    dataset = turn_to_list(input_data)
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    result = fpgrowth(df, min_support=a.min_sup, use_colnames=True)
    print(result)
    # return results
