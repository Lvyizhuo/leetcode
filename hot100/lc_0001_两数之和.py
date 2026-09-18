def two_sum(nums: list[int], target: int) -> list[int]:
    hashmap = {}
    
    for idx , num in enumerate(nums):
        complement = target - num
        if complement in hashmap:
            return [hashmap[complement],idx]
        hashmap[num] = idx
    return []




def main():
    """ACM OJ 入口：只处理IO，OJ提交时执行这里"""
    import sys
    # 一次性读取所有输入，过滤空行，避免EOF异常，适配多组测试用例
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    ptr = 0  # 指针，用来逐行读取输入
    # 循环读取多组用例，直到读完所有输入
    while ptr < len(input_lines):
        # 当前行转为数组
        nums = list(map(int, input_lines[ptr].split()))
        ptr += 1
        # 下一行读取目标值 target
        target = int(input_lines[ptr])
        ptr += 1
        # 调用核心算法函数计算答案
        ans = two_sum(nums, target)
        # 输出两个下标，空格分隔，OJ标准输出格式
        print(ans[0], ans[1])


def run_test():
    """本地单元测试，仅本地调试使用，OJ不会执行"""
    # 测试用例1
    assert two_sum([2,7,11,15],9) == [0,1]
    # 测试用例2
    assert two_sum([3,2,4],6) == [1,2]
    # 测试用例3，两个相同数字
    assert two_sum([3,3],6) == [0,1]
    print("✅ 全部测试用例通过")


if __name__ == "__main__":
    # ========== 切换开关 ==========
    # 本地调试：启用 run_test()，自动跑单元测试验证算法
    # OJ提交：注释run_test()，启用 main()，读取标准输入输出答案
    run_test()
    # main()
