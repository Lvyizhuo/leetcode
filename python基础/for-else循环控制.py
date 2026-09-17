# for else 正常执行完for循环后才执行else语句块，如果for循环中执行了break语句，则不会执行else语句块。



# 场景：遍历列表查找特定元素
fruits = ["apple", "banana", "orange", "grape"]

# 使用 for-else
print("=== 使用 for-else ===")
for fruit in fruits:
    if fruit == "orange":
        print(f"找到: {fruit}")
        break
    print(f"检查: {fruit}")
else:
    print("未找到目标")

print("\n=== 不使用 break ===")
# 另一种写法（不使用 else）
found = False
for fruit in fruits:
    if fruit == "orange":
        print(f"找到: {fruit}")
        found = True
        break
    print(f"检查: {fruit}")

if not found:
    print("未找到目标")