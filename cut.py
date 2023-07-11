#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将文本分类数据集分为训练集和测试集
@author: CSD
"""
import glob
import os
import random
import shutil
from threading import Thread, Lock
from queue import Queue


THREADLOCK = Lock()


def check_dir_exist(dir):
    # 坚持目录是否存在，不存在则创建
    if not os.path.exists(dir):
        os.mkdir(dir)


def copyfile(q):
    while not q.empty():
        full_folder, train, test, divodd = q.get()
        files = glob.glob(full_folder)
        filenum = len(files)
        testnum = int(filenum * divodd)
        testls = random.sample(list(range(filenum)), testnum)
        for i in range(filenum):
            if i in testls:
                shutil.copy(files[i], os.path.join(test, os.path.basename(files[i])))
            else:
                shutil.copy(files[i], os.path.join(train, os.path.basename(files[i])))
        with THREADLOCK:
            print(full_folder)


def data_divi(from_dir, to_dir, divodd=0.2):
    train_folder = os.path.join(to_dir, "train")
    test_folder = os.path.join(to_dir, "test")
    check_dir_exist(train_folder)
    check_dir_exist(test_folder)

    q = Queue()

    for basefolder in os.listdir(from_dir):
        if basefolder.startswith('.DS'):
            continue
        full_folder = os.path.join(from_dir, basefolder)
        print(basefolder)
        train = os.path.join(train_folder, basefolder)
        check_dir_exist(train)
        test = os.path.join(test_folder,basefolder)
        check_dir_exist(test)
        full_folder += "/*.txt"
        q.put((full_folder, train, test, divodd))

    for i in range(8):
        Thread(target=copyfile, args=(q,)).start()


if __name__ == "__main__":
    corpus_dir = './Corpus'
    exp_path = './NCorpus/'
    divodd = 0.2
    data_divi(corpus_dir, exp_path, divodd)