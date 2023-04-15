import bioread
import datetime
import numpy as np

import pandas

data = bioread.read_file("/Users/odayan/Downloads/NIH_Doors_sample_2222.acq")


df = pandas.DataFrame()
df['Time'] = data.channels[1].time_index

print(data.channels)
channelsData = pandas.DataFrame(data.channels)
print(channelsData)
print(data.channels[1])
print(data.channels[1].data)


# dataArray = np.array(data.channels[1].data).byteswap().newbyteorder()

df['Data'] = data.channels[1].data

df["Time"] = df["Time"].astype(float)
df["Time"] = df["Time"].round(3)
df = df.set_index("Time")

print(df)

gameDF = pandas.read_csv("./Df.csv")
gameDF["CurrentTime"] = gameDF["CurrentTime"].round(2)
gameDF = gameDF.set_index("CurrentTime")

print(df.dtypes)
print("============")
print(gameDF.dtypes)

mergedDF = gameDF.join(df)
#
# gameDF.set_index("CurrentTime").join(df.set_index("Time"))
print(mergedDF)
mergedDF.to_csv("./merged.csv")
