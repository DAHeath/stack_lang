from stdlib import globalEnv

import sys
if __name__ == '__main__':
    env = globalEnv()
    env.execute(sys.stdin.read())
    print env.stack
