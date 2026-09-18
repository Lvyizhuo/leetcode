#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# LeetCode 49. 字母异位词分组 (Group Anagrams)  |  难度：中等
# ------------------------------------------------------------
# 题目：给定字符串数组 strs，把互为"字母异位词"的字符串分到同一组。
#       异位词 = 组成字母完全相同、只是排列顺序不同（如 eat / tea / ate）。
#       返回结果列表，组与组之间、组内的顺序都无所谓。
# 涉及知识点：哈希表（dict）· 字符串排序 · setdefault · 空间换时间
#
# 命名与存放（本技能约定）：
#   文件名 = lc_<题号4位>_<中文题名>.py，本文件即 lc_0049_字母异位词分组.py
#   默认路径：/Users/lvyizhuo/project/i/leetcode/hot100/
#
# 运行方式：
#   python lc_0049_字母异位词分组.py                        # 终端直接跑 -> 自测模式，跑全部内置用例
#   python lc_0049_字母异位词分组.py --test                 # 强制自测模式
#   echo 'strs = ["eat","tea","tan"]' | python lc_0049_字母异位词分组.py   # ACM 模式（管道）
#   python lc_0049_字母异位词分组.py < in.txt               # ACM 模式（重定向）
#   python lc_0049_字母异位词分组.py --acm < in.txt         # 强制 ACM 模式
#
# 脚本结构（四段解耦，改题时只动对应那一段）：
#   ① class Solution      -- 纯算法，与 LeetCode 提交区一致，不碰任何 IO
#   ①' class SolutionCountKey -- 进阶解法（计数数组做键），仅供学习对比，不提交
#   ② parse_input()       -- stdin 文本 -> 算法入参（唯一负责"读"的地方）
#   ③ format_output()     -- 算法返回值 -> 输出字符串（唯一负责"写"的地方）
#   ④ main() / _run_selftest() -- 入口与自测，决定走 ACM 还是自测
#
# 注释约定（算法层强制）：每个 API / 关键字 / 语法糖首次出现处都要解释，
# 三要素齐全 -- 作用 · 关键参数（含默认值）· 返回或副作用；同一 API 之后只写短注释。
# ============================================================

import ast
import re
import sys
from typing import List


# ============================================================
# ① 核心算法：与 LeetCode 提交区一致，可整段复制粘贴提交
#    - 只依赖标准库（LeetCode 已预导入 collections / heapq / math / bisect 等）
#    - 禁止出现 input() / print() / sys.stdin，保证 Solution 能脱离 IO 单独使用
# ============================================================
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """一次遍历 + 哈希表：把"排序后相同的字符串"归到同一组。

        思路：异位词只是字母顺序不同，所以把每个词内部排序后当作"分组键"，
              排序结果相同的词必然互为异位词。扫到词 s 时用 key 查表，
              把 s 追加进对应分组即可；最后返回所有分组。
        为什么快：判断"两个词是否互为异位词"，最笨的办法是两两比对全部排列
                  （O(k!) 级别）；而"排序后比相等"只要 O(k log k)。再用哈希表把
                  "找 s 属于哪一组"从两两比对（O(n^2)）降为单次 O(1) 查询。
        时间复杂度 O(n·k·log k)：n 个词，每个词排序一次，k 为词长（本题 ≤ 100）。
        空间复杂度 O(n·k)：哈希表存下所有词（即答案本身）。

        关键 Python 语法（首次出现处详解，后续同款写法不再展开）：
          - dict.setdefault(key, default)：键不存在时先写入默认值再返回，
            省掉 "if key not in d: d[key] = []" 两行判断；返回的是表里那个列表
            本身（引用），对它 append 就直接改进了表。
          - sorted(iterable)：返回排好序的"新列表"，不原地修改原对象；对字符串
            按字符 Unicode 码点逐个排，如 sorted("eat") -> ['a', 'e', 't']。
          - "".join(可迭代对象)：把字符列表拼回字符串，当作字典的键（字符串可哈希）。
          - dict.values()：返回所有值组成的"动态视图"（不是拷贝），
            视图随字典变化，list() 包一层转成普通列表。
        """
        groups = {}                                # 【dict】分组键(排序后的词) -> 该组的词列表

        for s in strs:                             # 每个词只处理一遍
            key = "".join(sorted(s))               # 排序后作键："eat"/"tea"/"ate" 全变成 "aet"
                                                   # 【易错】sorted(s) 返回字符列表，必须 join 回
                                                   #   字符串才能做键；直接拿列表当键会因不可哈希报错
            groups.setdefault(key, []).append(s)   # 【API】setdefault(key, default)
                                                   #   作用：键不存在就先塞 default 再返回它，存在则直接返回旧值
                                                   #   关键参数：default 只在键缺失时生效，这里给空列表
                                                   #   返回：键对应的值（这里就是该组的列表，append 原地生效）
        return list(groups.values())               # 【API】dict.values()
                                                   #   作用：取出所有分组（每组一个列表）
                                                   #   返回：动态视图对象，list() 转成普通列表即为答案
                                                   #   【易错】直接 return groups.values() 类型是视图不是 List，
                                                   #   提交时类型校验（部分 OJ）会报错，必须 list() 包一层


