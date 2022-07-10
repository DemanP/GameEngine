from math import sin, cos

def multiply(X, Y):
    result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
    return result
def rotation(angle): 
    return [
    [ cos(angle), -sin(angle) ],
    [ sin(angle), cos(angle) ]
    ]