num = 20
str_s = ''
for i in range(num):
    str_s = str_s + '%s,'
str_s = str_s[:-1]

print(str_s)

def main():
    # Generate data
    values = []
    print("Generate data")
    for i in range(100000):
        name = "name_{}".format(i)
        value = i
        text = "text_{}".format(i)
        values.append([name,value,text])
    print("Length of data: {}".format(len(values)))
    print()


if __name__ == "__main__":
    main()
