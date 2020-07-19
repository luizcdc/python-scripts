from collections import OrderedDict
ncases = int(input())
for _ in range(ncases):
    input()
    perm_merged = map(int, input().split())
    log = OrderedDict()
    for x in perm_merged:
        log[x] = None

    for x in log.keys():
        print(x, end=' ')
    print()
