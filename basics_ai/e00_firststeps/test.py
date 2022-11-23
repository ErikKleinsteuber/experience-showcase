__author__ = 'johannes'
import unittest
import ex_firststeps as ex


class TestFirstSteps(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(ex.get_hello_world(), "Hello, World!")

    def test_answer_to_everything(self):
        self.assertEqual(ex.answer_to_everything(), 42)

    def test_flip(self):
        a, b, c = ex.flip(1, 2, 3)
        self.assertEqual(a, 2)
        self.assertEqual(b, 1)
        self.assertEqual(c, 3)

    def test_get_dict_entry(self):
        dic = {"Stefan": "Otte",
               "Johannes": "Kulick",
               "Marc": "Toussaint"}
        r = ex.get_dict_entry(dic, "Marc")
        self.assertEqual(r, "Toussaint")
