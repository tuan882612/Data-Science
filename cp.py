def out(n):
    print(n)
    if n != 1:
        if n % 2 == 0:
            n = n//2
        else:
            n = n*3 + 1
        return out(n)
        
if __name__ == "__main__":
    print(out(int(input())))