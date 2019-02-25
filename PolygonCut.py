from DataStruct import *
import sys

# 进出性判断有些问题
# TODO 进出性的判断 点在边上的两种情况的判断

def isVertexInPolygon(v, list):
    judgeIndex = 0
    for i in range(len(list)):
        j = i + 1
        minY = min(list[i % len(list)].y, list[j % len(list)].y)
        maxY = max(list[i % len(list)].y, list[j % len(list)].y)
        if v.y > maxY or v.y < minY:
            continue
        if maxY == minY:    # 同一水平线上
            if v.x > max(list[i % len(list)].x, list[j % len(list)].x): # 点在线段右边 看成一个交点
                judgeIndex += 1
                continue
            elif v.x < min(list[i % len(list)].x, list[j % len(list)].x): # 点在线段左边 无交点
                continue
            else:   # 点在线段上
                return True
        # 做射线
        x = (list[i % len(list)].x - list[j % len(list)].x) / (list[i % len(list)].y - list[j % len(list)].y) * (v.y - list[i % len(list)].y) + list[i % len(list)].x
        if(abs(v.x - x)) < sys.float_info.epsilon: # 点在线上
            return None
        if v.x > x: # 有交点
            judgeIndex += 1
    if judgeIndex % 2 != 0:
        return True
    return False

def getX(v):
    return v.x
def getY(v):
    return v.y

def CutByVerticalLine(s1, s2, list):
    assert s1.x == s2.x
    crossXs = []
    x = s1.x

    shearedList = [Vertex(r.x, r.y) for r in list]

    minY = min(s1.y, s2.y)
    maxY = max(s1.y, s2.y)

    for i in range(len(list)):
        vertex = list[i]
        c1 = shearedList[i % len(list)]
        c2 = shearedList[(i + 1) % len(list)]

        if(c1.x == c2.x and c1.x == x):
            continue    # 重合
        if(c1.x > x and c2.x > x):
            continue    # 不相交
        if(c1.x < x and c2.x < x):
            continue

        y = float('%.9f' % LineCrossV(x, c1, c2))

        inters = Intersection(x, y)

        next = None
        if((y > minY and y < maxY)                  # 交点在s1s2中
        # or (c2.y == y and x == s2.x)                # 线段交点在双方末端（在首端无视）
        # or (c1.y == y and x == s1.x)
        or (c2.x == x and y == s1.y)                # 交点在端点的时候，一条线段的首和另一条的尾才能有交点，上述注释做法在某种情况失效
        or (c1.x == x and y == s2.y)
        or (y == minY and c1.x != x and c2.x != x)  # 交点在s1s2一端
        or (y == maxY and c1.x != x and c2.x != x)):
            while not ((isinstance(vertex, Vertex) and isinstance(vertex.next, Vertex)) or (isinstance(vertex, Intersection) and isinstance(vertex.nextS, Vertex))):
                if isinstance(vertex, Vertex):
                    assert isinstance(vertex.next, Intersection)
                    if (c1.x < c2.x and inters.x < vertex.next.x) or (c1.x > c2.x and inters.x > vertex.next.x):    # c1c2的横坐标不可能相同，否则和s1s2重合
                        break
                    vertex = vertex.next
                else:
                    assert isinstance(vertex.nextS, Intersection)
                    if (c1.x < c2.x and inters.x < vertex.nextS.x) or (c1.x > c2.x and inters.x > vertex.nextS.x):
                        break
                    vertex = vertex.nextS
            if isinstance(vertex, Vertex):
                next = vertex.next
            else:
                next = vertex.nextS
            if isinstance(vertex, Vertex):
                vertex.next = inters
            else:
                assert isinstance(vertex, Intersection)
                vertex.nextS = inters
            inters.nextS = next
            print("s1:%s, s2:%s, c1:%s, c2:%s, inter:%s" % (("%f, %f" % (s1.x, s1.y)), ("%f, %f" % (s2.x, s2.y)), ("%f, %f" % (c1.x, c1.y)), ("%f, %f" % (c2.x, c2.y)), ("%f, %f" % (inters.x, inters.y))))
            crossXs.append(inters)
    return crossXs

def LineCrossH(y, c1, c2):
    return c1.x + (c2.x - c1.x) * (y - c1.y) / (c2.y - c1.y)

def LineCrossV(x, c1, c2):
    return c1.y + (c2.y - c1.y) * (x - c1.x) / (c2.x - c1.x)

