# -*- coding : utf-8-*-
import json
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

def deal_data_pre(path):
    file = open(path, 'r', encoding='utf-8')
    data = []
    for line in file.readlines():  # 由于文件过大 所以一行一行读取
        dic = json.loads(line)
        data.append(dic)
    all_data = []
    # print(data[0])
    for i in range(len(data)):
        text = data[i]['text']
        spo_list = data[i]['spo_list']
        spo_list_1 = []
        spo_list_2 = []
        for j in range(len(spo_list)):
            object_item = []
            if len(spo_list[j]['object']) >= 2:
                count = 0
                while count < len(spo_list[j]['object']):
                    spo_list_1.append(spo_list[j]['subject'])
                    end = []  # 用于暂时存储object的键值 eg. value、in work...
                    for k, m in spo_list[j]['object'].items():
                        end.append(k)
                        object_item.append(m)
                    if end[count] == 'inWork':
                        spo_list_1.append(spo_list[j]['predicate'] + '作品')
                    elif end[count] == 'inArea':
                        spo_list_1.append(spo_list[j]['predicate'] + '地点')
                    elif end[count] == 'onDate':
                        spo_list_1.append(spo_list[j]['predicate'] + '日期')
                    elif end[count] == 'period':
                        spo_list_1.append(spo_list[j]['predicate'] + '时间')
                    else:
                        spo_list_1.append(spo_list[j]['predicate'])
                    # spo_list_1.append(spo_list[j]['predicate'] + '_' + end[count])
                    spo_list_1.append(object_item[count])
                    count += 1
                    spo_list_2.append(spo_list_1)
                    spo_list_1 = []
            else:
                spo_list_1.append(spo_list[j]['subject'])
                for k, m in spo_list[j]['object'].items():
                    object_item.append(m)
                # if spo_list[j]['predicate'] == '票房' or spo_list[j]['predicate'] == '配音' \
                #         or spo_list[j]['predicate'] == '获奖' or spo_list[j]['predicate'] == '饰演' \
                #         or spo_list[j]['predicate'] == '上映时间':
                #     spo_list_1.append(spo_list[j]['predicate'] + '_' + end[0])
                # else:
                spo_list_1.append(spo_list[j]['predicate'])
                spo_list_1.append(object_item[0])
                spo_list_2.append(spo_list_1)
                spo_list_1 = []
        # print(spo_list_2)
        all_data.append(
            {
                'text': text,
                'spo_list': spo_list_2
            }
        )
    # print(len(all_data))
    # 以上对数据处理完毕
    with open("demo.json", "w", encoding='utf8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    return all_data


def load_scheme_direct(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        predicate2id = json.load(f)
        id2predicate = {}
        for i, item in enumerate(predicate2id):
            id2predicate[i] = item
            predicate2id[item] = i
        # print(id2predicate)
    return id2predicate, predicate2id


if __name__ == "__main__":
    # deal_data_pre('D:/知识图谱/DuIE数据集/data/train_data.json')
    # load_scheme_direct('D:/知识图谱/DuIE数据集/data/predicate2id.json')
    f = open('../../image/batch64 seq_len256 lr0.01/test_0.txt')
    loss_test = f.readline()
    loss_test_list = json.loads(loss_test)
    f = open('../../image/batch64 seq_len256 lr0.01/train_0.txt')
    loss_train = f.readline()
    loss_train_list = json.loads(loss_train)
    epoch_test = range(len(loss_test_list))
    epoch_train = range(len(loss_train_list))
    plt.plot(epoch_train, loss_train_list, 'r', label='training loss')
    plt.plot(epoch_test, loss_test_list, 'b', label='test loss')
    plt.title('Training loss')
    plt.show()
