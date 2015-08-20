from decimal import Decimal
from unittest import TestCase

from graphql.lexer import GraphQLLexer
from graphql.exceptions import LexerError


class GraphQLLexerTest(TestCase):
    lexer = GraphQLLexer()

    def assert_output(self, lexer, expected):
        actual = list(lexer)
        len_actual = len(actual)
        len_expected = len(expected)
        self.assertEqual(
            len_actual,
            len_expected,
            'Actual output length %s does not match expected length %s\n'
            'Actual: %s\n'
            'Expected: %s' % (len_actual, len_expected, actual, expected)
        )
        for i, token in enumerate(actual):
            self.assertEqual(token.type, expected[i][0])
            self.assertEqual(token.value, expected[i][1])

    def test_punctuator(self):
        self.assert_output(self.lexer.input('!'), [('BANG', '!')])
        self.assert_output(self.lexer.input('$'), [('DOLLAR', '$')])
        self.assert_output(self.lexer.input('('), [('PAREN_L', '(')])
        self.assert_output(self.lexer.input(')'), [('PAREN_R', ')')])
        self.assert_output(self.lexer.input(':'), [('COLON', ':')])
        self.assert_output(self.lexer.input('='), [('EQUALS', '=')])
        self.assert_output(self.lexer.input('@'), [('AT', '@')])
        self.assert_output(self.lexer.input('['), [('BRACKET_L', '[')])
        self.assert_output(self.lexer.input(']'), [('BRACKET_R', ']')])
        self.assert_output(self.lexer.input('{'), [('BRACE_L', '{')])
        self.assert_output(self.lexer.input('}'), [('BRACE_R', '}')])
        self.assert_output(self.lexer.input('...'), [('SPREAD', '...')])

    def test_name(self):
        for name in ('a', 'myVar_42', '__LOL__', '_', '_0'):
            self.assert_output(self.lexer.input(name), [('NAME', name)])

    def test_reserved_words(self):
        reserved = ('fragment', 'query', 'mutation', 'on',
                    'true', 'false', 'null')
        for word in reserved:
            self.assert_output(self.lexer.input(word), [(word.upper(), word)])

    def test_int(self):
        for val in ('0', '-0', '42', '-42'):
            self.assert_output(
                self.lexer.input(val),
                [('INT_VALUE', int(val))],
            )

    def test_float(self):
        for val in ('-0.5e+42', '42.0', '2E64', '2.71e-0002'):
            self.assert_output(
                self.lexer.input(val),
                [('FLOAT_VALUE', Decimal(val))],
            )

    def test_string(self):
        for s in ('""', u'""', '"42"', r'"\t\n\u0042 ^"'):
            self.assert_output(self.lexer.input(s), [('STRING_VALUE', s)])

    def test_comment(self):
        lexer = self.lexer.input("""
            42 # lol this is a number. But this -> 9000 is not.
            "" # lol this is a string. But this -> "gav" is not.
            # lol the whole line commented
            #
        """)
        self.assert_output(lexer, [('INT_VALUE', 42), ('STRING_VALUE', '""')])

    def test_illegal_chars(self):
        for s in ('"', '^'):
            try:
                list(self.lexer.input(s))
                self.fail('Illegal char exception not raised for %s' % repr(s))
            except LexerError as e:
                self.assertEqual(1, e.line)
                self.assertEqual(1, e.column)
                self.assertTrue(
                    str(e).startswith('Line 1, col 1: Illegal character')
                )
                self.assertEqual(s, e.value)

    def test_positional_info(self):
        for i, t in enumerate(self.lexer.input('1\n  3\n    5\n')):
            self.assertEqual(i + 1, t.lineno)
            self.assertEqual(i * 2 + 1, self.lexer.find_column(t))

