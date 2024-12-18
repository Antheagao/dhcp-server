
print(hex(118))
print(0x02)
print(0xff)


if hex(2) == 0x02:
    print("yes")
else:
    print("no")

rat = []

rat.append(234)
rat.append(57)
rat.append(251)
rat.append(132)
rat.append(70)
rat.append(198)

rat3 = []
rat3.append(123)
rat3.append(241)
rat3.append(75)
rat3.append(226)
rat3.reverse()
rat4 = rat3
rat3 = bytes(rat3)

rat2 = bytes(rat)
print(rat2)
print(rat3)

print([0x00, 0x00, 0x00, 0x00])

print(bytes(192))

num = 46
print([1,2] + [3,4] + [num])