import matplotlib.pyplot as plot
import time


def sample_distant(x, y):
    z = ((x[0] - y[0])**2 + (x[1] - y[1])**2)**0.5
    return z


def seed_adjust(seed):
    if len(seed) == 1:
        return seed
    else:
        i = 0
        j = 0
        l = len(seed)
        while i != l-2 or j != l-1:
            l = len(seed)
            flag = False
            for i in range(len(seed) - 1):
                for j in range(i + 1, len(seed)):
                    if sample_distant(seed[i], seed[j]) < D:
                        seed.append([(seed[i][0] + seed[j][0]) / 2.0, (seed[i][1] + seed[j][1]) / 2.0])
                        seed.pop(i)
                        seed.pop(j-1)
                        flag = True
                        break
                if flag:
                    break
        return seed


def centerofgravity(sample_list):
    t1 = 0
    t2 = 0
    for s in sample_list:
        t1 = t1 + s[0]
        t2 = t2 + s[1]
    return [t1/len(sample_list), t2/len(sample_list)]


def classify(seed, sample, class_list):
    temp = []
    for se in seed:
        temp.append(sample_distant(se, sample))
    if min(temp) > d:
        seed.append(sample)
        class_list.append([sample])
    else:
        class_list[temp.index(min(temp))].append(sample)
        seed[temp.index(min(temp))] = centerofgravity(class_list[temp.index(min(temp))])
    return [seed, class_list]


start = time.clock()
data = open('/home/lqm/python/data/K-means data.txt', 'r')
sample_str = data.readlines()
sample_num = []
for i in range(len(sample_str)):
    sample_num.append(map(lambda x: float(x), sample_str[i].strip('\n').split('\t')))

k = 3
D = 3
d = 4
seed = sample_num[0:k]
seed = seed_adjust(seed)
class_list = [[] for i in range(len(seed))]
for i in range(len(seed)):
    class_list[i].append(seed[i])
for s in range(k):
    [seed, class_list] = classify(seed, sample_num[s], class_list)
for s in range(k, len(sample_num)):
    [seed, class_list] = classify(seed, sample_num[s], class_list)
    seed = seed_adjust(seed)


while True:
    class_list = [[] for i in range(len(seed))]
    '''
    for s_n in sample_num:
        temp = []
        for se in seed:
            temp.append(sample_distant(se, s_n))
        class_list[temp.index(min(temp))].append(s_n)
    '''
    for s_n in sample_num:
        [seed, class_list] = classify(seed, s_n, class_list)
        seed = seed_adjust(seed)
    new_seed = []
    for i in range(len(class_list)):
        new_seed.append(centerofgravity(class_list[i]))
    new_seed = seed_adjust(new_seed)
    if new_seed == seed:
        seed = new_seed
        break
    else:
        seed = new_seed

plot.figure('K-means')
ax = plot.gca()
ax.set_xlabel('x')
ax.set_ylabel('y')
color = ['r', 'k', 'g', 'b', 'y', 'm', 'pink', 'navy', 'orange']
for i in range(len(class_list)):
    x_list = []
    y_list = []
    for c in class_list[i]:
        x_list.append(c[0])
        y_list.append(c[1])
        ax.scatter(x_list, y_list, c=color[i], s=20, alpha=0.5)
for i in range(len(seed)):
    ax.scatter(seed[i][0], seed[i][1], s=50, c='yellow', marker='+')
plot.show()
end = time.clock()
print end-start

