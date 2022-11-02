x = input("请输入一个三位数：")
x = int(x)
a, b = divmod(x, 100)  # x/100后将得到的值存到a，模到b中
print(b)
b, c = divmod(b, 10)
print(a, b, c)
