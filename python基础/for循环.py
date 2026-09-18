# ============================================================
# 【for 循环全用法】单变量 · 解包 · 嵌套 · for-else · break/continue · 推导式 · zip · reversed · *rest · 生成器
# 涉及知识点：for-each 语义 · enumerate() · dict.items() · 元组解包 · for...else · range()
#            · zip() · reversed() · *rest 解包 · 生成器表达式 · 惰性求值
# 运行方式：python 本文件名.py（无额外依赖）
# 隔离情况：各段独立；nums / res / d / s / names / scores / data / gen 都是各段自己的变量，无跨段依赖
# ============================================================

# Python for 循环全用法汇总
# > Python 的 for 是迭代循环（for-each），不是C/Java那种传统的三段式for；它本质是不断从可迭代对象取出元素。
# > 语法基础：for 变量 in 可迭代对象:

# ================ 【1】基础用法：单变量迭代（最常用） ================
print("\n"+"="*60)                    # 输出分隔块（固定样式）：60 个 = 起头，先换行防止挤在上一行
print("【1】基础用法：单变量迭代")
print("="*60)
# 遍历列表
nums = [1,2,3]
for x in nums:
    print(x)

# 遍历字符串
for ch in "hello":
    print(ch)

# 遍历range，模拟传统数字循环
for i in range(5):
    print(i)
print("-"*60)                         # 输出收尾线（固定样式）

# 【本段知识点】
# 1. for 是 for-each：每次循环从可迭代对象里取一个元素给 x，取完自动结束，不需要下标和自增。
# 2. 字符串也可迭代，逐字取出；range(5) 产出 0~4，用来模拟 C 语言的 for(i=0;i<n;i++)。
# 3. 循环变量 x 循环结束后仍然存在，值是最后一个元素——Python 不会帮你清掉它。

# ================ 【2】多变量解包迭代：enumerate / items / 元组列表 ================
print("\n"+"="*60)
print("【2】多变量解包迭代")
print("="*60)
# 迭代对象里每个元素是元组/列表，for 后面写多个变量自动解包。
# 2.1 enumerate：同时拿到下标+值（刷题高频）
nums = [2,7,11]
for idx, val in enumerate(nums):   # 【API】enumerate(可迭代对象) —— 作用：边遍历边数下标；参数：可迭代对象（可选 start 起始值，默认 0）；返回：枚举迭代器，每个元素是 (下标, 值) 元组
    print(idx, val)

# 2.2 遍历字典 items()：key value
d = {"a":1, "b":2}
for k, v in d.items():   # 【API】dict.items() —— 作用：把字典拆成 (键, 值) 元组的视图；参数：无；返回：可迭代的键值对视图
    print(k, v)

# 2.3 遍历元组列表
points = [(1,2), (3,4)]
for x, y in points:
    print(x,y)

# 2.4 三个及以上变量解包
data = [(1,10,100), (2,20,200)]
for a,b,c in data:
    print(a,b,c)
print("-"*60)

# ⚠️ 变量数量必须和每个元素长度匹配，否则报错。

# 【本段知识点】
# 1. for 后面写多个变量 = 自动解包：每个元素是 (x, y) 元组，拆开分别赋给 x、y。
# 2. enumerate 最常用在"既要下标又要值"（如两数之和）；等价写法是 for i in range(len(nums)) 再 nums[i]。
# 3. 字典直接 for 只给键，想同时要值必须 .items()；解包变量个数和元素长度不一致会 ValueError。

# ================ 【3】嵌套 for 循环：外层取行，内层取元素 ================
print("\n"+"="*60)
print("【3】嵌套 for 循环")
print("="*60)
matrix = [[1,2],[3,4]]
for row in matrix:
    for item in row:
        print(item)
print("-"*60)

# 【本段知识点】
# 1. 外层循环先取一行（row），内层循环把这一行的每个元素取出来打印。
# 2. 执行节奏：外层走一步，内层完整走一遍，所以输出 1、2、3、4 按行顺序。
# 3. 嵌套层数越多越难读，能用推导式拍平就优先用推导式。

