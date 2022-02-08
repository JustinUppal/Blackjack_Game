"""Unit tests for the blackjack program."""
import unittest

import blackjack3


class TestBlackjack(unittest.TestCase):

    def test_score_basic(self):
        test = blackjack3.Hand([3])
        ret = test.score()
        self.assertEqual((3, 0), ret)

        test2 = blackjack3.Hand([3, 2])
        ret = test2.score()
        self.assertEqual((5, 0), ret)

        test3 = blackjack3.Hand([3, 2, 10])
        ret = test3.score()
        self.assertEqual((15, 0), ret)

        #         # 11 counts as 10
        test4 = blackjack3.Hand([3, 2, 10, 11])
        ret = test4.score()
        self.assertEqual((25, 0), ret)

    def test_part_one_cases(self):
        test5 = blackjack3.Hand([3, 12])
        self.assertEqual(test5.score(), (13, 0))

        test6 = blackjack3.Hand([5, 5, 10])
        self.assertEqual(test6.score(), (20, 0))

        test7 = blackjack3.Hand([11, 10, 1])
        self.assertEqual(test7.score(), (21, 0))

        test8 = blackjack3.Hand([1, 5])
        self.assertEqual(test8.score(), (16, 1))

        test9 = blackjack3.Hand([1, 1, 5])

        self.assertEqual(test9.score(), (17, 1))

        test10 = blackjack3.Hand([1, 1, 1, 7])
        self.assertEqual(test10.score(), (20, 1))

    def test_score_with_soft_aces(self):
        test11 = blackjack3.Hand([1])
        self.assertEqual((11, 1), test11.score())
        #
        test12 = blackjack3.Hand([1, 10])
        self.assertEqual((21, 1), test12.score())

        test13 = blackjack3.Hand([1, 2, 3, 10, 1])
        self.assertEqual((17, 0), test13.score())

    def test_stand_on_soft_rubric(self):
        hand_test_1 = blackjack3.Hand([5, 8])
        hand_test_2 = blackjack3.Hand([5, 7, 3])
        hand_test_3 = blackjack3.Hand([5, 7, 2, 2])
        hand_test_4 = blackjack3.Hand([5, 5, 5, 1])
        hand_test_5 = blackjack3.Hand([5, 5, 5, 1])
        hand_test_6 = blackjack3.Hand([5, 1])
        hand_test_7 = blackjack3.Hand([3, 3, 1])
        hand_test_8 = blackjack3.Hand([5, 5, 3, 4])

        stand_test_true = blackjack3.Strategy(16, True)
        stand_test_false = blackjack3.Strategy(16, False)

        #         # below stand on value, never stand
        self.assertFalse(stand_test_true.stand(hand_test_1))
        self.assertFalse(stand_test_true.stand(hand_test_2))

        #         # at stand on value, and the hand is hard, should stand either way
        self.assertTrue(stand_test_true.stand(hand_test_3))
        #         # at stand on value, and the hand is hard (but contains an ace), should stand either way
        self.assertTrue(stand_test_true.stand(hand_test_4))
        self.assertTrue(stand_test_false.stand(hand_test_5))
        #         # at stand on value, and the hand is soft
        self.assertTrue(stand_test_false.stand(hand_test_6))

        #
        #         # above stand on value, always stand
        self.assertTrue(stand_test_true.stand(hand_test_7))
        #
        self.assertTrue(stand_test_true.stand(hand_test_8))


#
#
#
if __name__ == '__main__':
    unittest.main()
