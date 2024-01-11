import os

path = '/Users/omerdayan/Downloads/inst_E/'
i = 1
for file in os.listdir(path):
    new_name = f"instructions_E_{file[5:]}"
    source = path + file
    dest = path + new_name
    os.rename(source, dest)
    i += 1

path = '/Users/omerdayan/Downloads/inst_m/'
i = 1
for file in os.listdir(path):
    new_name = f"instructions_M_{file[5:]}"
    source = path + file
    dest = path + new_name
    os.rename(source, dest)
    i += 1

path = '/Users/omerdayan/Downloads/inst_f/'
i = 1
for file in os.listdir(path):
    new_name = f"instructions_F_{file[5:]}"
    source = path + file
    dest = path + new_name
    os.rename(source, dest)
    i += 1