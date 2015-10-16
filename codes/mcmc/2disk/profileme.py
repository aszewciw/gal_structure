
x = 1000
y = 2000

@profile
def main():
    for i in range(x):
        print(y/x)

if __name__ == '__main__':
    main()
