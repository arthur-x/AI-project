import math

# 四个参数为a经纬度b经纬度（角度）
# 返回 b 相对于 a 的方位角 范围0~360 0为正北顺时针 值域可以在tmpA后面自己调
# 注意因为math.pi的不精确与浮点数计算 存在一定误差（极小）无法确定是否有后期影响
# 注意本假设中将地球看作标准球，实际有椭球误差的可能存在


def angle(aj, aw, bj, bw):
    j1 = aj / 180 * math.pi
    w1 = aw / 180 * math.pi
    j2 = bj / 180 * math.pi
    w2 = bw / 180 * math.pi
    r90 = math.pi/2

    cosc = math.cos(r90-w2)*math.cos(r90-w1) + math.sin(r90-w2)*math.sin(r90-w1)*math.cos(j2-j1)
    sinc = math.sqrt(1-cosc**2)
    sinA = math.sin(r90-w2)*math.sin(j2-j1)/sinc

    tmpA = math.asin(sinA)/math.pi*180  # sinA是方位角的正弦值 反三角函数时考虑一下值域
    
    if (w2 < w1):
        tmpA = 180-tmpA

    if tmpA<0:
        tmpA += 360
    
    return tmpA  

#  TEST
#print(angle(180,70,0,80))