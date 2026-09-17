# ============================================================
# 【函数（Function）】定义与调用 · 参数传递 · 匿名函数 lambda · return · 递归与嵌套
# 涉及知识点：def · 形参/实参 · 不可变 vs 可变对象传参 · 必备/关键字/默认/不定长参数
#            · *args / **kwargs · lambda · map / filter · 闭包 · / 和 * 分区 · 递归
# 运行方式：python 本文件名.py（无额外依赖）
# 隔离情况：printinfo 被重定义 4 次、printme / f / sum 各 2 次——每段都在自己定义后立刻调用，覆盖属安全；
#           max / sum / str 用作名字会遮蔽内置同名函数，本文件未再用内置版本，不报错；拆段单跑要用本段定义
# ============================================================

# 函数

## example 1
print("\n"+"="*60)                    # 输出分隔块（固定样式）：60 个 = 起头，先换行防止挤在上一行
print("【example 1】最简单的函数：def + 调用")
print("="*60)
def hello() :
    print("Hello World!")

hello()                       # 定义不执行函数体，这一行调用才真正跑 print
print("-"*60)                         # 输出收尾线（固定样式）

# 【本段知识点】
# 1. def 只是"定义"：函数体要等 hello() 被调用才执行，定义阶段屏幕上什么都没有。
# 2. 函数体必须缩进；空函数占位要写 pass，否则直接 IndentationError。
# 3. def hello() : 冒号前多个空格不报错，但规范写法是紧贴：def hello():。

## example 2
print("\n"+"="*60)
print("【example 2】带参数和返回值：自己实现 max")
print("="*60)
def max(a, b):
    if a > b:
        return a
    else:
        return b
a = 4
b = 5
print(max(a, b))              # return 的值顶替掉 max(a, b) 这个表达式，等价于 print(5)
print("-"*60)

# 【本段知识点】
# 1. return 把结果交回调用处并立刻结束函数；return 后面的代码不会再执行。
# 2. 函数里的 a、b 是形参，和外面的 a=4、b=5 是两个独立变量，只是把值传了进来。
# 3. 函数名叫 max 会遮蔽内置 max()（内置那个能 max(列表)）；本文件没再用内置版本所以不报错，自己写时别这么命名。

## example 3
print("\n"+"="*60)
print("【example 3】多函数协作：面积计算")
print("="*60)
# 计算面积函数
def area(width, height):
    return width * height
def print_welcome(name):
    print("Welcome", name)
print_welcome("Runoob")       # 先执行这个调用：打印 Welcome Runoob
w = 4
h = 5
print("width =", w, " height =", h, " area =", area(w, h))   # area(w, h) 被替换成 4*5=20 再打印
print("-"*60)

# 【本段知识点】
# 1. 一个文件可定义多个函数，函数间互相调用协作：area() 负责算，print_welcome() 负责打招呼。
# 2. area() 只 return 不打印，"算"和"显示"分开，是函数设计的好习惯。
# 3. 代码从上往下执行：先打印 Welcome 再打印 width/height/area，调用顺序决定输出顺序。

## 函数调用
print("\n"+"="*60)
print("【函数调用】同一函数调用两次")
print("="*60)
# 定义函数
def printme( str ):
    # 打印任何传入的字符串
    print (str)
    return
# 调用函数
printme("我要调用用户自定义函数!")
printme("再次调用同一函数")
print("-"*60)

# 【本段知识点】
# 1. 函数定义一次、可调用任意次：printme 被调用两遍，同一段逻辑反复复用。
# 2. 参数名写成 str 会遮蔽内置 str()，本 demo 没用到所以没事，实战别这么起名。
# 3. 单独一个 return（不带值）表示"提前结束函数"，等价于返回 None。

# 函数参数
## 传不可变对象实例
print("\n"+"="*60)
print("【传不可变对象实例】整数参数：函数内改不动外面")
print("="*60)
def change(a):
    print(id(a))   # 指向的是同一个对象
    a=10
    print(id(a))   # 一个新对象
a=1
print(id(a))
change(a)
print("-"*60)

# 【本段知识点】
# 1. 【API】id(obj) —— 作用：取对象的内存地址；参数：任意对象；返回：整数；同一对象的 id 相同。
# 2. 传参时内外指向同一个 1（id 相同）；函数内 a=10 后形参改指新地址（id 变了）——重新绑定，没动原对象。
# 3. 整数/字符串/元组这类"不可变对象"传进函数，函数内怎么改都影响不到外面。

