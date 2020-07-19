ncases = int(input())
for _ in range(ncases):
    X, Y, Z = map(int, input().split())

    A = [X, Y]
    B = [X, Z]
    C = [Y, Z]
    found = False
    for a in A:
        for b in B:
            for c in C:
                if X == max(a, b) and Y == max(a, c) and Z == max(b, c):
                    print("YES")
                    print(a, b, c)
                    found = True
                    break
            else:
                continue
            break
        else:
            continue
        break

    if not found:
        print("NO")
