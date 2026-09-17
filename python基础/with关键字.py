# ============================================================
# 【with 关键字】上下文管理器：手动关文件 · with 自动关文件 · 多文件 · 线程锁 · 临时精度 · 自定义
# 涉及知识点：with 语句 · try/finally · open()/read()/close()/write() · 上下文管理器协议
#            （__enter__/__exit__）· contextlib.contextmanager · yield 暂停
# 运行方式：python 本文件名.py（需当前目录存在 example_with关键字.txt 与 example_with关键字-input.txt）
# 隔离情况：8 段 demo 基本独立；file / content 在 example 1、2、应用场景1 各段自己重新赋值，属安全覆盖；
#           sqlite3 段整段注释不执行；没有会污染后续运行的全局状态
# ============================================================

# with关键字

# ================ 【example 1】try/finally：手动关文件的"笨办法" ================
## example 1
file = open('example_with关键字.txt', 'r')   # 【API】open(路径, 模式) —— 作用：打开文件返回文件对象；参数：文件路径（必填）、模式（默认 'r' 只读）；返回：文件对象
try:
    content = file.read()   # 【API】file.read() —— 作用：把整个文件读成一个字符串；参数：可选"读多少字节"，默认全读；返回：字符串
    # 处理文件内容
finally:
    file.close()      # 【API】file.close() —— 作用：关闭文件、释放系统句柄；参数：无；返回：None；忘关的话文件会被一直占着

# 【本段知识点】
# 1. try/finally 保证 file.close() 一定会执行：就算 read() 中途抛异常，也会先关文件再往上抛。
# 2. 这样写要三行样板（open → try → finally），忘写 close() 文件句柄就占着不放，所以才有下一节的 with。
# 3. 别在 finally 里写 return 或业务逻辑：它会覆盖 try 的正常返回值，还可能把异常吞掉。

# ================ 【example 2】with 自动关文件：try/finally 的语法糖 ================
print("\n"+"="*60)                    # 输出分隔块（固定样式）：60 个 = 起头，先换行防止挤在上一行
print("【example 2】with 自动关文件：try/finally 的语法糖")
print("="*60)
## example 2
with open('example_with关键字.txt', 'r') as file:   # 同名覆盖：file 在这里重新绑定，example 1 那个已关闭的 file 就此丢弃，互不干扰
    content = file.read()              # 和 example 1 的 read() 是同一个方法，只是少写 try/finally 三行
    print(content)                     # 打印文件内容
# 文件已自动关闭
print("-"*60)                         # 输出收尾线（固定样式）

# 【本段知识点】
# 1. with 是 try/finally 的语法糖：块结束（正常或异常）时自动调 file.close()，样板代码全省。
# 2. 只有实现了 __enter__/__exit__ 的对象才能进 with ... as（这种对象叫上下文管理器），后面看怎么自定义。
# 3. 块结束后文件已关闭：在 with 外面再 read() 会抛 ValueError: I/O operation on closed file。

# ================ 【应用场景 1】同时打开多个文件：读写一肩挑 ================
## 应用场景1 
# 同时打开多个文件
with open('example_with关键字-input.txt', 'r') as infile, open('example_with关键字-output.txt', 'w') as outfile:
    content = infile.read()
    outfile.write(content.upper())   # 【API】file.write(内容) —— 作用：把字符串写进文件；参数：要写的内容（必填）；返回：写入的字符数；upper() 上一份文件讲过：返回全大写新字符串

# 【本段知识点】
# 1. with 能一次管多个文件，逗号隔开：任何一个抛异常，两个文件都会被自动关闭。
# 2. 'w' 模式会先清空再写：outfile 原来有内容也会被覆盖，别拿重要文件试。
# 3. 这段全程没有 print，屏幕上看不到任何输出，产物是 output 文件里的全大写内容。

# ================ 【应用场景 2】连接数据库（整段注释，不会执行） ================
# ## 应用场景2 连接数据库
# import sqlite3
# with sqlite3.connect('database.db') as conn:
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users')
#     results = cursor.fetchall()
# # 连接自动关闭

# ================ 【应用场景 3】线程锁：with 保证加锁解锁成对 ================
print("\n"+"="*60)
print("【应用场景 3】线程锁：with 保证加锁解锁成对")
print("="*60)
## 应用场景3 线程锁
import threading

lock = threading.Lock()   # 【API】threading.Lock() —— 作用：创建一把互斥锁；参数：无；返回：Lock 对象；锁是"一次只放一个线程进门"的门禁

