def parse(s):
    s += '\n'
    res = []
    token = ""
    quoteDepth = 0
    inString = False
    for c in s:
        if c.isspace() and token and quoteDepth == 0 and not inString:
            res.append(token)
            token = ""
        elif c == '"':
            inString = not inString
            token += c
        elif c == '[':
            quoteDepth = quoteDepth + 1
            token += c
        elif c == ']':
            quoteDepth = quoteDepth - 1
            token += c
        elif not c.isspace() or inString or quoteDepth > 0:
            token += c
    return res