# ============================================================
# ①' 进阶解法（仅学习对比，不提交）：
#     把"排序做键"换成"26 个字母计数做键"，单词排序 O(k log k) 压到 O(k)
# ============================================================
class SolutionCountKey:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """计数数组做键：统计每个词里 26 个小写字母各自出现几次，把计数元组当键。

        与 ① 的区别：① 对每个词排序（O(k log k)）；本解法只需逐字符数一遍
        （O(k)），键是 26 元计数元组，如 "eat" 与 "tea" 都对应
        (1,0,0,0,1,0,...,1,...)。n 个词、词长 k 时总时间 O(n·k)，
        比排序法少一个 log 因子，但常数更大（每次建 26 长度的列表），
        实际差距在 k 很小时不明显。仅作学习对比，提交请用 ① 段。
        """
        groups = {}                                # 计数键 -> 分组
        for s in strs:
            cnt = [0] * 26                         # 【语法】[0] * 26：列表重复，生成 26 个 0 的计数表
                                                   #   （下标 0 对应 'a'，25 对应 'z'）
            for ch in s:
                cnt[ord(ch) - ord('a')] += 1       # 【API】ord(单字符) -> 该字符的 Unicode 码点
                                                   #   ord('a') == 97，减 97 得 0..25 的下标
            key = tuple(cnt)                       # 【语法】tuple(列表)：转成元组才能做字典键
                                                   #   （列表可变、不可哈希，元组不可变、可哈希）
            groups.setdefault(key, []).append(s)
        return list(groups.values())


# ============================================================
# ② 输入解析层：stdin 原始文本 -> 算法入参
#    唯一允许"读输入"的地方；交给算法的是干净的 Python 对象。
#    Solution 完全不知道输入长什么样，所以换输入格式不用动算法。
# ============================================================

# ---- 通用解析工具：吃 LeetCode 控制台 / 常见 OJ 的输入写法，可整段复用 ----

_LITERAL_FIXES = (
    (r"\bnull\b", "None"),      # LeetCode 用 null 表示空节点（链表、二叉树题常见）
    (r"\btrue\b", "True"),      # 少数题面混用 JS 风格布尔
    (r"\bfalse\b", "False"),
)


def _to_obj(tok: str):
    """把一段文本还原成 Python 对象。

    优先级：带引号的字符串 > Python 字面量 > 把 null/true/false 换成 Python 写法 > 裸字符串

    【API】ast.literal_eval(字符串或 AST 节点)
      作用：安全地求值"字面量表达式"，只认数字/字符串/列表/字典/元组/布尔/None；
            不会像 eval() 那样执行函数调用，所以拿外部输入来解析是安全的。
      关键参数：接受 str 或 AST 节点；不支持 null（那是 JavaScript 写法），需要先替换。
      返回：对应的 Python 对象；解析失败抛 ValueError / SyntaxError，这里用 try 接住后降级处理。
    """
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in ("\"", "'"):
        return tok[1:-1]                    # 显式带引号 -> 剥掉引号当字符串，不再 eval
    try:
        return ast.literal_eval(tok)        # [1,2,3] / 9 / "abc" / 3.14 / True / None
    except (ValueError, SyntaxError):
        pass
    fixed = tok
    for pattern, repl in _LITERAL_FIXES:
        # 【API】re.sub(正则, 替换文本, 原字符串)
        #   作用：把匹配到的片段全部替换掉；参数：\b 表示"单词边界"，
        #         保证只换独立的 null，不会误伤 "annulled" 这种字符串内部；
        #   返回：替换后的新字符串（原字符串不变，字符串是不可变对象）
        fixed = re.sub(pattern, repl, fixed)
    if fixed != tok:
        try:
            return ast.literal_eval(fixed)   # [3,9,20,null,null,15,7] -> [3,9,20,None,None,15,7]
        except (ValueError, SyntaxError):
            pass
    return tok                               # 兜底：当裸字符串，例如输入就是 abc


