# ============================================================
# 【迭代器与生成器】iter() / next() 三种遍历写法 + 自定义迭代器 + yield 生成器
# 涉及知识点：可迭代对象 vs 迭代器 · iter() · next() · StopIteration · __iter__/__next__
#            · 生成器（Generator）· yield · 惰性求值
# 运行方式：python 本文件名.py（无额外依赖）
# 隔离情况：5 段 demo 互相独立；it 在 example 1/2/3 里各被重新赋值一次，属安全覆盖；
#           两个迭代器类已用 _2 后缀区分；sys 在 example 3 和生成器 example 2 各导了一次，互不依赖
# ============================================================

# ================ 【example 1】手动 next()：一个元素一个元素地取 ================
print("\n"+"="*60)                    # 输出分隔块（固定样式）：60 个 = 起头，先换行防止挤在上一行
print("【example 1】手动 next()：一个元素一个元素地取")
print("="*60)
# example1
lst = [1,2,3,4]
it = iter(lst)      # 【API】iter(obj) —— 作用：把列表这类"可迭代对象"包装成迭代器；参数：任意可迭代对象；返回：迭代器对象
print(next(it))     # 【API】next(it) —— 作用：取出迭代器里的下一个元素，内部指针自动后移；参数：迭代器（可选再传一个"取不到时的默认值"）；返回：下一个元素
print(next(it))     # 第二次取值拿到 2：进度记在 it 身上，不是记在 lst 身上
print("-"*60)       # ⚠️ 原为 print("-"*20)，统一成固定分隔样式；这是 example 1 的输出收尾线（全文件第一次出现，后面几处不再标注）

# 【本段知识点】
# 1. 列表是"可迭代对象"不是"迭代器"：能被 for 遍历，但不能直接 next()，得先用 iter() 转换。
# 2. 迭代器只进不退：指针一路向前，取过的元素拿不回来，想重来必须重新 iter()。
# 3. next() 取到尽头会抛 StopIteration，所以 example 3 要用 try 把它接住。

# ================ 【example 2】把迭代器交给 for 循环 ================
print("\n"+"="*60)
print("【example 2】把迭代器交给 for 循环")
print("="*60)
# example 2
list_2 = [1,2,3,4]
it = iter(list_2)      # 同名覆盖：it 被重新指向 list_2 的新迭代器，example 1 那个就此丢弃；本段自给自足，两段互不干扰
for x in it:           # for 的底层就是反复调 next(it)，直到捕获 StopIteration 才安静退出，所以不用自己写 try
    print(x,end=' ')   # end=' ' 改写结尾字符：默认是换行，这里换成空格，输出就挤在一行
print("\n"+"-"*60)     # ⚠️ 原为 print("\n"+"-"*20)，宽度统一成 60；"\n" 必须保留，因为上一行用 end=' ' 没有换行

# 【本段知识点】
# 1. for 遍历迭代器和手动 next() 是同一件事，for 只是帮你把异常处理藏起来了。
# 2. 迭代器是一次性的：for 会把它整个消费掉。这里重新 iter(list_2) 造了全新迭代器，所以从头输出 1、2、3、4；若把 example 1 那只已取到一半的 it 丢给 for，会从 3 接着取。
# 3. print 的 end 参数默认是 '\n'，换掉它就能控制不换行输出。

# ================ 【example 3】while + try 手动接住 StopIteration ================
print("\n"+"="*60)
print("【example 3】while + try 手动接住 StopIteration")
print("="*60)
# example 3
import sys                    # 本例还没用到 sys，真正用到它在最后的生成器 example 2；惯例上 import 统一放文件开头
list_3 = [1,2,3,4]
it = iter(list_3)             # 同样是自己重新 iter()，不是沿用 example 2 的 it
while True:                   # 死循环，靠下面 except 里的 break 跳出
    try:
        print(next(it))       # 正常取值：依次打印 1、2、3、4
    except StopIteration:     # 迭代器取空后 next() 抛的就是这个异常，接住它
        break                 # 取空即跳出，等价于 for 的自动行为
print("-"*60)

# 【本段知识点】
# 1. try/except StopIteration + break = 手写版的 for 循环，看懂它才算真懂 for 干了什么。
# 2. except 只接你想接的异常：写 StopIteration 而不是光溜溜的 except:，否则别的错误会被一起吞掉。
# 3. import 语句写在中途也能用，但惯例是统一放文件开头。

# ================ 【自定义迭代器 example 1】无限迭代器：__iter__ + __next__ ================
print("\n"+"="*60)
print("【自定义迭代器 example 1】无限迭代器：__iter__ + __next__")
print("="*60)
# 创建迭代器 example1（无限迭代器演示）
class MyNumbers:              # 自定义迭代器必须同时实现 __iter__ 和 __next__
    def __iter__(self):       # 【API】__iter__(self) —— 作用：返回迭代器本身，for / iter() 第一步就调它；参数：self；返回：self
        self.a = 1            # 计数器挂在实例上；若写成类属性，多个实例会共用一份数据
        return self
    def __next__(self):       # 【API】__next__(self) —— 作用：定义"取下一个"的规则；返回：下一个值；取完时必须 raise StopIteration
        x = self.a
        self.a += 1
        return x              # 没有终止条件 → 取之不尽，所以叫无限迭代器
