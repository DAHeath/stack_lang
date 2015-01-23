from parse import parse

def tokenToValue(token):
    try:
        return int(token)
    except:
        try:
            return float(token)
        except:
            if token == 'True':
                return True
            elif token == 'False':
                return False
            else:
                return token


class Env():
    def __init__(self, stack, dictionary):
        self.stack      = stack
        self.dictionary = dictionary

    def eval(self, token):
        """
        eval updates the environment based on the token
        """
        value = tokenToValue(token)
        try:
            if value.startswith("'"):
                self.stack.append(value[1:])
            elif value.startswith('"') or value.startswith('['):
                self.stack.append(value)
            else:
                f = self.dictionary[token]
                try:
                    f(self)
                except:
                    self.doQuote(f)
        except:
            self.stack.append(value)

    def topOfStack(self):
        return self.stack.pop()

    def execute(self, s):
        tokens = parse(s)
        for t in tokens:
            self.eval(t)

    def doQuote(self, q):
        self.execute(q[1:len(q)-1])