def split_top_level(text: str, sep: str = ",") -> List[str]:
    """按 sep 切分字符串，但忽略括号 [] () {} 内部和引号内部的 sep。

    【为什么需要】"strs = [\"eat\",\"tea\"], n = 2" 直接 text.split(",") 会被数组里的逗号
    切碎，所以用一个计数器记录括号深度 depth：depth 为 0 时遇到的逗号才是真分隔符；
    同时用 quote 记住"当前在字符串内部"，字符串里的逗号同样要跳过。

    例："nums = [2,7], target = 9" -> ["nums = [2,7]", "target = 9"]
    """
    items, buf, depth, quote = [], [], 0, None   # buf 是当前正在拼的片段
    for ch in text:
        if quote:                                # 字符串内部：原样收下，只等收尾引号
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("\"", "'"):
            quote = ch
            buf.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == sep and depth == 0:           # 顶层分隔符 -> 收一个片段，开新的
            items.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    items.append("".join(buf))
    return [s.strip() for s in items if s.strip()]


def parse_args(text: str, order=None) -> tuple:
    """解析"参数区"文本，返回按方法签名顺序排列的实参元组。

    支持两种常见写法：
      1) 具名式（LeetCode 控制台、题面 Example 的写法）：strs = ["eat","tea","tan"]
      2) 逐行式（一行一个参数值，OJ 常见）：["eat","tea","tan"]

    order 传形参名元组（如 ("strs",)）时，具名式按形参名对号入座，
    与书写顺序无关；传 None 则按出现顺序返回。

    【API】re.match(正则, 字符串)
      作用：从字符串开头尝试匹配；参数：^ 表示开头，[A-Za-z_]\\w* 匹配合法标识符，
            \\s*=\\s* 容忍等号两边有空格，(.+) 把等号右边整体抓出来；
      返回：匹配成功返回 Match 对象（group(1)/group(2) 取捕获组），失败返回 None。
      对比 re.search 是"任意位置找"，re.fullmatch 是"整串必须完全匹配"。
    """
    text = text.strip()
    if not text:
        return ()
    flat = " ".join(text.split())     # 【语法】str.split() 不带参数 = 按任意空白切分并丢弃空串，
                                      # 再用 " ".join(...) 拼回一行，于是多行嵌套结构也能压成一行，
                                      # 而 [ ["eat","tea"], ["tan"] ] 这种跨行写法照样能解析。

    if "=" in flat:                   # ---- 具名式 ----
        pairs = []
        for chunk in split_top_level(flat):
            m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+)$", chunk, re.S)
            if m:
                pairs.append((m.group(1), _to_obj(m.group(2))))
            else:
                pairs.append((None, _to_obj(chunk)))    # 没写名字 -> 当位置参数
        if order is None:
            return tuple(v for _, v in pairs)
        named = {k: v for k, v in pairs if k}          # 【语法】字典推导式：从 (键,值) 序列建 dict
        rest = [v for k, v in pairs if not k]          # 【语法】列表推导式：筛出匿名的位置参数
        out = []
        for name in order:
            if name in named:
                out.append(named[name])
            elif rest:
                out.append(rest.pop(0))                # 【API】list.pop(0) 弹出并返回首个元素
                                                       #   注意是 O(n)（后面元素整体前移），
                                                       #   这里只用 1~2 次，无所谓；循环里别这么写
            else:
                raise ValueError(f"输入里缺少参数 {name!r}：{text!r}")
        return tuple(out)

    # ---- 逐行式：每行一个参数值，行内再用顶层逗号切开 ----
    items = []
    for line in text.splitlines():
        if line.strip():
            items.extend(split_top_level(line))        # 【API】list.extend(可迭代对象)：把元素逐个追加
    return tuple(_to_obj(i) for i in items)


