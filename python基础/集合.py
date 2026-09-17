# 集合的基础
parame = {1,2,3,4}
print(parame)





# set()把（）里面的类型转换成集合，如“列表[]”,“集合{}”
parame_02 = set((1,2,3,4))
print(parame_02)
print(type(parame_02))


# 集合之间的运算
a = set('lvyizhuo')		
b = set('lvonezhuo')

print(a)
print(b)
print(a - b)		# 集合a中包含而集合b中不包含的元素
print(a | b)		# 集合a或b中包含的所有元素
print(a & b)		# 集合a和b中都包含了的元素
print(a ^ b)		# 不同时包含于a和b的元素

# 集合的操作
parame_03 = set('123')

parame_03.add(4)		# add x to sets
print(parame_03)

parame_03.remove(4)		# remove x from sets
print(parame_03)

parame_03.pop()
print(parame_03)		# 随机 remove 一个元素

print(len(parame_03))	# compute sets's length

parame_03.clear()		# claer sets
print(parame_03)		# 空集合

parame_03.add('1234')
print(parame_03)
print('1234' in parame_03)


parame_03 = set('1234')
print(parame_03)
print('1' in parame_03)

parame_03.discard('1')
print(parame_03)


















