import os
from functools import cmp_to_key
from xpinyin import Pinyin
pin = Pinyin()
numberset = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}

def cmpval(x, y):
    if(x > y):
        return 1
    elif(x < y):
        return -1
    else:
        return 0

def cmp_each(x, y):
    if x["priority"] != y["priority"]:
        return -cmpval(x["priority"], y["priority"])
    return cmpval(x["value"], y["value"])

def cmp(x, y):
    for i in range(min(len(x), len(y))):
        ret = cmp_each(x[i], y[i])
        if ret !=0:
            return ret
    # return
def proc_filename(x):
    x = x.replace("\n", "")
    ret = []
    pos = 0
    numbercache = ""
    while True:
        if pos >= len(x):
            break
        xlen = len(x[pos].encode("utf-8"))
        if xlen == 1:
            if x[pos] in numberset:
                # is number
                numbercache = ""
                while True:
                    numbercache += x[pos]
                    pos += 1
                    if (pos >= len(x)) or (x[pos] not in numberset):
                        break
                ret.append({"type":"number","priority": 100, "value": int(numbercache), "origin": str(numbercache)})
                continue
            else:
                # not number
                ret.append({"type": "ASCII", "priority": 50, "value": x[pos], "origin": x[pos]})
        else:
            ret.append({"type": "utf-8", "priority": 30, "value": pin.get_pinyin(x[pos]), "origin": x[pos]})
        pos += 1
            # non ascii character
    # for i in range(len(x)):
    #     xlen = len(x[i].encode("utf-8"))
    #     if xlen == 1: # ASCII only
    #         ret.append({"type": "ASCII", "value": x[i]})
    #     else:
    #         ret.append({"type": "UTF-8", "value":x[i]})
    return ret

def pnt(x):
    for i in range(len(x)):
        for j in range(len(x[i])):
            # for k in range(len(x[i][j])):
            print(x[i][j]["origin"], end="")
        print("", end=", ")
    print()

if __name__ == '__main__':
    # print(a > b)
    f = open("list", "r", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = proc_filename(lines[i])
        print(lines[i])
    print("Input:  ")
    pnt(lines)
    lines.sort(key = cmp_to_key(cmp))
    print("Output: ")
    pnt(lines)
