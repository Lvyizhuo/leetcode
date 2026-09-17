# 函数

## example 1
def hello() :
    print("Hello World!")

hello()

## example 2
def max(a, b):
    if a > b:
        return a
    else:
        return b
 
a = 4
b = 5
print(max(a, b))

## example 3
# 计算面积函数
def area(width, height):
    return width * height
 
def print_welcome(name):
    print("Welcome", name)
 
print_welcome("Runoob")
w = 4
h = 5
print("width =", w, " height =", h, " area =", area(w, h))

## 函数调用
# 定义函数
def printme( str ):
   # 打印任何传入的字符串
   print (str)
   return
 
# 调用函数
printme("我要调用用户自定义函数!")
printme("再次调用同一函数")

# 函数参数
## 传不可变对象实例
def change(a):
    print(id(a))   # 指向的是同一个对象
    a=10
    print(id(a))   # 一个新对象
 
a=1
print(id(a))
change(a)

## 传可变对象实例

#!/usr/bin/python3
 
# 可写函数说明
def changeme( mylist ):
   "修改传入的列表"
   mylist.append([1,2,3,4])
   print ("函数内取值: ", mylist)
   return
 
# 调用changeme函数
mylist = [10,20,30]
changeme( mylist )
print ("函数外取值: ", mylist)

# 参数
## 1. 必备参数
def printinfo(name, age):
   "打印任何传入的字符串"
   print ("Name: ", name)
   print ("Age ", age)
   return

printinfo("Alice", 25) #按顺序传参
# printinfo()会报错

## 2. 关键字参数
 
#可写函数说明
def printme( str ):
   "打印任何传入的字符串"
   print (str)
   return
 
#调用printme函数，传入关键字参数
printme( str = "菜鸟教程")

## 3. 默认参数
#可写函数说明
def printinfo( name, age = 35 ):
   "打印任何传入的字符串"
   print ("名字: ", name)
   print ("年龄: ", age)
   return
 
#调用printinfo函数
printinfo( age=50, name="runoob" )
print ("------------------------")
printinfo( name="runoob" )

### 4. 不定长参数
# 可写函数说明
def printinfo( arg1, *vartuple ):
   "打印任何传入的参数"
   print ("输出: ")
   print (arg1)
   print (vartuple)
 
# 调用printinfo 函数
printinfo( 70, 60, 50 )

def printinfo( arg1, *vartuple ):
   "打印任何传入的参数"
   print ("输出: ")
   print (arg1)
   for var in vartuple:
      print (var)
   return
 
# 调用printinfo 函数
printinfo( 10 )
printinfo( 70, 60, 50 )

def printinfo( arg1, **vardict ):
   "打印任何传入的参数"
   print ("输出: ")
   print (arg1)
   print (vardict)
 
# 调用printinfo 函数
printinfo(1, a=2,b=3)

def f(a,b,*,c):
    return a+b+c
f(1,2,c=3)

## 匿名函数
sum = lambda arg1, arg2: arg1 + arg2
 
# 调用sum函数
print ("相加后的值为 : ", sum( 10, 20 ))
print ("相加后的值为 : ", sum( 20, 20 ))

numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # 输出: [1, 4, 9, 16, 25]

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # 输出：[2, 4, 6, 8]

def myfunc(n):
  return lambda a : a * n
 
mydoubler = myfunc(2)
mytripler = myfunc(3)
 
print(mydoubler(11))
print(mytripler(11))

## return 语句
def sum( arg1, arg2 ):
   # 返回2个参数的和."
   total = arg1 + arg2
   print ("函数内 : ", total)
#    return total
 
# 调用sum函数
total = sum( 10, 20 )
print ("函数外 : ", total)

## 强制位置参数和关键字参数
def f(a, b, /,   # ① / 之前：仅限位置形参
      c, d,      # ② / 和 * 之间：位置或关键字形参（普通形参）
      *,         # ③ * 之后：仅限关键字形参
      e, f):
    print(a, b, c, d, e, f)

f(10, 20, 30, d=40, e=50, f=60)

## 递归函数
def tri_recursion(k):
  if(k > 0):
    result = k + tri_recursion(k - 1)
    print(result)
  else:
    result = 0
  return result

tri_recursion(6)

## 嵌套函数
def outer_function():
    print("外部函数被调用")
    def inner_function():
        print("内部函数被调用")
    inner_function()
    print("外部函数执行完毕")
    return "外部函数的返回值"

result = outer_function()
print(result)

## 函数相互调用
def b():
    print("函数b")

def a():
    print("函数a")
    b()   # a里面调用b，b已经定义好了 ✅

a()

