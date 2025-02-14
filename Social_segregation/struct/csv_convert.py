# 读取读取CSV文件，提取其中Theme1,Theme2, Theme3,Theme4,和Themes 到一个新的CSV文件中

import csv
import os

def read_csv_fold(csv_fold,output_path):
    for file in os.listdir(csv_fold):
        if file.endswith(".csv"):
            csv_path = os.path.join(csv_fold,file)
            with open(csv_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                #读取第二行
                for i,row in enumerate(csv_reader):
                    if i ==1:
                        print(row)
                        #提取Theme1,Theme2, Theme3,Theme4,和Themes
                        city_name=row[0]
                        theme1 = row[2]
                        theme2 = row[3]
                        theme3 = row[4]
                        theme4 = row[5]
                        themes = row[6]
                        #写入到新的CSV文件中
                        with open(output_path, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([city_name,theme1,theme2,theme3,theme4,themes])

if __name__ == '__main__':
    csv_fold = r"D:\date\social segregation\SSI\Data\Step2_SSI\Global"
    output_path = r"../data/SSI_golbal_data.csv"
    read_csv_fold(csv_fold,output_path)

