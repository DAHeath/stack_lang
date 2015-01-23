from pymonad import curry
import operator as op
from env import *
from parse import parse

def dup(env):
    x = env.stack.pop()
    env.stack.append(x)
    env.stack.append(x)

def drop(env):
    env.stack.pop()

def swap(env):
    a = env.stack.pop()
    b = env.stack.pop()
    env.stack.append(a)
    env.stack.append(b)

def over(env):
    a = env.stack.pop()
    b = env.stack.pop()
    env.stack.append(a)
    env.stack.append(b)
    env.stack.append(a)

def rot(env):
    a = env.stack.pop()
    b = env.stack.pop()
    c = env.stack.pop()
    env.stack.append(a)
    env.stack.append(c)
    env.stack.append(b)

def stdIf(env):
    alternative = env.stack.pop()
    consequent  = env.stack.pop()
    condition   = env.stack.pop()
    if condition == True:
        env.doQuote(consequent)
    else:
        env.doQuote(alternative)

def stdApply(env):
    env.doQuote(env.stack.pop())

def define(env):
    name = env.stack.pop()
    body = env.stack.pop()
    env.dictionary[name] = body

@curry
def biop(f, env):
    b = env.stack.pop()
    a = env.stack.pop()
    env.stack.append(f(a, b))

def head(env):
    q = env.stack.pop()
    token = parse(q[1:len(q)-1])[0]
    value = tokenToValue(token)
    env.stack.append(value)

def tail(env):
    q = env.stack.pop()
    token = parse(q[1:len(q)-1])[1:]
    res = '[' + ' '.join(token) + ']'
    env.stack.append(res)

def prepend(env):
    q = env.stack.pop()
    toPrepend = env.stack.pop()
    token = q[1:len(q)-1]
    if token:
        res = '[' + str(toPrepend) + ' ' + str(token) + ']'
    else:
        res = '[' + str(toPrepend) + ']'
    env.stack.append(res)

def globalEnv():
    d = {}
    # 'Keywords'
    d['def'] = define
    d['if'] = stdIf

    # Stack manipulations
    d['dup'] = dup
    d['drop'] = drop
    d['swap'] = swap
    d['over'] = over
    d['rot'] = rot

    # Ops
    d['!']  = stdApply
    d['+']  = biop(op.add)
    d['-']  = biop(op.sub)
    d['*']  = biop(op.mul)
    d['/']  = biop(op.div)
    d['<']  = biop(op.lt)
    d['>']  = biop(op.gt)
    d['<='] = biop(op.le)
    d['>='] = biop(op.ge)
    d['=']  = biop(op.eq)

    d['head'] = head
    d['tail'] = tail
    d['::'] = prepend
    return Env([], d)