def parse_input(text: str):
    """stdin 原文 -> groupAnagrams(strs) 的实参元组 (strs,)。

    改题时只改这个函数的最后一行：把形参名元组换成新方法的形参名。
    输入格式特殊（"第一行 n，第二行 n 个数"、纯空格分隔等）时在这里手写解析，
    复用上面的 _to_obj / split_top_level 即可。
    """
    return parse_args(text, order=("strs",))


# ============================================================
# ③ 输出格式化层：算法返回值 -> 标准输出字符串
#    只在这里做格式适配，算法和解析层都不用改。
# ============================================================
def format_output(result) -> str:
    """字母异位词分组的输出就是嵌套列表，直接 str() 得到 [['bat'], ['nat', 'tan']] 这种
    LeetCode 展示格式（组与组、组内顺序都无所谓）。

    【API】str(对象) 会调用对象的 __str__；对嵌套 list 来说得到带方括号的写法。
    注意打印出来的是单引号（Python 默认），LeetCode 网页显示双引号，但判题不比对字符串原文，
    只比对数据结构，所以这里不需要做引号替换。
    其他常见适配（用到再改这里，绝不改 Solution）：
      - 布尔：return "true" if result else "false"      # OJ 常要求小写 true/false
      - 浮点：return f"{result:.5f}"                    # 保留 5 位小数
      - 一行空格分隔：return " ".join(map(str, result)) # map 是惰性的，join 时才真正求值
      - 多答案无序：return str(sorted(result))          # 先规范化再打印，避免判题机比对顺序
    """
    return str(result)


# ============================================================
# ④ 驱动层：ACM/OJ 模式 + 自测模式
# ============================================================
def solve(text: str) -> str:
    """IO 层总装（纯函数，便于自测）：stdin 原文 -> stdout 字符串。"""
    (strs,) = parse_input(text)
    result = Solution().groupAnagrams(strs)
    return format_output(result)


def _run_acm() -> int:
    """ACM/OJ 模式：整体读入 stdin，算一次，打印一行结果。"""
    text = sys.stdin.read()            # 【API】sys.stdin.read()：一次读完整个标准输入（含换行），
                                       #   返回 str；判题机把输入重定向进来，所以能直接读到全部内容
    if not text.strip():
        return 0                       # 空输入安静退出，避免判题机因为异常判 RE
    sys.stdout.write(solve(text) + "\n")   # 【API】sys.stdout.write(s)：写字符串，不自动加换行，
                                       #   所以手动补 "\n"；对比 print 会自动换行并做 sep/end 处理
    return 0


def main(argv=None) -> int:
    """入口：决定走自测还是 ACM。

      命令行带 --test            -> 自测（不管有没有管道）
      命令行带 --acm             -> ACM（读 stdin）
      没带参数且 stdin 是终端     -> 自测（人手动打开脚本，看用例结果）
      没带参数且 stdin 被重定向   -> ACM（判题机 / 管道场景）

    【API】sys.stdin.isatty()
      作用：判断标准输入是不是连着交互式终端；参数：无；
      返回：True 表示"有人在终端敲"，False 表示"被管道或文件重定向了"。
      判题机上必然是 False，所以提交到 OJ 时不会误跑自测。
    """
    argv = sys.argv[1:] if argv is None else argv
    if "--test" in argv:
        return _run_selftest()
    if "--acm" in argv:
        return _run_acm()
    if sys.stdin.isatty():
        return _run_selftest()
    return _run_acm()


# ============================================================
# ⑤ 内置测试：运行脚本即全量验证（常规 + 边界 + IO 端到端）
#    提交到 LeetCode 时 __name__ 不是 "__main__"，整段不会执行，可放心一起粘贴
# ============================================================

# ---- 比较器：算法返回值常常"不等价形式但都算对"，按题目挑一个 ----
def eq(got, want):
    """严格相等，默认比较器。"""
    return got == want


def eq_groups(got, want):
    """字母异位词分组的比较器：组与组之间、每组内部都允许任意顺序。

    先对每个分组内部排序，再对所有分组排序，两边规范化后比相等。
    【API】sorted(可迭代对象) 对嵌套列表也有效：内层按第一个字符串比，
    字符串之间按字典序比，不会抛 TypeError。
    """
    def norm(groups):
        return sorted(sorted(g) for g in groups)   # 内层 sorted 抹平组内顺序，
                                                   # 外层 sorted 抹平组间顺序
    return norm(got) == norm(want)


