# -*- coding: utf-8 -*-
"""
HW 3 - Connor Smith


"""

#SETUP

import math

#create list for sequences
seq_list = []

#open doc
file_in = open('hw3.txt')

#open output doc
file_out = open('hw3_smith_output.txt','w')
file_out.write("HW3 Output Connor Smith\n")

#iterate through each line
for seq in file_in.read().split('\n'):
    # check to see length
    if len(seq) > 0:
        #add to seq_list if results
        seq_list.append(seq)

print(seq_list)

#close doc
file_in.close()

# Next, iterate through sequences
# Entropy Calculation

# Find number of sequences
num_seq = len(seq_list)
# Find length of MSA
seq_length = len(seq_list[0])

# Intialize Entropy Score
entropy_val = 0

#interate through each column
for col_idx in range(0,seq_length):
    # fill temporary list with value from each seq in column
    col_vals_temp = []
    for row_idx in range(0,num_seq):
        col_vals_temp.append(seq_list[row_idx][col_idx])
    # create set of unique values in column
    col_vals_set = set(col_vals_temp)
    # placeholder for column score
    col_score = 0
    # count how many times each one appears, calculate entropy an add to score
    for val in col_vals_set:
        # times in column
        times_in_col = col_vals_temp.count(val)
        # temp score
        score_temp = -(times_in_col/num_seq)*math.log10(times_in_col/num_seq)
        col_score += score_temp
    # add column score to entropy calc
    entropy_val += col_score

# Return result to screen
print("Entropy score of MSA: "+str(entropy_val))
file_out.write("Entropy score of MSA: "+str(entropy_val)+"\n")

# Last, calculate pairwise scoring
# Pairwise scoring

# Create scoring matrix using pandas
import pandas
# i first converted the scoring matrix from a text file to csv using excel
# mostly because I forgot how to properly do it
blosum62_file = open('blosum62.csv')
blosum62_matrix = pandas.read_csv(blosum62_file, index_col =0)

#create tuples of unique pairwise
pairwise_combos = []
for i in range(0,num_seq):
    for j in range(0,num_seq):
        # add combo to 
        pairwise_combos.append(sorted([i,j]))
# remove duplicates of combos
pairwise_unique = []
for item in pairwise_combos:
    if (item not in pairwise_unique and item[0] != item[1]):
        pairwise_unique.append(tuple(item))

#create dictionary of scores for comparisons
pairwise_scores = {}
#iterate through unique pairwise combos
for pw in pairwise_unique:
    pair_score = 0
    #iterate through each column
    for col_idx in range(0,seq_length):
        blosum_score = 0
        #check to see if both are a gap
        if (seq_list[pw[0]][col_idx] == '-' and seq_list[pw[1]][col_idx] == '-'):
            # do not score this column
            blosum_score = 0
        else:
            #score this column
            # note: the matrix uses the * symbol for a gap, so i must substitute in my string call
            seq1_val = seq_list[pw[0]][col_idx]
            seq2_val = seq_list[pw[1]][col_idx]
            blosum_score = blosum62_matrix[seq1_val.replace('-','*')][seq2_val.replace('-','*')]
        #add values from column to score
        pair_score += blosum_score
    # store scores for each pair in dictionary
    pairwise_scores[pw] = pair_score
#print results of each pair
for key,item in pairwise_scores.items():
    print("Pairwise for Seq" + str(key[0]+1) + " and Seq" + str(key[1]+1) + ": " + str(item))
    file_out.write("Pairwise for Seq" + str(key[0]+1) + " and Seq" + str(key[1]+1) + ": " + str(item)+"\n")
file_out.close()