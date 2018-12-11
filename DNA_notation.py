#!/usr/bin/python
# -*- coding: utf-8 -*-


def width_control(width, content, f):  # 定义控制输出到文件时的每行的宽度的函数
    for i in range(int(len(content) / width) + 1):
        start = i * width
        end = (i + 1) * width
        f.write('%s\n' % content[start:end])
    f.write("\n\n")


def bp_reverse(seq):  # 定义反向互补配对的函数
    seq = list(seq)
    seq.reverse()
    for i in range(len(seq)):
        if seq[i] == 'A':
            seq[i] = 'T'
            continue
        if seq[i] == 'T':
            seq[i] = 'A'
            continue
        if seq[i] == 'C':
            seq[i] = 'G'
            continue
        if seq[i] == 'G':
            seq[i] = 'C'
            continue
    seq = "".join(seq)
    return seq

# 建立密码子表字典


genetic_code = {
    'U': {
        'U': {'U': 'F', 'C': 'F', 'A': 'L', 'G': 'L'},
        'C': {'U': 'S', 'C': 'S', 'A': 'S', 'G': 'S'},
        'A': {'U': 'Y', 'C': 'Y', 'A': '', 'G': ''},
        'G': {'U': 'C', 'C': 'C', 'A': '', 'G': 'W'}
    },
    'C': {
        'U': {'U': 'L', 'C': 'L', 'A': 'L', 'G': 'L'},
        'C': {'U': 'P', 'C': 'P', 'A': 'P', 'G': 'P'},
        'A': {'U': 'H', 'C': 'H', 'A': 'Q', 'G': 'Q'},
        'G': {'U': 'R', 'C': 'R', 'A': 'R', 'G': 'R'}
    },
    'A': {
        'U': {'U': 'I', 'C': 'I', 'A': 'I', 'G': 'M'},
        'C': {'U': 'T', 'C': 'T', 'A': 'T', 'G': 'T'},
        'A': {'U': 'N', 'C': 'N', 'A': 'K', 'G': 'K'},
        'G': {'U': 'S', 'C': 'S', 'A': 'R', 'G': 'R'}
    },
    'G': {
        'U': {'U': 'V', 'C': 'V', 'A': 'V', 'G': 'V'},
        'C': {'U': 'A', 'C': 'A', 'A': 'A', 'G': 'A'},
        'A': {'U': 'D', 'C': 'D', 'A': 'E', 'G': 'E'},
        'G': {'U': 'G', 'C': 'G', 'A': 'G', 'G': 'G'}
    }
                }

fna = open(r'/home/lqm/python/data/NC_006270.fna', 'r')  # 读入fna文件
fna_data = fna.readlines()[1:]  # 去掉表头
chromosome = "".join(fna_data)  # 连成一条完整的DNA序列
chromosome = chromosome.replace("\n", "")  # 去掉换行符
ptt = open(r'/home/lqm/python/data/NC_006270.ptt', 'r')  # 读入ptt文件
ptt_data = ptt.readlines()[3:]  # 去掉表头
Location_start = [0]*len(ptt_data)  # 存放序列起始位置
Location_end = [0]*len(ptt_data)    # 存放序列终止位置
strand = ['0']*len(ptt_data)        # 存放正反链信息
product = ['0']*len(ptt_data)       # 存放序列产物名称
for i in range(len(ptt_data)):      # 遍历每行,取出对应信息
    Location_start[i] = int(ptt_data[i].split("\t")[0].split("..")[0])
    Location_end[i] = int(ptt_data[i].split("\t")[0].split("..")[1])
    strand[i] = ptt_data[i].split("\t")[1]
    product[i] = ptt_data[i].split("\t")[8]
start_codon = ['0']*len(ptt_data)   # 存放起始密码子
trans_DNA = ['0']*len(ptt_data)     # 存放用于下一步转录翻译的序列信息
result = file(r'/home/lqm/python/data/result.ffn', 'w')  # 结果写入result.ffn
for i in range(len(ptt_data)):
    if strand[i] == '+':
        result.write('from %d to %d %s %s\n' % (Location_start[i], Location_end[i], product[i], strand[i]))  # 写入每个片段的信息
        width_control(70, chromosome[(Location_start[i] - 1):(Location_end[i])], result)   # 将对应序列按70的长度写入文件
        start_codon[i] = chromosome[(Location_start[i] - 1):(Location_start[i]+2)]
        trans_DNA[i] = chromosome[(Location_start[i] - 1):(Location_end[i])]
    if strand[i] == '-':
        reverse_chromosome = bp_reverse(chromosome[(Location_start[i] - 1):(Location_end[i])])
        result.write('from %d to %d %s %s\n' % (Location_end[i], Location_start[i], product[i], strand[i]))
        width_control(70, reverse_chromosome, result)
        start_codon[i] = reverse_chromosome[0:3]
        trans_DNA[i] = reverse_chromosome
result.close()
print "ffn file is done!"
summary = {}
for s_c in start_codon:
    summary[s_c] = start_codon.count(s_c)  # 统计起始密码子种类和个数
print summary

result2 = file(r'/home/lqm/python/data/result.faa', 'w')  # 氨基酸序列结果写入result.faa
for i in range(len(ptt_data)):
    peptide = []
    for j in range(len(trans_DNA[i])/3):                  # 对每三个碱基翻译一个氨基酸
        trans_DNA[i] = trans_DNA[i].replace('T', 'U')
        peptide.append(genetic_code[trans_DNA[i][j*3]][trans_DNA[i][j*3+1]][trans_DNA[i][j*3+2]])  # 根据对应密码子表翻译
    result2.write('from %d to %d %s %s\n' % (Location_start[i], Location_end[i], product[i], strand[i]))
    width_control(70, "".join(peptide), result2)
result2.close()
print "faa file is done!"