## 传可变对象实例
print("\n"+"="*60)
print("【传可变对象实例】列表参数：函数内能改到外面")
print("="*60)
#!/usr/bin/python3
# 可写函数说明
def changeme( mylist ):
    "修改传入的列表"
    mylist.append([1,2,3,4])      # 【API】list.append(元素) —— 作用：把元素加到列表末尾；参数：要加的元素；返回：None（原地修改）
    print ("函数内取值: ", mylist)
    return
# 调用changeme函数
mylist = [10,20,30]
changeme( mylist )
print ("函数外取值: ", mylist)
print("-"*60)

# 【本段知识点】
# 1. 列表是"可变对象"：append 原地修改，函数内外看到同一个列表，所以外面也变了。
# 2. "函数内取值"和"函数外取值"打印出同样的内容，就是"改的是同一个东西"的证据。
# 3. 不想被函数改动就传副本：changeme(mylist[:])，原列表不受影响。
# 4. 文件中间的 #!/usr/bin/python3 只是普通注释（shebang 只对第一行生效），不影响运行。

# 参数
## 1. 必备参数
print("\n"+"="*60)
print("【必备参数】按顺序传参")
print("="*60)
def printinfo(name, age):
    "打印任何传入的字符串"
    print ("Name: ", name)
    print ("Age ", age)
    return

printinfo("Alice", 25) #按顺序传参
# printinfo()会报错
print("-"*60)

# 【本段知识点】
# 1. 必备参数必须按声明顺序传够数量：printinfo("Alice", 25) 即 name="Alice"、age=25。
# 2. 少传/多传都会 TypeError——下一行 # printinfo() 会报错 说的就是这个。
# 3. 函数第一行的字符串是文档字符串（docstring），会挂在 __doc__ 上，help(函数名) 能查到。

## 2. 关键字参数
print("\n"+"="*60)
print("【关键字参数】按名字传参")
print("="*60)
#可写函数说明
def printme( str ):
    "打印任何传入的字符串"
    print (str)
    return
#调用printme函数，传入关键字参数
printme( str = "菜鸟教程")
print("-"*60)

# 【本段知识点】
# 1. 关键字参数用 形参名=值 传参，顺序可乱、可读性好：printme(str="菜鸟教程")。
# 2. printme 在"函数调用"段已定义过一次，这里重新定义覆盖了它——覆盖发生在调用前，所以结果正确。

## 3. 默认参数
print("\n"+"="*60)
print("【默认参数】不传就用默认值")
print("="*60)
#可写函数说明
def printinfo( name, age = 35 ):
    "打印任何传入的字符串"
    print ("名字: ", name)
    print ("年龄: ", age)
    return
#调用printinfo函数
printinfo( age=50, name="runoob" )
print ("-"*60)        # ⚠️ 原为 print ("------------------------")，统一成固定分隔样式
printinfo( name="runoob" )
print("-"*60)

# 【本段知识点】
# 1. 带默认值的参数可以不传：printinfo(name="runoob") 时 age 自动用 35。
# 2. 关键字传参 + 默认值组合：printinfo(age=50, name="runoob") 两个都显式给、顺序随意。
# 3. 默认值在函数定义时只算一次：别用可变对象当默认值（如 age=[]），要用就写 None 再在函数内处理。

### 4. 不定长参数
print("\n"+"="*60)
print("【不定长参数 ①】*vartuple：多余参数打包成元组")
print("="*60)
# 可写函数说明
def printinfo( arg1, *vartuple ):
    "打印任何传入的参数"
    print ("输出: ")
    print (arg1)
    print (vartuple)
# 调用printinfo 函数
printinfo( 70, 60, 50 )
print("-"*60)

# 【本段知识点】
# 1. *vartuple 收集"多余的按位置传的参数"成元组：70 给 arg1，60、50 进 vartuple。
# 2. 打印 (60, 50) 说明 vartuple 是元组，不可变。
# 3. 这个版本没有 return，函数结束返回 None；调用处没接返回值，所以不影响。

print("\n"+"="*60)
print("【不定长参数 ②】*vartuple：for 逐个打印")
print("="*60)
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
print("-"*60)

