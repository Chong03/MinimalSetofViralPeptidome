from Bio import SeqIO
import pandas as pd 
import ahocorasick as ahc

remain_Seq = list(SeqIO.parse("remainingSeq.fasta","fasta"))
remain_kmer = [line.rstrip('\n') for line in open ("remainingKmer.txt")]

def make_automaton(kmer_list):
    A = ahc.Automaton()  
    for kmer in kmer_list:
        A.add_word(kmer, kmer)
    A.make_automaton() 
    return A

def find_matching(line, A):
    found_kmers = []
    for end_index, kmer in A.iter(str(line)):
        found_kmers.append(kmer)
    return found_kmers

a = 0

while(len(remain_kmer) != 0):
    
    A = make_automaton(remain_kmer)
    
    matching_file = 'match/matching'+str(a)
    remain_kmer_file = 'match/remain_kmer'+str(a)
    
    # save matching to file
    with open(matching_file, 'w') as f:
        for index in range(len(remain_Seq)):
            x = remain_Seq[index].id
            y = find_matching(remain_Seq[index].seq, A)
            z = len(y)
            f.write(x + ';' + str(y) + ';' + str(z) + '\n')
    
    # read matching file and sorted by descending & some cleaning
    df = pd.read_csv(matching_file, delimiter=';', names=['sequence_id', 'matched_kmer', 'count']).sort_values(by='count',ascending=False, kind='mergesort')
    df['matched_kmer'] = df['matched_kmer'].str.replace(r"\[|\]|'","")
    
    # save highest count id to file
    fileZ = open('fileZ.txt', 'a')
    fileZ.write(df['sequence_id'].iloc[0] + '\n')
    
    # remove highest count kmer
    kmer_to_remove = df['matched_kmer'].iloc[0].split(', ')
    remain_kmer = list(set(remain_kmer) - set(kmer_to_remove))
    
    # save remain kmer to file
    with open(remain_kmer_file, 'w') as f:
     for i in remain_kmer:
         f.write(i + '\n')
         
    a = a + 1