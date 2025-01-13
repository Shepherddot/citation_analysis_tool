with open('paper_names0.txt', 'r') as f1:
    f1_filelist = f1.readlines()

with open('paper_names1.txt', 'r') as f2:
    f2_filelist = f2.readlines()

for i in f1_filelist:
    if i in f2_filelist:
        print(i.rstrip())