# ================ 【4】for + else：循环没被 break 打断才走 else ================
print("\n"+"="*60)
print("【4】for + else：没被 break 打断才走 else")
print("="*60)
# > else 属于 for循环，不是if！
# > ✅ 触发：循环正常跑完，没有被break中断，才执行else。
# > ❌ 如果执行了break跳出循环，else块不会运行。
# 刷题场景：用来标记「遍历完都没找到目标」。
nums = [1,2,3]
for x in nums:
    if x == 5:
        break
else:                     # 这个 else 对齐的是 for，不是 if——注意缩进
    print("循环正常结束，没有触发break")
print("-"*60)

# 【本段知识点】
# 1. for...else 的 else 属于循环：只有循环"自然跑完"（没 break）才执行。
# 2. 本 demo 里 5 不在 nums 中，break 从未触发，所以 else 正常打印。
# 3. 想看反面：把 if x == 5 改成 if x == 2，命中后 break，else 就不会打印了。

# ================ 【5】break / continue：终止整个循环 vs 跳过本次 ================
print("\n"+"="*60)
print("【5】break / continue")
print("="*60)
# - break：立刻终止整个for循环
# - continue：跳过本次迭代，直接进入下一轮
for i in range(10):
    if i == 3:
        break
    if i ==1:
        continue
    print(i)
print("-"*60)

# 【本段知识点】
# 1. continue 在 i=1 时跳过本次，所以 1 没打印；break 在 i=3 时终止整个循环，3 及以后都不打印。
# 2. 最终只输出 0、2——这就是两个控制语句的直观区别。
# 3. 刷题时 continue 常用于跳过非法输入，break 常用于找到目标后提前收工。

# ================ 【6】推导式：for 的特殊简写（一行循环，高频刷题） ================
# 本质是for循环表达式写法，分列表、字典、集合推导式
# 原文档这段只定义、没有 print，运行起来屏幕上看不到输出；想验证结果自己加 print(res) / print(d) / print(s)
# 列表推导式
res = [x*2 for x in range(5)]
# 带条件
res = [x for x in range(10) if x%2==0]

# 字典推导式
d = {k:k*k for k in range(3)}

# 集合推导式
s = {x%3 for x in range(10)}

# 【本段知识点】
# 1. 推导式是 for 的"表达式版"：三行循环压成一行，结果直接产出新容器。
# 2. 列表推导式 [x*2 for x in range(5)] → [0,2,4,6,8]；带 if 的只留偶数；花括号带冒号是字典、不带冒号是集合（自动去重）。
# 3. 这段只定义没打印，屏幕无输出；想亲眼看结果，自己加 print(res)、print(d)、print(s)。

# ================ 【7】并行迭代 zip()：多个容器同步遍历 ================
print("\n"+"="*60)
print("【7】并行迭代 zip()")
print("="*60)
# 同时取多个可迭代对象的元素，按最短长度截断
names = ["a","b"]
scores = [90,80]
for name, score in zip(names, scores):   # 【API】zip(可迭代对象1, 可迭代对象2, ...) —— 作用：把多个容器按位置配成对；参数：两个及以上可迭代对象；返回：元组迭代器，按最短的那个截断
    print(name, score)
print("-"*60)

# 【本段知识点】
# 1. zip 按"最短容器"截断：这里两个都是 2 个元素，正好配成两对输出。
# 2. 每次取出的 (name, score) 元组被 for 双变量自动解包。
# 3. 想拿配对结果的列表用 list(zip(...))；zip 是惰性迭代器，不会一次性全算好。

# ================ 【8】反向迭代 reversed() ================
print("\n"+"="*60)
print("【8】反向迭代 reversed()")
print("="*60)
nums = [1,2,3]
for x in reversed(nums):   # 【API】reversed(可迭代对象) —— 作用：倒序产出元素；参数：有长度的可迭代对象；返回：反向迭代器（惰性）
    print(x)
print("-"*60)

