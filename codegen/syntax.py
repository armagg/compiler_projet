def jpf(*o):
    return f'(JPF, {o[0]}, {o[1]}, )'


def jp(*o):
    return f'(JP, {o[0]}, , )'


def add(*o):
    return f'(ADD, {o[0]}, {o[1]}, {o[2]})'


def subtract(*o):
    return f'(SUB, {o[0]}, {o[1]}, {o[2]})'


def multiply(*o):
    return f'(MULT, {o[0]}, {o[1]}, {o[2]})'


def assign(*o):
    return f'(ASSIGN, {o[0]}, {o[1]}, )'


def lessthan(*o):
    return f'(LT, {o[0]}, {o[1]}, {o[2]})'


def equal(*o):
    return f'(EQ, {o[0]}, {o[1]}, {o[2]})'


def output(*o):
    return f'(PRINT, {o[0]}, , )'
