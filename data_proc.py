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
    
    # print(return_dataset[0])
    return return_dataset