# 【本段知识点】
# 1. reversed 不改原列表，只是"倒着吐元素"：打印 3、2、1，nums 本身仍是 [1,2,3]。
# 2. 原地反转用 nums.reverse()（改原列表）；要新列表用 nums[::-1]。
# 3. 只支持有长度的对象（列表/元组/字符串），生成器不能 reversed。

# ================ 【9】打包解包进阶：* 可变变量接收（高级用法） ================
print("\n"+"="*60)
print("【9】*rest 解包")
print("="*60)
data = [(1,2,3), (4,5,6)]
for a, *rest in data:   # a 拿第一个元素，*rest 把剩下的全部打包进列表
    print(a, rest)
# a取第一个元素，剩下全部打包进rest列表
print("-"*60)

# 【本段知识点】
# 1. *rest 是"可变接收"：元素再多都接得住，rest 永远是列表。
# 2. 第一轮 a=1、rest=[2,3]；第二轮 a=4、rest=[5,6]——这就是打印结果。
# 3. 一个 for 里只能有一个 *；它可以放中间（a, *rest, b），但不能有两个 * 同时出现。

# ================ 【10】迭代器、生成器上的 for 循环 ================
print("\n"+"="*60)
print("【10】生成器上的 for")
print("="*60)
# for 可以直接遍历生成器表达式，不需要转列表，节省内存
gen = (x**2 for x in range(5))
for num in gen:
    print(num)
print("-"*60)

# 【本段知识点】
# 1. 生成器表达式不一次性算完：for 每取一个它才现算一个，省内存。
# 2. 不用 list() 包一层，for 直接消费生成器，中间列表省掉。
# 3. 生成器只能遍历一次：for 完就空了，想再遍历得重新造一个。

# ================ 【11】递归不是 for，不要混淆 ================
# > Python 没有 C 语言 for(i=0;i<n;i++) 这种原生三段式 for 语法，range 是模拟实现。
# （纯概念段，没有代码，所以也没有输出）

# ================ 【附】快速分类总结表（原文档表格，转成注释） ================
# | 类型 | 核心场景 |
# | ---- | ---- |
# | 单变量for | 遍历元素，最基础 |
# | 多变量解包for | enumerate / dict.items / 元组列表 |
# | zip并行for | 同步遍历多个序列 |
# | reversed反向for | 倒序遍历 |
# | for ... else | 判断循环是否被break中断（Python特有） |
# | for+break/continue | 控制循环跳转 |
# | 推导式 | 一行循环生成容器，刷题简写 |
# | *解包for | 不确定元素数量时接收剩余元素 |

# ---

# 对比：你现在刷题最常用的3个for写法
# 1. for num in nums: 只拿值
# 2. for idx, num in enumerate(nums): 拿下标+值（两数之和）
# 3. for k, v in hash_map.items(): 遍历字典

# ================ 【附】for...else 测试代码（原文档结尾提问，这里补上） ================
# 原文档最后问：要不要写一段测试代码演示 for...else 这个容易踩坑的特殊用法？——就是下面这段。
print("\n"+"="*60)
print("【附】for...else 测试：找到 vs 找不到")
print("="*60)

# 情况 1：目标 3 在列表里 → break 触发 → else 不执行
nums = [1, 2, 3, 4, 5]
for x in nums:
    if x == 3:
        print("找到了 3，break 跳出，else 不执行")
        break
else:
    print("没找到，循环自然跑完，else 执行")

# 情况 2：目标 99 不在列表里 → 循环自然跑完 → else 执行
for x in nums:
    if x == 99:
        print("找到了 99，break 跳出")
        break
else:
    print("没找到 99，循环自然跑完，else 执行")
print("-"*60)

# 【附·知识点】
# 1. 对比两段输出就懂：break 一触发 else 就失效；没 break 才轮到 else——else 是"循环的收尾"，不是 if 的。
# 2. 刷题套路：拿它当"搜索失败"哨兵，遍历完都没命中就进 else 处理"没找到"。
# 3. 最容易踩的坑：把 else 缩进到 for 循环体里（对齐 if），语义就完全变了；务必用上面这种"else 对齐 for"的写法。