def CutByLine(s1, s2, list):
    if s1.x == s2.x:
        return CutByVerticalLine(s1, s2, list)
    crossXs = []

    # 错切变换
    slope = (s2.y - s1.y) / (s1.x - s2.x)
    y = s1.x * slope + s1.y
    shearedList = [Vertex(r.x, r.x * slope + r.y) for r in list]

    minX = min(s1.x, s2.x)
    maxX = max(s1.x, s2.x)

    for i in range(len(list)):
        vertex = list[i]
        c1 = shearedList[i % len(list)]
        c2 = shearedList[(i + 1) % len(list)]

        if(c1.y == c2.y and c1.y == y):
            continue    # 重合
        if(c1.y > y and c2.y > y):
            continue    # 不相交
        if(c1.y < y and c2.y < y):
            continue

        x = float('%.9f' % LineCrossH(y, c1, c2))
        npy = y - x * slope
        inters = Intersection(x, npy)

        next = None

        if((x > minX and x < maxX)                  # 交点在s1s2中
        # or (c2.y == y and x == s2.x)                # 线段交点在双方末端（在首端无视）
        # or (c1.y == y and x == s1.x)
        or (c2.y == y and x == s1.x)                # 交点在端点的时候，一条线段的首和另一条的尾才能有交点，上述注释做法在某种情况失效
        or (c1.y == y and x == s2.x)
        or (x == minX and c1.y != y and c2.y != y)  # 交点在s1s2一端
        or (x == maxX and c1.y != y and c2.y != y)):
            # 查找插入点
            while not ((isinstance(vertex, Vertex) and isinstance(vertex.next, Vertex)) or (isinstance(vertex, Intersection) and isinstance(vertex.nextS, Vertex))):    # 如果下一个点是交点
                if isinstance(vertex, Vertex):
                    assert isinstance(vertex.next, Intersection)
                    # 下一个点应该在交点后，break执行插入
                    if (c1.x < c2.x and inters.x < vertex.next.x) \
                            or (c1.x > c2.x and inters.x > vertex.next.x)\
                            or (c1.y > c2.y and inters.y > vertex.next.y)\
                            or (c1.y < c2.y and inters.y < vertex.next.y):      # 后两个是垂直情况只能用y坐标判断
                        break
                    vertex = vertex.next
                else:
                    assert isinstance(vertex.nextS, Intersection)
                    if (c1.x < c2.x and inters.x < vertex.nextS.x)\
                            or (c1.x > c2.x and inters.x > vertex.nextS.x)\
                            or (c1.y > c2.y and inters.y > vertex.nextS.y)\
                            or (c1.y < c2.y and inters.y < vertex.nextS.y):
                        break
                    vertex = vertex.nextS
            if isinstance(vertex, Vertex):
                next = vertex.next
            else:
                next = vertex.nextS
            if isinstance(vertex, Vertex):
                vertex.next = inters
            else:
                assert isinstance(vertex, Intersection)
                vertex.nextS = inters
            inters.nextS = next
            print("s1:%s, s2:%s, c1:%s, c2:%s, inter:%s" % (("%f, %f" % (s1.x, s1.y)), ("%f, %f" % (s2.x, s2.y)), ("%f, %f" % (c1.x, c1.y - c1.x * slope)), ("%f, %f" % (c2.x, c2.y - c2.x * slope)), ("%f, %f" % (inters.x, inters.y))))
            crossXs.append(inters)

    return crossXs

def Compose(list):
    result = []
    # for inters in list:
    #     print(inters.x)
    #     print(inters.y)
    #     print(inters.crossDi)
    for inters in list:
        assert isinstance(inters, Intersection)
        if(not inters.used) and inters.crossDi == 0:    # 没用过并且表示进
            oneResult = []
            oneResult.append(Vertex(inters.x, inters.y))
            inters.used = True
            loopvar = inters.nextS
            while loopvar != None:
                oneResult.append(Vertex(loopvar.x, loopvar.y))
                if isinstance(loopvar, Intersection):
                    curr = loopvar
                    curr.used = True
                    next = curr.nextS if curr.crossDi == 0 else curr.nextC
                elif isinstance(loopvar, Vertex):
                    curr = loopvar
                    next = curr.next
                if next is inters:
                    break
                loopvar = next
            result.append(oneResult)
    return result

def processNoCross(listS, listC):
    sInC = isVertexInPolygon(listS[0], listC)
    if sInC:
        return listS
    cInS = isVertexInPolygon(listC[0], listS)
    if cInS:
        return listC
    return []

