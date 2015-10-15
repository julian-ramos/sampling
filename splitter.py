import csv

def splitter(filename,path,prefix="random",lines=50000):
    """
    Splits the data set into a number of subsets.
    filename : Original file to split
    path : path to where the files are going to be stored
    prefix : This is the name for each of the subsets plus a number for instance
    if prefix = subset then the stored file name will be subset_1.tsv, subset_2.tsv ....
    lines : Number of lines to be stored on each file created, the last file will always have at
    most this number of lines
    """
    
    input_file = open(filename, 'r')
    input_reader = csv.reader(input_file, delimiter="\t")
    output_file=open(path+"/"+prefix+"_1.tsv","w")
    output_writer=csv.writer(output_file,delimiter="\t")
    count=0
    filenum=1
    files=[]
    for row in input_reader:
        output_writer.writerow(row)
        count+=1
        if count==lines:
            count=0
            output_file.close()
            filenum+=1
            filename=path+"/"+prefix+"_%d.tsv"%(filenum)
            output_file=open(filename,"w")
            output_writer=csv.writer(output_file,delimiter="\t")
            files.append(filename)
    input_file.close()
    return files
    
    
if __name__=="__main__":
    filename="/Users/ingenia/git/data/data_sampling/user_bot_Data.tsv"
    path="/Users/ingenia/git/data/data_sampling/splits"
    prefix="split_data"
    splitter(filename,path,prefix,100000)
    