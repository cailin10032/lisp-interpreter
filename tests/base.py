import unittest
from core.interpreter import interpret_one_sentence

class BaseTest(unittest.TestCase):

    def test_num(self):
        expr = '1'
        result = interpret_one_sentence(expr)
        self.assertEqual(result, 1)

    def test_arithmetic(self):
        self.assertEqual(interpret_one_sentence('(+ 1 2)'), 3)
        self.assertEqual(interpret_one_sentence('(/ (* (+ 1 2) (- 10 5)) 5)'), 3)
        self.assertEqual(interpret_one_sentence('(- 1)'), -1)
        self.assertEqual(interpret_one_sentence('(* 1 2 3)'), 6)

    def test_bind(self):
        expr = '(let ((x 2)) x)'
        self.assertEqual(interpret_one_sentence(expr), 2)

    def test_call(self):
        expr1 = '((lambda (x) (* x 2)) 3)'
        expr2 = '((lambda (x y) (* x y)) 2 5) '
        self.assertEqual(interpret_one_sentence(expr1), 6)
        self.assertEqual(interpret_one_sentence(expr2), 10)

    def test_lambda_bind(self):
        expr = '''
        (let ((f (lambda (x) (* x 2))))
            (f 4)
        )
        '''
        self.assertEqual(interpret_one_sentence(expr), 8)

    def test_closure(self):
        expr = '''
        (let ((x 2))
            (let ((f (lambda (y) (* x y))))
                (let ((x 4))
                    (f 3))))
        '''
        self.assertEqual(interpret_one_sentence(expr), 6)

    def test_condition(self):
        self.assertEqual(interpret_one_sentence('(if (= 1 1) 1 0)'), 1)
        self.assertEqual(interpret_one_sentence('(if (!= 1 1) 1 0)'), 0)
        self.assertEqual(interpret_one_sentence('(if (> 2 1) 1 0)'), 1)
        self.assertEqual(interpret_one_sentence('(if (>= 1 1) 1 0)'), 1)
        self.assertEqual(interpret_one_sentence('(if (< 1 2) 1 0)'), 1)
        self.assertEqual(interpret_one_sentence('(if (<= 1 1) 1 0)'), 1)

    def test_recursive(self):
        expr = '''
        (let
            ((f (lambda (self n)
                    (if (= n 1) 1 (* n (self self (- n 1))))
                )
            ))
            (f f 5)
        )
        '''
        self.assertEqual(interpret_one_sentence(expr), 120)

if __name__ == '__main__':
    unittest.main()
