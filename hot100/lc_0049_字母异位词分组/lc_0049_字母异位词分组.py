#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# LeetCode 49. 字母异位词分组 (Group Anagrams)  |  难度：中等
# ------------------------------------------------------------
# 一句话：把互为"字母异位词"的字符串分到同一组（异位词 = 组成字母完全相同、只是顺序不同）。
# 涉及知识点：哈希表（dict）· 字符串排序做键 · setdefault · 空间换时间
#
# 提交方式：**整个文件就是 ACM/OJ 提交代码**——顶层直接跑 main()，从 stdin 读、往 stdout 写。
#
# 本地判题（in.txt 里串了 7 组用例）：
#     python lc_0049_字母异位词分组.py < in.txt
#     diff <(python lc_0049_字母异位词分组.py < in.txt) out.txt && echo PASS
#
# 脚本结构（四段解耦，改题时只动对应那一段）：
#   ① class Solution  -- 纯算法，与 LeetCode 提交区一致，不碰任何 IO
#   ② parse_input()   -- stdin 文本 -> 逐组实参（唯一负责"读"的地方）
#   ③ format_output() -- 算法返回值 -> 输出字符串（唯一负责"写"的地方）
#   ④ main()          -- ACM 主流程：逐组算、逐组输出
#
# 注释约定（算法层强制）：每个 API / 关键字 / 语法糖首次出现处都要解释，
# 三要素齐全 -- 作用 · 关键参数（含默认值）· 返回或副作用；同一 API 之后只写短注释。
# ============================================================

import sys
from typing import List


# ============================================================
# ① 核心算法：可整段复制回 LeetCode 提交区（方法签名与题面完全一致）
#    - 只依赖标准库
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
        空间复杂度 O(n·k)：哈希表存下所有词，也就是答案本身。

        关键 Python 语法（首次出现处详解，后续同款写法不再展开）：
          - dict.setdefault(key, default)：键不存在时先写入默认值再返回，
            省掉 "if key not in d: d[key] = []" 两行判断；返回的是表里那个列表
            本身（引用），对它 append 就直接改进了表。
          - sorted(iterable)：返回排好序的"新列表"，不原地修改原对象；对字符串
            按字符 Unicode 码点逐个排，如 sorted("eat") -> ['a', 'e', 't']。
          - "".join(可迭代对象)：把字符列表拼回字符串，字符串可哈希，能当字典键。
          - dict.values()：返回所有值组成的"动态视图"（不是拷贝），
            视图随字典变化，list() 包一层转成普通列表。
        """
        groups = {}                                # 【dict】分组键(排序后的词) -> 该组的词列表

        for s in strs:                             # 每个词只处理一遍
            key = "".join(sorted(s))               # 排序后作键："eat"/"tea"/"ate" 全变成 "aet"
                                                   # 【API】sorted(可迭代对象)：返回新列表，默认升序；
                                                   #   参数 reverse 默认 False，key 默认 None（不指定比较依据）
                                                   # 【易错】sorted(s) 返回的是字符列表，必须 join 回字符串
                                                   #   才能做键；直接拿列表当键会因不可哈希报 TypeError
            groups.setdefault(key, []).append(s)   # 【API】setdefault(key, default)
                                                   #   作用：键不存在就先塞 default 再返回它，存在则直接返回旧值
                                                   #   关键参数：default 只在键缺失时生效，这里给空列表
                                                   #   返回：键对应的值（这里就是该组的列表，append 原地生效）
        return list(groups.values())               # 【API】dict.values()
                                                   #   作用：取出所有分组（每组一个列表）
                                                   #   返回：动态视图对象，list() 转成普通列表即为答案
                                                   #   【易错】直接 return groups.values() 类型是视图不是 List，
                                                   #   提交回 LeetCode 类型校验会报错，必须 list() 包一层


# ============================================================
# ② 输入解析层：stdin 原始文本 -> 逐组算法入参
#    唯一允许"读输入"的地方；交给算法的是干净的 Python 对象。
#    格式（见 题目.md）：每组两行 —— n / n 个字符串，多组依次排列，读到 EOF 为止。
# ============================================================
def parse_input(text: str):
    """把 stdin 全文按组切开，逐组 yield 该组的字符串列表 strs。

    【语法】yield 让函数变成生成器：main 里 for 一次拿一组，组数不定也能读到 EOF 自然结束。
    【语法】str.split() 不带参数 = 按任意空白切分并丢掉空串，所以每组的词写成一行或拆成多行都行。
    """
    tokens = text.split()
    pos = 0                                     # 游标推进，别用 pop(0)（O(n)，多组会退化）
    while pos < len(tokens):
        n = int(tokens[pos]); pos += 1           # 【API】int(字符串)：输入全是字符串，必须自己转类型
        strs = tokens[pos:pos + n]               # 词本身就是 token，不用转换，切片直接拿到 List[str]
        pos += n
        yield strs


# ============================================================
# ③ 输出格式化层：算法返回值 -> 该组用例的输出文本
#    只在这里做格式适配。本题的关键：分组本身是无序的，OJ 判题要求唯一答案，
#    所以这里把"组内单词"和"组间顺序"都规范化，保证同样输入恒定同样输出。
# ============================================================
def format_output(result) -> str:
    """一组异位词占一行，行内按字典序；行之间也按字典序排（多行文本，main 会再拼各组）。"""
    rows = [" ".join(sorted(g)) for g in result]    # 【语法】列表推导式：逐组把词排序后拼成一行
    rows.sort()                                     # 【API】list.sort()：原地排序（返回 None，不改赋值），
                                                    #   对比 sorted(list) 返回新列表、原列表不动
                                                    # 【易错】组间顺序不排的话，同一输入每次跑顺序可能不同，
                                                    #   会跟 out.txt 随机对不上
    return "\n".join(rows)


# ============================================================
# ④ 驱动层：ACM 主流程（顶层直接调用，提交时不加 __main__ 包裹）
# ============================================================
def main():
    outs = []
    for strs in parse_input(sys.stdin.read()):   # 【API】sys.stdin.read()：一次读完整个标准输入
                                                 #   返回 str；判题机把输入重定向进来，能读到全部内容
        outs.append(format_output(Solution().groupAnagrams(strs)))
    if outs:                                    # 空输入就别输出，否则会凭空多一个空行
        sys.stdout.write("\n".join(outs) + "\n")    # 【API】sys.stdout.write(s)：写字符串、不自动换行，
                                                    #   所以手动补 "\n"；比多组循环 print 更快


main()
