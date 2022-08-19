# This is the code that will create and make charts of stocks.
import random
import matplotlib.pyplot as plt
from matplotlib import style
import time
import matplotlib.patches as mpatches

# 4 Stocks: Apple, Google, Microsoft, IBM
stock_name = ['Apple', 'Google', 'Microsoft', 'IBM']
stock = []
style.use('seaborn-paper')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

common_x = []
cnt_list = []
GOOG_y = []
APPL_y = []
IBM_y = []
MSFT_y = []
avg_y = []
plt.ion()
plt.title("Stock Chart (Randomly Generated)")
plt.ylabel("Stock Value (Dollars)")
plt.xlabel("Time (Days) ")
red_patch = mpatches.Patch(color='red', label="Apple")
blue_patch = mpatches.Patch(color="blue", label="Google")
orange_patch = mpatches.Patch(color="orange", label="Microsoft")
yellow_patch = mpatches.Patch(color="yellow", label="IBM")
black_patch = mpatches.Patch(color="black", label="Average")


def run():
    plt.legend(handles=[red_patch, blue_patch, orange_patch, yellow_patch, black_patch])
    count = 0
    cnt = 0

    def gen_new_val(old_stock, stock_num):
        new_stock = random.uniform(7, 15)
        new_stock = round(new_stock, 2)
        neg_chance = random.randint(1, 100)
        if neg_chance % 3 == 0:
            new_stock = new_stock * -1
        stock[stock_num] = old_stock + new_stock
        stock[stock_num] = round(stock[stock_num], 2)
        return

    for num_stocks in range(4):
        t = random.uniform(50, 100)
        t = round(t, 2)
        stock.append(t)

    print(stock)

    while True:
        cnt_list.append(cnt)
        for iterate in range(4):
            APPL_y.append(stock[0])
            GOOG_y.append(stock[1])
            MSFT_y.append(stock[2])
            IBM_y.append(stock[3])
            common_x.append(count)
            gen_new_val(stock[iterate], iterate)
            count += 1

            average = stock[0] + stock[1] + stock[2] + stock[3]
            average = average / 4
            avg_y.append(average)

        print("APPL: " + str(stock[0]) + "\nGOOG: " + str(stock[1]) + "\nMSFT: " + str(stock[2]) + "\nIBM: " + str(
            stock[3]) + "\n")
        print(stock)
        plt.plot(common_x, APPL_y, c="red")
        plt.plot(common_x, GOOG_y, c="blue")
        plt.plot(common_x, MSFT_y, c="orange")
        plt.plot(common_x, IBM_y, c="yellow")
        plt.plot(common_x, avg_y, c="black")
        plt.show()
        plt.pause(0.01)
        time.sleep(0.5)
        plt.gcf()
        cnt += 1


run()
