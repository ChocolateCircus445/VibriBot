scorevals = (
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [8, 7, 6, 5, 4, 3, 2],
    [36, 28, 21, 15, 10, 6, 3],
    [120, 84, 56, 35, 20, 10, 4],
    [330, 210, 126, 70, 35, 15, 5],
    [792, 462, 252, 126, 56, 21, 6],
    [1716, 924, 462, 210, 84, 28, 7],
    [3432, 1716, 792, 330, 120, 36, 8],
    [6435, 3003, 1287, 495, 165, 45, 9],
    [11440, 5005, 2002, 715, 220, 55, 10],
    [19448, 8008, 3003, 1001, 286, 66, 11],
    [31824, 12376, 4368, 1365, 364, 78, 12],
    [50388, 18564, 6188, 1820, 455, 91, 13],
    [77520, 27132, 8568, 2380, 560, 105, 14]
)


def calculate(num):
    global scorevals
    curval = num
    res = ""
    for place in range(0, 7):
        for compval in reversed(range(0,len(scorevals))):
            if curval < scorevals[compval][place]:
                continue
            else:
                res += str(compval) + " "
                curval = curval - scorevals[compval][place]
                break

    return res

if __name__ == "__main__":
    print(calculate(34))