def printList(start, isS):
    assert isinstance(start, Vertex)
    next = start.next
    print("#######################################################################")
    if isS:
        print("list S:")
        print(str(start.x) + "," + str(start.y))
        while next != start:
            print(str(next.x) + "," + str(next.y))
            if isinstance(next, Vertex):
                next = next.next
            else:
                assert isinstance(next, Intersection)
                next = next.nextS
    else:
        print("list C:")
        print(str(start.x) + "," + str(start.y))
        while next != start:
            print(str(next.x) + "," + str(
                next.y))
            if isinstance(next, Vertex):
                next = next.next
            else:
                assert isinstance(next, Intersection)
                next = next.nextC
    print("#######################################################################")


#---------------------------------------------------------
# 测试数据(数据默认顺时针方向)
# S = "161 137 429 376 558 192 619 418 281 431"
# C = "183 391 224 240 610 107 657 361 429 376"

# C包含S
# S = "281 159 472 155 569 248 506 419 242 366"
# C = "149 241 282 72 559 111 628 406 418 475 170 407"

# S包含C
# S = "259 113 689 107 548 481 103 374"
# C = "306 178 565 160 596 263 441 387 255 326"

# 完全不相交
# S = "79 176 221 169 341 240 282 430 52 429"
# C = "456 111 680 172 691 287 413 320"

# 底边重合
# S = "247 183 536 181 536 374 129 374"
# C = "128 71 295 70 455 374 263 374"

# 文档示例1
S = "70 104 227 357 281 219 412 455 625 299 688 484 120 487"
C = "125 256 689 242 710 427 40 371"

# 文档示例2
# S = "126 121 335 391 575 194 633 442 169 434"
# C = "176 234 622 132 656 362 90 328"

# 文档示例3
# S = "173 106 333 366 663 232 663 457 128 443"
# C = "81 183 737 179 713 379 59 292"

# 点在边上重合（图5-右）
# S = "180 115 357 115 378 293 180 293"
# C = "123 115 304 115 304 232 44 232"

# 点在边上
# S = "242 78 480 77 480 289 242 289"
# C = "162 110 388 19 386 103 162 247"
#---------------------------------------------------------
# 解析坐标
def PolyClipping(S, C):
    S_int = list(map(int, S.strip().split()))
    C_int = list(map(int, C.strip().split()))
    listS = []
    listC = []
    listI = []
    X = S_int[0::2]
    Y = S_int[1::2]
    assert len(X) == len(Y)
    for i in range(len(X)):
        listS.append(Vertex(X[i], Y[i]))
    X = C_int[0::2]
    Y = C_int[1::2]
    assert len(X) == len(Y)
    for i in range(len(X)):
        listC.append(Vertex(X[i], Y[i]))

    # 链接链表
    for i in range(len(listS)):
        listS[i - 1].next = listS[i]
    for i in range(len(listC)):
        listC[i - 1].next = listC[i]

    startS = listS[0]
    startC = listC[0]

    # 开始切割
    for cutStartIdx in range(len(listC)):
        s1 = listC[cutStartIdx]
        s2 = listC[(cutStartIdx + 1) % len(listC)]

        inters = CutByLine(s1, s2, listS)
        if len(inters) == 0:
            continue

        # 交点排序 准备插入
        if s1.x < s2.x:
            inters.sort(key=getX)
        elif s1.x == s2.x:
            assert s1.y != s2.y
            if s1.y < s2.y:
                inters.sort(key=getY)
            else:
                inters.sort(key=getY, reverse=True)
        else:
            inters.sort(key=getX, reverse=True)

        # 加入到listI
        for v in inters:
            listI.append(v)

        # 插入到C中
        s1.next = inters[0]
        for i in range(len(inters) - 1):
            inters[i].nextC = inters[i + 1]
        inters[len(inters) - 1].nextC = s2


    if len(listI) == 0: # 没有交点
        return [processNoCross(listS, listC)]

    # 按照S链表交点顺序记录进出性
    flag = 1
    startVertical = startS
    indexVertical = startVertical.next
    while indexVertical != startVertical:
        if isinstance(indexVertical, Vertex):
            indexVertical = indexVertical.next
        else:
            assert isinstance(indexVertical, Intersection)
            indexVertical.crossDi = flag
            flag = 1 if flag == 0 else 0
            indexVertical = indexVertical.nextS

    printList(startS, True)
    printList(startC, False)
    # 按规则连接交点
    return  Compose(listI)


print("####################")
result = PolyClipping(S, C)
for r in result:
    for re in r:
        print(str(re.x) + "," + str(re.y))
    print("####################")
