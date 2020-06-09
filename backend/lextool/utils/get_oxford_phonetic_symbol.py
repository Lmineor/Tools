import requests
import re
import MySQLdb
import time
import random
# 打开数据库连接
conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="words", charset='utf8')
cur = conn.cursor()



def get_phonetic_symbol(word):
    word = word.replace(" ", "_")
    time.sleep(random.uniform(0,1.1))
    request = requests.get("https://cn.bing.com/dict/search?q=" + word, timeout=5000)
    html = request.text

    regularExpression = r'<div\s+class="hd_prUS b_primtxt">美&#160;(.+?)</div>'  # /([^\/]*)/
    matchObject = re.search(regularExpression, html, re.I)

    phoneticSpelling = ""
    if matchObject:
        if matchObject.group(1):
            phoneticSpelling = matchObject.group(1)
    if phoneticSpelling.startswith('['):
        return phoneticSpelling
    else:
        return ''

def update_sql(sql):
    try:
        print(sql)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
def start():
    # 26575
    total = 103981
    # for sep in range(20, total//1000):
    #     for j in range(sep*1000, (sep+1)*1000):
    #         sql = "SELECT * FROM enwords WHERE id = %s" % j
    #         try:
    #             cur.execute(sql)
    #             # 获取所有记录列表
    #             result = cur.fetchone()
    #             spell = get_phonetic_symbol(result[0])
    #             sql_up = "UPDATE `enwords` SET `spelling` = '%s' WHERE `id` = %d" % (spell.replace('\'', '\\\''), j)
    #             update_sql(sql_up)
    #         except Exception as e:
    #             print (e)
    # for i in range(100000, 103982):
    #     sql = "SELECT * FROM enwords WHERE id = %s" % i
    #     try:
    #         cur.execute(sql)
    #         # 获取所有记录列表
    #         result = cur.fetchone()
    #         spell = get_phonetic_symbol(result[0])
    #         sql_up = "UPDATE `enwords` SET `spelling` = '%s' WHERE `id` = %d" % (spell.replace('\'', '\\\''), i)
    #         update_sql(sql_up)
    #     except Exception as e:
    #         print (e)

    # for i in range(287, 1000):
    #     sql = "SELECT * FROM enwords WHERE id = %s" % i
    #     try:
    #         cur.execute(sql)
    #         # 获取所有记录列表
    #         result = cur.fetchone()
    #         spell = get_phonetic_symbol(result[0])
    #         sql_up = "UPDATE `enwords` SET `spelling` = '%s' WHERE `id` = %d" % (spell.replace('\'', '\\\''), i)
    #         update_sql(sql_up)
    #     except Exception as e:
    #         print (e)

start()
if cur:
    cur.close()
if conn:
    conn.close()




# if __name__ == '__main__':
#     phonetic_symbol_text_dir = 'D:/github_project/make_anki_word_list/phonetic_symbol/phonetic_symbol.txt'
#     all_word_list = 'D:/github_project/make_anki_word_list/word_list/all.txt'
#     with open(all_word_list, 'r', encoding='utf-8') as f:
#         word_list = f.read().splitlines()
#     word_set = set(word_list)
#     word_set.discard('con')

#     # update txt ###################################################################################################
#     phonetic_symbol_line_list = list()
#     for word in tqdm(word_set, desc='decoding'):
#         phonetic_symbol = get_phonetic_symbol(word)
#         phonetic_symbol_line_list.append(word + '\\' + phonetic_symbol)

#     with open(phonetic_symbol_text_dir, 'w', encoding='utf-8') as f:
#         for line in phonetic_symbol_line_list:
#             f.write(line)
#             f.write('\n')