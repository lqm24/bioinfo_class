#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# max sum of non adjacent elements
def msna(tree_list):
    if len(tree_list) == 2:
        return max(tree_list)
    if len(tree_list) == 3:
        return max((tree_list[0] + tree_list[2]), tree_list[1])
    elif (msna(tree_list[:len(tree_list)-2]) + tree_list[len(tree_list)-1]) > msna(tree_list[:len(tree_list)-1]):
        return msna(tree_list[:len(tree_list)-2]) + tree_list[len(tree_list)-1]
    else:
        return msna(tree_list[:len(tree_list)-1])


msna([2, 7, 9, 3, 1, 2, 4, 2, 1, 2, 5, 6, 3, 6, 8, 2])


