import jieba
import os
from threading import Thread, Lock
from queue import Queue

userdict = './userdict.txt'
jieba.load_userdict(userdict)
LOCK = Lock()

def readfile(filepath, encoding='utf-8'):
    # 读取文本
    with open(filepath, "rt", encoding=encoding) as fp:
        content = fp.read()
    return content


def savefile(savepath, content):
    # 保存文本
    with open(savepath, "wt") as fp:
        fp.write(content)
        
def check_dir_exist(dir):
    # 坚持目录是否存在，不存在则创建
    if not os.path.exists(dir):
        os.mkdir(dir)

def text_segment(q):
    """
    对一个类别目录下进行分词
    """
    while not q.empty():
        from_dir, to_dir = q.get()
        with LOCK:
            print(from_dir)
        files = os.listdir(from_dir)
        for name in files:
            if name.startswith('.DS'):
                continue
            from_file = os.path.join(from_dir, name)
            to_file = os.path.join(to_dir, name)

            content = readfile(from_file)
            seg_content = jieba.cut(content)
            savefile(to_file, ' '.join(seg_content))


def corpus_seg(curpus_path, seg_path):
    """对文本库分词，保存分词后的文本库,目录下以文件归类 curpus_path/category/1.txt, 保存为 seg_path/category/1.txt"""
    check_dir_exist(seg_path)
    q = Queue()
    cat_folders = os.listdir(curpus_path)
    for folder in cat_folders:
        from_dir = os.path.join(curpus_path, folder)
        to_dir = os.path.join(seg_path, folder)
        check_dir_exist(to_dir)

        q.put((from_dir, to_dir))

    for i in range(len(cat_folders)):
        Thread(target=text_segment, args=(q,)).start()
if __name__ == '__main__':
    # 分词
    data_dir = './NCorpus/'
    corpus_seg(data_dir + 'train/', data_dir + 'train_seg')
    corpus_seg(data_dir + 'test/', data_dir + 'test_seg')