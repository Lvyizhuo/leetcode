dict_01 = {'name':'lvyizhuo'}

print("#############字典基础##############")

# 打印字典
print(dict_01)

# 查看字典长度
print("Length:",len(dict_01))

# 查看字典类型
print(type(dict_01))

print("#############查看/引用字典里数值##############")
print(dict_01['name'])

print("#############修改字典################")
dict_02 = {'name':'lvyizhuo','age':'24'}
print(dict_02)

# 修改元素的数值
dict_02['name'] = 'whh'
print(dict_02)

# 增加元素
dict_02['shcool'] = 'xyu'
print(dict_02)

# 删除字典元素
del dict_02['name']
print(dict_02)

dict_03 = {'text':'1'}
print("使用str方法可以拼接字典的字符串:" + str(dict_03))
print('text' in dict_03)

# 清空字典
dict_02.clear()
print(dict_02)

# # 删除字典
# del dict_02
# print(dict_02)

##############字典特性######################
# 同一个键只能出现一次，出现两次会被第二次的数值覆盖