# 【本段知识点】
# 1. 同样的 *vartuple，这次用 for 把元组里的参数逐个打印，而不是整体打印。
# 2. printinfo(10) 只传一个：vartuple 是空元组 ()，for 循环一次都不执行，只打印 10。
# 3. printinfo 在这里被第三次定义，覆盖前面所有版本——每段自给自足，顺序执行没问题。

print("\n"+"="*60)
print("【不定长参数 ③】**vardict：多余关键字打包成字典")
print("="*60)
def printinfo( arg1, **vardict ):
    "打印任何传入的参数"
    print ("输出: ")
    print (arg1)
    print (vardict)
# 调用printinfo 函数
printinfo(1, a=2,b=3)
print("-"*60)

# 【本段知识点】
# 1. **vardict 收集"多余的按关键字传的参数"成字典：a=2、b=3 进 vardict，打印出 {'a': 2, 'b': 3}。
# 2. 一个星 * 收位置参数，两个星 ** 收关键字参数，别混；名字可随便起（*args/**kwargs 是惯例），星号才是语法。
# 3. 这个 demo 同样没有 return，但不影响——调用处没接返回值。

def f(a,b,*,c):
    return a+b+c
f(1,2,c=3)        # 没有 print，返回值 6 被直接丢弃，所以这一段屏幕上看不到输出
# 【本段知识点】
# 1. 参数中间的单个 * 表示：它后面的参数（这里 c）只能按关键字传——f(1,2,c=3) 合法，f(1,2,3) 会报错。
# 2. return 的 6 没人接、没打印，等于白算；想看结果得改成 print(f(1,2,c=3))。

## 匿名函数
print("\n"+"="*60)
print("【匿名函数 ①】lambda 基本用法")
print("="*60)
sum = lambda arg1, arg2: arg1 + arg2     # lambda 参数: 表达式 —— 一行写完的小函数，返回表达式结果
# 调用sum函数
print ("相加后的值为 : ", sum( 10, 20 ))
print ("相加后的值为 : ", sum( 20, 20 ))
print("-"*60)

# 【本段知识点】
# 1. lambda 是一行版函数：lambda arg1, arg2: arg1 + arg2 等价于 def f(arg1, arg2): return arg1 + arg2。
# 2. 这里的 sum 遮蔽了内置 sum()，本段没用到内置版本所以没事，但别学这个命名。
# 3. lambda 只能写一个表达式，不能写多行语句（不能 if/for/赋值）；逻辑复杂就老老实实用 def。

print("\n"+"="*60)
print("【匿名函数 ②】map + lambda 批量变换")
print("="*60)
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))    # 【API】map(函数, 可迭代对象) —— 作用：把函数逐个作用到每个元素；参数：函数、可迭代对象；返回：惰性迭代器，要用 list() 逼出来
print(squared)  # 输出: [1, 4, 9, 16, 25]
print("-"*60)

# 【本段知识点】
# 1. map 把 lambda 逐个作用到 numbers 上：每个 x 都算 x**2。
# 2. map 返回的是惰性迭代器，必须 list() 包一层才能看到结果列表。
# 3. 这行等价于列表推导式 [x**2 for x in numbers]，两种写法选顺手的。

print("\n"+"="*60)
print("【匿名函数 ③】filter + lambda 筛选")
print("="*60)
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))    # 【API】filter(函数, 可迭代对象) —— 作用：按函数返回 True/False 决定元素去留；参数：函数、可迭代对象；返回：惰性迭代器
print(even_numbers)  # 输出：[2, 4, 6, 8]
print("-"*60)

# 【本段知识点】
# 1. filter 按 lambda 返回的 True/False 决定留不留：x % 2 == 0 为真才留下，筛出偶数。
# 2. 同样要 list() 逼出结果；等价于推导式 [x for x in numbers if x % 2 == 0]。
# 3. numbers 在这里被重新赋成新列表，和上一段互不干扰（同名覆盖，本段自给自足）。

print("\n"+"="*60)
print("【匿名函数 ④】闭包：函数返回函数")
print("="*60)
def myfunc(n):
    return lambda a : a * n      # 返回的不是结果，而是"函数本身"；lambda 记住了创建时的 n
