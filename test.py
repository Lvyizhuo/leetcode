str = 'eat'
print(sorted(str))  # ['a', 'e', 't'] —— sorted() 返回排序后的列表，原字符串不动
key = ''.join(sorted(str))  # ''.join() 把列表拼成字符串
print(key)  # 'aet' —— 排序后的字符串作为哈希表的

hashmap = {key:1 ,'name':'lvyzihzuo' }
print (list((hashmap.values())))