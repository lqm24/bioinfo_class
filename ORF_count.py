#!/usr/bin/python
# -*- coding: utf-8 -*-


def bp_reverse(seq):
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


def Find_ORF(wholeSeq):
    start = ['ATG']
    end = ['TAA', 'TGA', 'TAG']
    orfList = [[], [], []]
    for i in range(3):
        j = i
        while j < len(wholeSeq):
            if wholeSeq[j:(j + 3)] == start[0]:
                temp = ""
                while (wholeSeq[j:(j + 3)] not in end) and j < len(wholeSeq):
                    temp = temp + wholeSeq[j:(j + 3)]
                    j += 3
                temp = temp + wholeSeq[j:(j + 3)]
                if len(temp) > 120 and wholeSeq[j:(j + 3)] in end:
                    orfList[i].append(temp)
            else:
                j += 3
    return orfList


def FindoverlapORF(seq):
    start = ['ATG']
    smail_orf = [[], [], []]
    for i in range(len(seq)):
        for orf in seq[i]:
            if len(orf) > 123:
                j = 3
                while j < len(orf):
                    if orf[j:(j + 3)] == start[0] and len(orf[j:]) > 120:
                        smail_orf[i].append(orf[j:])
                        j += 3
                    else:
                        j += 3

    return smail_orf


data = open(r'/home/lqm/python/data/NC_006270.fna', 'r')
seq = data.readlines()[1:]
wholeSeq = ""
for i in range(len(seq)):
    wholeSeq = wholeSeq + seq[i].strip("\n")

forward_orf = Find_ORF(wholeSeq)
reverseWholeSeq = bp_reverse(wholeSeq)
reverse_orf = Find_ORF(reverseWholeSeq)
s_forward_orf = FindoverlapORF(forward_orf)
s_reverse_orf = FindoverlapORF(reverse_orf)
for i in range(3):
    print (len(forward_orf[i])+len(s_forward_orf[i]), len(reverse_orf[i])+len(s_reverse_orf[i]))
c1 = 0
c2 = 0
for i in range(3):
    c1 = c1+len(forward_orf[i])+len(s_forward_orf[i])
    c2 = c2+len(reverse_orf[i])+len(s_reverse_orf[i])
print(c1, c2)