with lock:                # with lock 等价于 lock.acquire() ... finally: lock.release()，忘解锁导致死锁的概率大降
    # 临界区代码
    print("这段代码是线程安全的")
print("-"*60)

# 【本段知识点】
# 1. 锁保证同一时刻只有一个线程进临界区：with 进块自动加锁、出块自动释放，解锁不可能被忘掉。
# 2. 单线程演示看不出并发效果，练的是写法；真正多线程时，没有锁的 print 会互相插队。
# 3. threading.Lock 是互斥锁：一次只放一个线程。需要可重入/多读场景还有 RLock、Semaphore 等，以官方文档为准。

# ================ 【应用场景 4】临时修改系统状态：decimal 精度 ================
## 应用场景4 临时修改系统状态
import decimal

with decimal.localcontext() as ctx:   # 【API】decimal.localcontext() —— 作用：临时切换十进制运算上下文，出块自动还原；参数：可传 ctx（默认新建）；返回：上下文管理器
    ctx.prec = 42  # 临时设置高精度
    # 执行高精度计算
    # 精度恢复原设置

# 【本段知识点】
# 1. localcontext() 是"进块改、出块还原"的典型：块内 prec=42，出块自动恢复全局默认，不用手动记着改回去。
# 2. 这种"借了东西保证还"的语义，正是上下文管理器相对 try/finally 的通用价值。
# 3. 需要精确十进制的场景（金额、税率）用 decimal；普通 float 会有 0.1+0.2!=0.3 的误差。

# ================ 【自定义上下文管理器】Timer：实现 __enter__ / __exit__ 协议 ================
print("\n"+"="*60)
print("【自定义上下文管理器】Timer：实现 __enter__ / __exit__ 协议")
print("="*60)
## 创建自定义上下文管理器
class Timer:
    def __enter__(self):              # 进 with 块时执行：这里记下开始时间
        import time
        self.start = time.time()      # 【API】time.time() —— 作用：取当前时间戳；参数：无；返回：自 1970-01-01 起的秒数（浮点）
        return self                   # return self 让 with Timer() as t 里的 t 拿到这个对象
    def __exit__(self, exc_type, exc_val, exc_tb):   # 出 with 块时执行（正常结束或抛异常都会来）
        import time
        self.end = time.time()
        print(f"耗时: {self.end - self.start:.2f}秒")  # f-string 里 {变量} 会替换成实际值；:.2f 保留两位小数
        return False                  # 返回 False = 有异常继续往上抛；返回 True 会把异常吞掉

# 使用示例
with Timer() as t:                    # __enter__ 的返回值 self 装进 t；块结束自动调 __exit__
    # 执行一些耗时操作
    sum(range(1000000))               # 【API】sum(可迭代对象) —— 作用：把数字序列加起来；参数：数字组成的可迭代对象；返回：总和
print("-"*60)

# 【本段知识点】
# 1. 上下文管理器协议就两个方法：__enter__ 进块时执行（这里记开始时间），__exit__ 出块时执行（这里打耗时）。
# 2. __exit__ 的四个参数是异常信息：exc_type 异常类型、exc_val 异常对象、exc_tb 回溯；没出错时前三个是 None。
# 3. import time 写在方法里也能用（模块会被缓存），但惯例是统一放文件开头。

# ================ 【contextmanager 装饰器】用生成器函数造上下文管理器 ================
print("\n"+"="*60)
print("【contextmanager 装饰器】用生成器函数造上下文管理器")
print("="*60)
## 使用 contextlib.contextmanager 装饰器创建上下文管理器
from contextlib import contextmanager

# 【API】contextlib.contextmanager —— 作用：把"中间带 yield 的生成器函数"装饰成上下文管理器，省掉手写 __enter__/__exit__；参数：无；返回：装饰器
@contextmanager
def tag(name):
    print(f"<{name}>")    # yield 之前 = __enter__：进块时打印开标签
    yield                 # yield 处把控制权让给 with 块；块内跑完才回到这里
    print(f"</{name}>")   # yield 之后 = __exit__：出块时打印闭标签

# 使用示例
with tag("h1"):           # 执行顺序：<h1> → 块内 print → </h1>
    print("这是一个标题")
print("-"*60)

# 【本段知识点】
# 1. @contextmanager 把"中间有 yield 的生成器函数"变成上下文管理器：yield 前是 __enter__，yield 后是 __exit__。
# 2. 这里的 yield 不是"取值"而是"让位"：with 块里的代码全部跑完，生成器才从 yield 后面继续执行。
# 3. 对比 Timer：手写类适合逻辑复杂、要保存状态的；contextmanager 适合这种"进出各打一行"的轻量场景。
