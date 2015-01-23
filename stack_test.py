import unittest
from stdlib import globalEnv
from parse import *

class Test(unittest.TestCase):
    def setUp(self):
        self.env = globalEnv()

    def test_parse(self):
        self.assertEqual(['a', 'b', 'c'], parse('a b c'))

    def test_parse_with_string(self):
        self.assertEqual(['a', '"hello world"', 'c'],
                parse('a "hello world" c'))

    def test_parse_with_newline(self):
        self.assertEqual(['a', 'b', 'c'], parse('a\nb c'))

    def test_parse_with_quote(self):
        self.assertEqual(['[dup *]', 'a', 'b'], parse('[dup *] a b'))

    def test_parse_decimal(self):
        self.env.execute('1.5')
        self.assertEqual([1.5], self.env.stack)

    def test_parse_nested_quotes(self):
        self.assertEqual(['[[ a ]]'], parse('[[ a ]]'))

    def assertTopIs(self, exp):
        self.assertEqual(exp, self.env.topOfStack())

    def test_eval(self):
        self.env.eval(5)
        self.assertTopIs(5)

    def test_eval_two(self):
        self.env.eval(5)
        self.env.eval(4)
        self.assertTopIs(4)

    def test_eval_adding(self):
        self.env.eval(5)
        self.env.eval(4)
        self.env.eval('+')
        self.assertTopIs(9)

    def test_eval_string(self):
        self.env.eval('"hello world"')
        self.assertTopIs('"hello world"')

    def test_eval_quote(self):
        self.env.eval('[dup *]')
        self.assertTopIs('[dup *]')

    def test_apply(self):
        self.env.execute('3 [dup *] !')
        self.assertTopIs(9)

    def test_if_true(self):
        self.env.execute('True [2] [4] if')
        self.assertTopIs(2)

    def test_if_false(self):
        self.env.execute('False [2] [4] if')
        self.assertTopIs(4)

    def test_definition(self):
        self.env.execute("[dup *] 'square def")
        self.env.execute('4 square')
        self.assertTopIs(16)

    def test_head(self):
        self.env.execute('[1 2 3] head')
        self.assertTopIs(1)

    def test_tail(self):
        self.env.execute('[1 2 3] tail')
        self.assertTopIs('[2 3]')

    def test_prepend(self):
        self.env.execute('1 [2 3] ::')
        self.assertTopIs('[1 2 3]')

    def test_prepend_empty(self):
        self.env.execute('1 [] ::')
        self.assertTopIs('[1]')

if __name__ == '__main__':
    unittest.main()
