import unittest
from string import ascii_lowercase
from godfather.utils.text_manager import TextManager


class TextManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.five_num_gen = (str(i) for i in range(5))
        self.five_letters_gen = (
            lett for i, lett in enumerate(ascii_lowercase) if i < 5
        )

    def _rand_str_seq_one(self):
        yield "Trains."
        yield "George Washington."
        yield "Washing machine."

    def _rand_str_seq_two(self):
        yield "Jester"
        yield "Mafia Member"
        yield "Arsonist"

    def test_lines_compiler_without_codeblock(self):
        test_values = (
            (self.five_num_gen, "0\n1\n2\n3\n4"),
            (self.five_letters_gen, "a\nb\nc\nd\ne"),
            (self._rand_str_seq_one(), "Trains.\nGeorge Washington."
                "\nWashing machine."),
            (self._rand_str_seq_two(), "Jester\nMafia Member\nArsonist")
        )

        for generator, expected in test_values:
            with self.subTest(generator=generator, expected=expected):
                self.assertEqual(
                    TextManager.compile_lines(generator), expected
                )

    def test_lines_compiler_with_codeblock(self):
        test_values = (
            (self.five_num_gen, "```\n0\n1\n2\n3\n4\n```"),
            (self.five_letters_gen, "```\na\nb\nc\nd\ne\n```"),
            (self._rand_str_seq_one(), "```\nTrains.\nGeorge Washington."
                "\nWashing machine.\n```"),
            (self._rand_str_seq_two(), "```\nJester\nMafia Member\n"
                "Arsonist\n```")
        )

        for generator, expected in test_values:
            with self.subTest(generator=generator, expected=expected):
                self.assertEqual(
                    TextManager.compile_lines(generator, codeblock=True),
                    expected
                )

    def test_lines_compiler_mix_codeblock_two(self):
        test_values = (
            (
                'Opening line without, preceeding list with.',
                ('This is a list of numbers!', self.five_num_gen),
                (False, True),
                'This is a list of numbers!\n```\n0\n1\n2\n3\n4\n```'
            ),

            (
                'Opening line with, preceeding list without.',
                (self.five_letters_gen, 'Choose your letters wisely.'),
                (True, False),
                '```\na\nb\nc\nd\ne\n```\nChoose your letters wisely.'
            ),

            (
                'Double code blocks.',
                (
                    (str(i) for i in range(5, 10)),
                    (str(i) for i in range(10, 15))
                ),
                (True, True),
                '```\n5\n6\n7\n8\n9\n```\n```\n10\n11\n12\n13\n14\n```'
            ),

            (
                'Two without code blocks.',
                (self._rand_str_seq_one(), self._rand_str_seq_two()),
                (False, False),
                'Trains.\nGeorge Washington.\nWashing machine.\nJester\n'
                'Mafia Member\nArsonist'
            )
        )

        for msg, lines, codeblock_bool, expected in test_values:
            with self.subTest(msg=msg, lines=lines,
                              codeblock_bool=codeblock_bool,
                              expected=expected):
                self.assertEqual(
                    TextManager.compile_msg_blocks(
                        (lines[0], codeblock_bool[0]),
                        (lines[1], codeblock_bool[1])
                    ),
                    expected
                )

    def test_lines_compiler_mix_codeblock_three(self):
        EXPECTED_ONE = ("```\n0\n1\n2\n3\n4\n```\na\nb\nc\nd\ne\n"
                        "```\n5\n6\n7\n8\n9\n```")

        EXPECTED_TWO = ("Below is a list of things you should not forget.\n"
                        "```\nTrains.\nGeorge Washington."
                        "\nWashing machine.\n```\n"
                        "```\nJester\nMafia Member\nArsonist\n```")

        test_values = (
            (
                [
                    (self.five_num_gen, True),
                    (self.five_letters_gen, False),
                    ((str(i) for i in range(5, 10)), True)
                ],
                EXPECTED_ONE
            ),

            (
                [
                    ("Below is a list of things you should not forget.", False),
                    (self._rand_str_seq_one(), True),
                    (self._rand_str_seq_two(), True)
                ],
                EXPECTED_TWO
            )
        )

        for func_args, expected in test_values:
            with self.subTest(func_args=func_args, expected=expected):
                self.assertEqual(
                    TextManager.compile_msg_blocks(*func_args),
                    expected
                )