myclass = MyNumbers()
myiter = iter(myclass)
print(next(myiter))           # 1
print(next(myiter))           # 2
print(next(myiter))           # 3
print(next(myiter))           # 4
print(next(myiter))           # 5
print("-"*60)

# 【本段知识点】
# 1. 类只要实现了 __iter__ 和 __next__，它的实例就是迭代器，能被 next() 和 for 使用——这就是迭代协议。
# 2. iter(对象) 实际去调 __iter__()；next(对象) 实际去调 __next__()，两件事要分清。
# 3. __next__ 不抛 StopIteration 的后果：只能手动 next() 有限次，一旦丢给 for 就会无限循环卡死。

# ================ 【自定义迭代器 example 2】有限迭代器：补上终止条件 ================
print("\n"+"="*60)
print("【自定义迭代器 example 2】有限迭代器：补上终止条件")
print("="*60)
# 创建迭代器 example2 有限迭代器
class MyNumbers_2:            # 用户自己加的 _2 后缀：与上面的 MyNumbers 区分，两个类不会互相覆盖
    def __iter__(self):
        self.a = 1
        return self
    def __next__(self):
        if self.a <= 20:      # 还没到 20 就正常返回
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration   # 【API】raise StopIteration —— 作用：显式宣告"取完了"，让 for 正常收尾，不算报错；参数：无
myclass_2 = MyNumbers_2()
myiter_2 = iter(myclass_2)
for x in myiter_2:            # 因为是有限的，交给 for 遍历很安全，会依次打印 1~20
    print(x)
print("-"*60)

# 【本段知识点】
# 1. 无限迭代器和有限迭代器的唯一区别：__next__ 里有没有终止条件。
# 2. StopIteration 是"正常结束"的信号，不是错误；for 接住它就直接退出，程序不会崩。
# 3. 写成 self.a <= 20 而不是 < 20，这种边界差一（off-by-one）是实践中最常见的 bug。

# 生成器
# ================ 【生成器 example 1】yield 让函数"暂停再续"：countdown 倒数 ================
print("\n"+"="*60)
print("【生成器 example 1】yield 让函数“暂停再续”：countdown 倒数")
print("="*60)
## example 1
def countdown(n):             # 函数体里有 yield → 这就是"生成器函数"：调用它不会执行，只返回一个生成器对象
    while n > 0:
        yield n               # 【API】yield 值 —— 作用：暂停函数并把值交出去，下次 next() 从这一行接着跑；参数：要交出的值；副作用：连同局部变量一起记住执行位置
        n -= 1                # 重新进入后从 yield 的下一行继续，n 在这里递减
# 创建生成器对象
generator = countdown(5)      # 调用生成器函数一行代码都不跑，只拿到生成器对象，值全没算
# 通过迭代生成器获取值
print(next(generator))  # 输出: 5
# next() 第一次触发执行：函数跑到第一个 yield 暂停，交出 5
print(next(generator))  # 输出: 4
# 第二次 next()：从上次暂停的 yield 之后接着跑，n 减到 4，再交出 4
print(next(generator))  # 输出: 3
# 第三次：交出 3，函数还剩 2、1 没算
# 使用 for 循环迭代生成器
for value in generator:       # for 接手剩余进度：自动 next 到底，无需手动调用
    print(value)  # 输出: 2 1
print("-"*60)

# 【本段知识点】
# 1. yield 是"暂停并交出"：函数状态（局部变量、执行到哪一行）被完整保存，下次 next() 原地续跑——这是生成器与普通函数最大的区别。
# 2. 生成器对象本身就是迭代器：能 next() 也能 for，所以前面那套迭代协议对生成器同样成立。
# 3. 值不是一次性算好的，是"边要边算"：下一个值只在 next() 时才现算，这叫惰性求值（Lazy Evaluation）。

# ================ 【生成器 example 2】无限斐波那契：yield 在循环里 ================
print("\n"+"="*60)
print("【生成器 example 2】无限斐波那契：yield 在循环里")
print("="*60)
## example 2
import sys                    # 同一个模块可以重复导入，不会报错；惯例上开头导一次就够
def fibonacci(n): # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0   # 一次赋好三个变量：a 是当前值，b 是下一个值，counter 数已交出的个数
    while True:
        if (counter > n):     # 已交出超过 n 个，该收场了
            return            # return 不带值 = 抛 StopIteration，正好是迭代结束的信号
        yield a               # 交出当前的 a（0、1、1、2、3…），函数在这里暂停
        a, b = b, a + b       # 滚动赋值：新 a 用旧 b，新 b 用旧 a+旧 b，一步推进数列
        counter += 1

f = fibonacci(10) # f 是一个迭代器，由生成器返回生成
while True:
    try:
        print (next(f), end=" ")
    except StopIteration:     # 生成器里 return 时会抛 StopIteration，接住它收尾
        sys.exit()            # 【API】sys.exit() —— 作用：结束整个程序；参数：可传退出码，默认 0 表示正常退出；其实这里用 break 跳出循环就够，不必把整个程序关掉
print("-"*60)

# 【本段知识点】
# 1. 生成器函数里 return（不带值）不是报错，而是发 StopIteration 信号，正好被外层 try 接住收尾。
# 2. a, b = b, a + b 是同步赋值：右边的 b 和 a+b 用的都是旧值，互不污染，比写两行临时变量干净。
# 3. 生成器能"假装"无限：斐波那契没有尽头，但每次只现算一个值，内存占用恒定，这正是生成器适合长序列的原因。
