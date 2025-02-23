import math

# 삼각함수를 이용해 두 점 사이의 거리 구하기
"""
arctan((y2-y1)/(x2-x1)) = degree
"""

# 두 점의 좌표
start = (1, 1)
end = (2, 2)

a = abs(end[0] - start[0])    # x 좌표의 차이
b = abs(end[-1] - start[-1])    # y 좌표의 차이

# 두 점 사이의 거리
r = math.sqrt(a**2 + b**2)

# 아크 탄젠트를 이용하기
radian = math.atan(b/a)

print(r, math.degrees(radian))


# ----------------------------------------------------------------------- #
# 1쿠션 계산법
# 내 공이 정사영까지 이동하기 위한 각도
PI = 3.141592

# 세타 계산
def calculate_theta(x1, y1, x2, y2):
    # 1. 내 공과 정사영까지의 x 거리 a
    a = x2 - x1
    # 2. 내 공과 정사영까지의 y 거리 b
    b = y1 + y2
    # 3. 내 공이 법선과 벽의 교차점으로 이동하기 위한 방향
    tan_theta = a/b
    theta = math.atan(tan_theta)
    
    return theta

x1, y1 = 1.0, 2.0    # 내 공의 초기 위치
x2, y2 = 5.0, 1.0    # 목표 위치

# 세타 계산
alpha = calculate_theta(x1, y1, x2, y2)

# 출력
print(f'내 공의 출발 각도 (라디안): {alpha}')
print(f'내 공의 출발 각도 (degree): {alpha * 180/PI}도')

# ------------------------------------------------------------------------ #
# 스트레이트 샷 - 분리각 계산법
def straight_shot(myball, target, hole):
    # 1. 내 공의 hole 방향 각도
    x = abs(myball[0] - hole[0])
    y = abs(myball[-1], hole[-1])
    
    ga = math.atan(x/y)
    
    # 2. 내 공과 접점 사이의 거리