mydoubler = myfunc(2)            # 拿到"乘以 2"的函数
mytripler = myfunc(3)            # 拿到"乘以 3"的函数
print(mydoubler(11))
print(mytripler(11))
print("-"*60)

# 【本段知识点】
# 1. myfunc 返回 lambda 函数本身：mydoubler = myfunc(2) 得到"乘以 2 的函数"。
# 2. 闭包：lambda 记住创建时的 n（2 或 3），所以 mydoubler(11)=22、mytripler(11)=33。
# 3. "函数造函数"是装饰器、偏函数等高级特性的地基。

## return 语句
print("\n"+"="*60)
print("【return 语句】返回值 vs 打印")
print("="*60)
def sum( arg1, arg2 ):
    # 返回2个参数的和."
    total = arg1 + arg2
    print ("函数内 : ", total)
#    return total
# 调用sum函数
total = sum( 10, 20 )
print ("函数外 : ", total)
print("-"*60)

# 【本段知识点】
# 1. return 被注释掉了：sum(10, 20) 返回 None，所以"函数外"的 total 打印出来是 None。
# 2. 对比"函数内: 30"和"函数外: None"：函数内是 print 出来的，函数外拿到的是返回值——两者不是一回事。
# 3. 这个 def sum 覆盖了前面的 lambda sum，也遮蔽内置 sum；真想求和别自己起名叫 sum。

## 强制位置参数和关键字参数
print("\n"+"="*60)
print("【强制位置/关键字参数】/ 与 * 三种分区")
print("="*60)
def f(a, b, /,   # ① / 之前：仅限位置形参
    c, d,      # ② / 和 * 之间：位置或关键字形参（普通形参）
    *,         # ③ * 之后：仅限关键字形参
    e, f):
    print(a, b, c, d, e, f)

f(10, 20, 30, d=40, e=50, f=60)
print("-"*60)

# 【本段知识点】
# 1. / 左边只能按位置传；* 右边只能按关键字传；两者中间是"位置或关键字都行"。
# 2. f(10, 20, 30, d=40, e=50, f=60)：a、b 位置传，c 也位置传（30），d、e、f 关键字传——全部符合规则。
# 3. 这个 f 覆盖了不定长参数段那个 f(a,b,*,c)，同名函数只有最后一个定义生效。

## 递归函数
print("\n"+"="*60)
print("【递归函数】自己调用自己")
print("="*60)
def tri_recursion(k):
    if(k > 0):
        result = k + tri_recursion(k - 1)   # 先递归到底，再一层层往回算、往回打印
        print(result)
    else:
        result = 0
    return result

tri_recursion(6)
print("-"*60)

# 【本段知识点】
# 1. 递归 = 函数自己调自己：tri_recursion(k) 先调 tri_recursion(k-1)，算到底再往回打印。
# 2. 必须有终止条件（else: result = 0），否则无限递归会报 RecursionError。
# 3. 输出 1、3、6、10、15、21 是 1~6 的累加和：每层 return 后打印一次，所以从小到大。

## 嵌套函数
print("\n"+"="*60)
print("【嵌套函数】函数里定义函数")
print("="*60)
def outer_function():
    print("外部函数被调用")
    def inner_function():
        print("内部函数被调用")
    inner_function()
    print("外部函数执行完毕")
    return "外部函数的返回值"

result = outer_function()
print(result)
print("-"*60)

# 【本段知识点】
# 1. 函数里可以再定义函数：inner_function 只在 outer_function 内部可见，外面直接调用会 NameError。
# 2. 执行顺序：打印"外部" → 定义内部函数 → 调用它 → 打印"执行完毕" → return 字符串。
# 3. 返回值被 result 接住再打印，所以"外部函数的返回值"出现在最后一行。

## 函数相互调用
print("\n"+"="*60)
print("【函数相互调用】a 调用 b")
print("="*60)
def b():
    print("函数b")

def a():
    print("函数a")
    b()   # a里面调用b，b已经定义好了 ✅

a()
print("-"*60)

# 【本段知识点】
# 1. 函数只要在"被调用的那一刻"已定义即可：a() 在最底部才调用，此时 b 早已定义完成，安全。
# 2. 顺序的真相：所有 def 先按顺序执行完（只是定义，不跑函数体），最后 a() 才真正运行。
# 3. 实战习惯：函数定义统一放前面、调用统一放后面，就不会踩"还没定义就调用"的坑。
