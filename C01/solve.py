nums = [106, 128, 117, 55, 127, 130, 123, 55, 117, 128, 102, 122, 123, 59, 121, 114, 102, 126, 59, 122, 102, 121, 112, 110, 111, 123, 132]
flag = ''.join(chr(n - 7) for n in nums)
print(flag)
# Output: cyn0x{t0ny_st4rk_w4s_right}
