import lzw
import pandas as pd
import glob, os
from datetime import datetime
import csv

def compress1(uncompressed):
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result

def custom_compressor(data):
    compressed_list = compress1(data)
    return str(float(len(data)-len(list(compress1(data))))/float(len(data))*100)
def library_compressor(data):
    return str(float(len(data)-len(list(lzw.compress(lzw.ByteEncoder(12).encodetobytes(data)))))/float(len(data))*100)
def lexicalDensity(message):
  list_words = message.split()
  words = float(len(list_words))
  uWords = float(len(set(list_words)))
  return (words-(uWords))/(words)*100

# with open('test.txt', 'r') as myfile:
#     data=myfile.read().replace('\n', ' ')

# compressed_list = compress1(data)

# reduced_str = ''
# for i in range(len(compressed_list)):
#     if(isinstance(compressed_list[i],basestring)): 
#         reduced_str+=compressed_list[i]
#     else:
#         reduced_str+='*'
# print data
# print reduced_str

# print str(float(len(data)-len(list(lzw.compress(lzw.readbytes('test.txt')))))/float(len(data))*100) + "% compressed"
# print str(float(len(data)-len(list(lzw.compress(lzw.readbytes('test2.txt')))))/float(len(data))*100) + "% compressed"
# print str(lexicalDensity(data))
# print str(lexicalDensity(open('test.txt','r').read().replace('\n',' ')))

party_dict = {'Abraham_Lincoln' : 'Republican', 'Andrew_Jackson' : 'Democrat', 'Andrew_Johnson' : 'Union', 'Barack_Obama' : 'Democrat', 'Benjamin_Harrison' : 'Republican', 'Bill_Clinton' : 'Democrat', 'Calvin_Coolidge' : 'Republican', 'Chester_A._Arthur' : 'Republican', 'Donald_Trump' : 'Republican', 'Dwight_D._Eisenhower' : 'Republican', 'Franklin_D._Roosevelt' : 'Democrat', 'Franklin_Pierce' : 'Democrat', 'George_H._W._Bush' : 'Republican', 'George_W._Bush' : 'Republican', 'George_Washington' : 'Federalist', 'Gerald_Ford' : 'Republican', 'Grover_Cleveland' : 'Democrat', 'Harry_S._Truman' : 'Democrat', 'Herbert_Hoover' : 'Republican', 'James_A._Garfield' : 'Republican', 'James_Buchanan' : 'Democrat', 'James_K._Polk' : 'Democrat', 'James_Madison' : 'Democratic-Republican', 'James_Monroe' : 'Democratic-Republican', 'Jimmy_Carter' : 'Democrat', 'John_Adams' : 'Federalist', 'John_F._Kennedy' : 'Democrat', 'John_Quincy_Adams' : 'Democratic-Republican', 'John_Tyler' : 'Whig', 'Lyndon_B._Johnson' : 'Democrat', 'Martin_Van_Buren' : 'Democrat', 'Millard_Fillmore' : 'Whig', 'Richard_Nixon' : 'Republican', 'Ronald_Reagan' : 'Republican', 'Rutherford_B._Hayes' : 'Republican', 'Theodore_Roosevelt' : 'Republican', 'Thomas_Jefferson' : 'Democratic-Republican', 'Ulysses_S._Grant' : 'Republican', 'Warren_G._Harding' : 'Republican', 'William_Harrison' : 'Whig', 'William_McKinley' : 'Republican', 'William_Taft' : 'Republican', 'Woodrow_Wilson' : 'Democrat', 'Zachary_Taylor' : 'Whig'}

name_list = []
party_list = []
date_list = []
custom_compress_list = []
library_compress_list = []
lexical_list = []
length_list = []

os.chdir("Speeches_Master/")
for file in glob.glob("*.txt"):
    split_file = (file).split("_")
    name_list.append(file.replace((split_file)[len(split_file)-1],'')[:-1])
    party_list.append(party_dict[file.replace((split_file)[len(split_file)-1],'')[:-1]])
    f = open(file,'r')
    date_str = datetime.strptime(f.readline().replace('\n',''), '%B %d, %Y') - datetime.strptime('January 01 1789', '%B %d %Y')
    date_list.append(int(date_str.days))
    data = f.read().strip().replace('\n', ' ')
    custom_compress_list.append(custom_compressor(data))
    library_compress_list.append(library_compressor(data))
    lexical_list.append(lexicalDensity(data))
    length_list.append(len(data))

full_data = []
full_data.append(name_list)
full_data.append(party_list)
full_data.append(date_list)
full_data.append(custom_compress_list)
full_data.append(library_compress_list)
full_data.append(lexical_list)
full_data.append(length_list)

df = pd.DataFrame(full_data).T
df.columns = ['Name', 'Party.Affiliation', 'Days.since.Jan.01.1789', 'Custom.Compression.Percentage', 'Library.Compression.Percentage', 'Unique.Word.Count.Percentage', 'Character.Length']
df.to_csv("output.csv",)

# headers = ['Name', 'Party.Affiliation', 'Days.since.Jan.01.1789', 'Custom.Compression.Percentage', 'Library.Compression.Percentage', 'Unique.Word.Count.Percentage']
# df = pd.read_csv("Speeches_Master/output.csv", names=headers)
# x = df['Days.since.Jan.01.1789']
# y = df['Library.Compression.Percentage']
# plt.plot(x,y)
# plt.show()