# ---- 用例表：(说明, 传给方法的实参元组, 期望值, 比较器[可选，默认 eq]) ----
CASES = [
    ("常规：题目样例 1（期望值故意写成题面顺序，验证组序无关）",
     (["eat", "tea", "tan", "ate", "nat", "bat"],),
     [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]], eq_groups),
    ("常规：题目样例 2（单个空串）", ([""],), [[""]], eq_groups),
    ("常规：题目样例 3（单个字符）", (["a"],), [["a"]], eq_groups),
    ("边界：两个完全相同的词", (["a", "a"],), [["a", "a"]], eq_groups),
    ("边界：所有词互不为异位词", (["abc", "def", "ghi"],),
     [["abc"], ["def"], ["ghi"]], eq_groups),
    ("边界：空串与普通词混排", (["", "", "b"],), [["", ""], ["b"]], eq_groups),
    ("边界：同字母重复出现（a 出现两次应同组）", (["a", "b", "a"],),
     [["a", "a"], ["b"]], eq_groups),
    ("边界：等长但不同组 + 异位词同时存在", (["ab", "ba", "abc", "cba"],),
     [["ab", "ba"], ["abc", "cba"]], eq_groups),
]

# ---- IO 层端到端用例：(说明, stdin 原文, 期望的 stdout 字符串) ----
IO_CASES = [
    ("IO 具名式输入（LeetCode 控制台写法）",
     'strs = ["eat","tea","tan","ate","nat","bat"]',
     "[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]"),
    ("IO 逐行式输入（常见 OJ 写法）", '[""]', "[['']]"),
    ("IO 单字符输入", '["a"]', "[['a']]"),
]


def _run_selftest() -> int:
    print("=" * 60)
    print("自测模式：LeetCode 49. 字母异位词分组 (Group Anagrams)")
    print("=" * 60)

    total = 0
    failed = 0

    # 第 1 关：直接调算法层，不经过任何 IO
    print(f"[算法层] 直接调用 Solution.groupAnagrams(...)，共 {len(CASES)} 个用例")
    for name, args, want, *rest in CASES:      # 【语法】*rest 收集可选的第 4 个元素（比较器）
        checker = rest[0] if rest else eq
        got = Solution().groupAnagrams(*args)  # 【语法】*args 把元组拆成多个位置实参
        total += 1
        ok = checker(got, want)
        failed += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print(f"         入参：{args}")
            print(f"         期望：{want!r}")   # {值!r} 用 repr() 打印，能区分 1 和 "1"
            print(f"         实际：{got!r}")

    # 第 1.5 关：进阶解法（计数键）也过一遍同一批用例，防止写错
    print(f"[算法层] 进阶解法 SolutionCountKey.groupAnagrams(...)，共 {len(CASES)} 个用例")
    for name, args, want, *rest in CASES:
        checker = rest[0] if rest else eq
        got = SolutionCountKey().groupAnagrams(*args)
        total += 1
        ok = checker(got, want)
        failed += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}（进阶解法）")
        if not ok:
            print(f"         入参：{args}")
            print(f"         期望：{want!r}")
            print(f"         实际：{got!r}")

    # 第 2 关：走完整 IO 链路（解析 -> 算法 -> 格式化）
    print(f"[IO 层] solve(stdin 文本) 端到端，共 {len(IO_CASES)} 个用例")
    for name, text, want in IO_CASES:
        got = solve(text)
        total += 1
        ok = got == want
        failed += 0 if ok else 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print(f"         输入：{text!r}")
            print(f"         期望：{want!r}")
            print(f"         实际：{got!r}")

    print("-" * 60)
    print(f"合计 {total} 个用例：通过 {total - failed}，失败 {failed}")
    if failed:
        print("存在失败用例，退出码 1（可直接挂到 CI 或 git pre-commit 上）")
    print("-" * 60)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())                 # 【API】sys.exit(code)：抛出 SystemExit 结束进程，
                                     #   code 为 0 表示成功，非 0 表示失败，shell / CI 据此判断
