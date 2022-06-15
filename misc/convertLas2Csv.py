"""
By: Alvaro Bertin
06-2022

A program to convert las into csv with these columns:

x y z r g b

The rgb values are in 255 format.
"""
import laspy as lp
import numpy as np
import pandas as pd

def transform_colors(f):
    #https://github.com/strawlab/python-pcl/issues/171
    red = (f.red)
    green = (f.green)
    blue = (f.blue)
    # 16bit to convert 8bit data(data Storage First 8 bits case)
    red = np.right_shift(red, 8).astype(np.uint8)
    green = np.right_shift(green, 8).astype(np.uint8)
    blue = np.right_shift(blue, 8).astype(np.uint8)
    red = red.astype(np.uint32)
    green = green.astype(np.uint32)
    blue = blue.astype(np.uint32)

    return (red, green, blue)

def main1():
    input_path = "../data/"
    dataname = "MDS-"
    i = 1

    print("converting #" + str(i) + "...")

    las = lp.read(input_path + dataname + str(i) +".las")

    point_data = np.vstack((las.x, las.y, las.z)).transpose()
    red, green, blue = transform_colors(las)
    colors = np.vstack((red, green, blue, las.classification)).transpose()

    df = pd.DataFrame(data = point_data, columns=["x", "y", "z"])

    color = pd.DataFrame(data = colors, columns=["r", "g", "b", "class"])

    m = df.join(color)

    print(m.head(10))

def main():
    input_path = "../data/"
    dataname = "MDS-"

    for i in range(1, 12):

        print("converting #" + str(i) + "...")

        las = lp.read(input_path + dataname + str(i) +".las")

        point_data = np.vstack((las.x, las.y, las.z)).transpose()
        red, green, blue = transform_colors(las)
        colors = np.vstack((red, green, blue)).transpose()
        
        clas =  np.vstack(las.classification).transpose()

        df = pd.DataFrame(data= point_data, columns=["x", "y", "z"])

        color = pd.DataFrame(data= colors, columns=["r", "g", "b"])

        m = df.join(color)

        

        m.to_csv("LAS-" + str(i) + ".csv")

        print("DONE")


main1()