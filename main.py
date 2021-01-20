import pickle
import threading
import time

import matplotlib.pyplot as plt
import numpy as np

from entity import CloudServiceProvider, CloudServiceUser, ModelOwner
from learning import evaluation, training
from preprocessing import preprocessing
from structure import Timer
from utility import protocol, size, tree_info

DATAPATH = ["./data/heart-disease/processed.cleveland.data",
            "./data/nursery/nursery.data", "./data/weather/weatherAUS.csv"]


def draw1():
    index = np.arange(3)
    width = 0.2
    alpha = 0.5

    plt.figure(figsize=(16, 4))

    plt.subplot(141)
    plt.bar(index, [14.54, 13.58, 15.49], width,
            alpha, label='Splitting query data')
    plt.bar(index+0.2, [31.09, 71.85, 210.06],
            width, alpha, label='Classification')
    plt.xlabel("Dataset")
    plt.ylabel("Time cost (ms)")
    plt.title("(a) Time cost with N = 32")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index+0.1, ("heart", "nursery", "weatherAUS"))

    plt.subplot(142)
    plt.bar(index, [15.49, 14.98, 15.64], width,
            alpha, label='Splitting query data')
    plt.bar(index+0.2, [31.17, 71.99, 211.45],
            width, alpha, label='Classification')

    plt.xlabel("Dataset")
    plt.ylabel("Time cost (ms)")
    plt.title("(b) Time cost with N = 128")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index+0.1, ("heart", "nursery", "weatherAUS"))

    plt.subplot(143)
    plt.bar(index, [2, 2.97, 8.24], width, alpha, label='CSU')
    plt.bar(index+0.2, [0.88, 4.84, 57.36], width, alpha, label='CSP')

    plt.xlabel("Dataset")
    plt.ylabel("Storage overhead (kB)")
    plt.title("(c) Storage overhead with N = 32")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index+0.1, ("heart", "nursery", "weatherAUS"))
    plt.ylim(0, 80)

    plt.subplot(144)
    plt.bar(index, [2.29, 3.15, 9.11], width, alpha, label='CSU')
    plt.bar(index+0.2, [0.97, 5.81, 76.6], width, alpha, label='CSP')

    plt.xlabel("Dataset")
    plt.ylabel("Storage overhead (kB)")
    plt.title("(d) Storage overhead with N = 128")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index+0.1, ("heart", "nursery", "weatherAUS"))
    plt.ylim(0, 80)
    plt.show()


def draw2():
    index = np.arange(4)
    width = 0.6
    alpha = 0.5

    plt.figure()

    plt.subplot(121)
    plt.bar(index, [42, 51, 53, 58], width,
            alpha, label='Time cost of CSP')

    plt.xlabel("Number of users")
    plt.ylabel("Time cost (ms)")
    plt.title("(a) Nursery")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index, ("2","4","6","8"))
    plt.ylim(0, 150)

    plt.subplot(122)
    plt.bar(index, [74, 87, 90, 100], width,
            alpha, label='Time cost of CSP')

    plt.xlabel("Number of users")
    plt.ylabel("Time cost (ms)")
    plt.title("(b) WeatherAUS")
    plt.legend(prop={'size': 9})
    plt.grid(True)
    plt.xticks(index, ("2","4","6","8"))
    plt.ylim(0, 150)
    plt.show()


def job(csu, csp, index):
    timer = Timer()
    for i in range(index, index + 50):
        csu.new_data(trainingData.loc[i])
        csu.send_share(csp)
        protocol(csu, csp, csu.node, csp.node)
    print(index, timer.end())


if __name__ == '__main__':
    datas = preprocessing(DATAPATH)
    for name, data in datas.items():
        print(f"Processing {name} dataset -> {len(data)}")
        margin = int(len(data)*0.8)
        trainingData = data[:margin].reset_index(drop=True)
        testingData = data[margin:].reset_index(drop=True)
        with open(f"C:\\Users\\johnny\\Desktop\\paper\\model\\{name}.pk", "rb") as f:
            model = pickle.load(f)
        # evaluation(model, testingData)

        mo = ModelOwner(model)
        csp = CloudServiceProvider()

        # for j in [10,20,30,40]:
        #     timer = Timer()
        #     threads = []
        #     for i in range(j):
        #         csu = CloudServiceUser()
        #         mo.distributed_shares(csu, csp)
        #         threads.append(threading.Thread(target=job, args=(csu,csp,i*50)))
        #         threads[i].start()
    draw2()
    #     for i in range(j):
    #         threads[i].join()
    #     print(f"total with {j} users: {timer.end():.4f}")

    # timestamp1 = []
    # timestamp2 = []
    # timer1 = Timer()
    # timer2 = Timer()
    # for i in range(1):
    #     timer1.reset("Split query data")
    #     csu.new_data(trainingData.loc[i])
    #     csu.send_share(csp)
    #     timestamp1.append(timer1.end())

    #     timer2.reset("Evaluation once")
    #     protocol(csu, csp, csu.node, csp.node)
    #     timestamp2.append(timer2.end())

    # print(np.mean(timestamp1))
    # print(np.mean(timestamp2))
    # nodes, depth = tree_info(mo.model)
    # print(size(csu.node) * depth + size(csu.seed) +
    #       size(csu.data) + size(csu.share1)+size(csu.share2))
    # print(size(csp.node) + size(csp.data))

    # correct = 0
    # for i in range(len(testingData)):
    #     csu.new_data(testingData.loc[i])
    #     csu.send_share(csp)
    #     if protocol(csu, csp, csu.node, csp.node) == csu.data['label']:
    #         correct += 1
    # print(f"Accuracy: {correct/len(testingData):.4f}")
    # nodes, depth = tree_info(mo.model)
    # print(f"數據維度/節點數/深度: {data.shape[1]}/{nodes}/{depth}")
    # print()
