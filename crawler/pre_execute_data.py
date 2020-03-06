# coding = utf-8

import os
import hashlib
import random

path = "../resources/lyrics/JayChou/"

def run():
    ls = os.listdir(path)
    ls.remove("all_lyrics.txt")
    ls.remove("download")
    for file_name in ls:
        print("------{}------".format(file_name))
        temp_file = "__" + file_name
        lines = []
        lines_md5 = {}
        with open(path + file_name, "r", encoding="utf-8") as file_in:
            contents = file_in.read().split("\n\n\n")
            for content in contents:
                content = content.strip()
                if len(content) > 0:
                    hash = hashlib.md5(content.encode()).hexdigest()
                    if hash not in lines_md5:
                        lines_md5[hash] = True
                        lines.append(content)
        with open(path + temp_file, "w", encoding="utf-8") as file_out:
            for line in lines:
                file_out.write(line)
                file_out.write("\n\n")
        os.remove(path + file_name)
        os.rename(path + temp_file, path + file_name)

def merge():
    merge_file_name = "all_lyrics.txt"
    ls = os.listdir(path)
    ls.remove("all_lyrics.txt")
    ls.remove("download")
    lines = []
    lines_md5 = {}
    for file_name in ls:
        print("------{}------".format(file_name))
        with open(path + file_name, "r", encoding="utf-8") as file_in:
            contents = file_in.read().split("\n\n")
            for content in contents:
                content = content.strip()
                if len(content) > 0:
                    hash = hashlib.md5(content.encode()).hexdigest()
                    if hash not in lines_md5:
                        lines_md5[hash] = True
                        lines.append(content)
    print(len(lines))
    with open(path + merge_file_name, "w", encoding="utf-8") as file_out:
        for line in lines:
            file_out.write(line)
            file_out.write("\n\n")


def shuffle():
    shuffle_file_name = "all_lyrics.txt"
    temp_file = "__" + shuffle_file_name

    with open(path + shuffle_file_name, "r", encoding="utf-8") as file:
        lines = file.read().split("\n\n")
    random.shuffle(lines)
    with open(path + temp_file, "w", encoding="utf-8") as file:
        for line in lines:
            if len(line) <= 0:
                continue
            file.write(line)
            file.write("\n\n")
    os.remove(path + shuffle_file_name)
    os.rename(path + temp_file, path + shuffle_file_name)


if __name__ == "__main__":
    # run()
    # merge()
    shuffle()