import poker
import unittest

class TestCard(unittest.TestCase):
    def testFromStr(self):
        c = poker.Card.from_str("Ad")
        self.assertEqual(c.str_value, "A")
        self.assertEqual(c.suit, poker.DIAMONDS)


class TestHand(unittest.TestCase):
    def testFromStr(self):
        h = poker.Hand.from_str("AdAsAh10c")
        self.assertEqual(4, len(h.cards))
        self.assertEqual(h.cards[-1].str_value, "10")
        self.assertEqual(h.cards[0].str_value, "A")
        
    def testSort(self):
        h = poker.Hand.from_str("10c4c8c2cAc7c")
        self.assertEquals(poker.card_value("A"), h.cards[0].value)
        self.assertEquals(poker.card_value("10"), h.cards[1].value)
        self.assertEquals(poker.card_value("8"), h.cards[2].value)
        self.assertEquals(poker.card_value("7"), h.cards[3].value)
        self.assertEquals(poker.card_value("4"), h.cards[4].value)
        self.assertEquals(poker.card_value("2"), h.cards[5].value)

    def testIsSuited(self):
        self.assertTrue(poker.is_suited(poker.Hand.from_str("Ad").cards))
        self.assertTrue(poker.is_suited(poker.Hand.from_str("Ad2d").cards))
        self.assertTrue(poker.is_suited(poker.Hand.from_str("Ad2d3d").cards))
        self.assertFalse(poker.is_suited(poker.Hand.from_str("Ad2c").cards))
        self.assertFalse(poker.is_suited(poker.Hand.from_str("Ad2c3s").cards))
    

    def testIsSequential(self):
        self.assertTrue(poker.is_sequential(poker.Hand.from_str("10dJdQdKdAd").cards))
        self.assertFalse(poker.is_sequential(poker.Hand.from_str("JdQdKdAd2d").cards))
        self.assertFalse(poker.is_sequential(poker.Hand.from_str("10dJdQdKdAd2d").cards))
        self.assertTrue(poker.is_sequential(poker.Hand.from_str("Ad2d3d4d5d").cards))
        
    def testHands(self):
        self.assertEquals(poker.hand_value("Straight flush"), poker.Hand.from_str("AcKcQcJc10c").value[0])
        self.assertEquals(poker.hand_value("Four of a kind"), poker.Hand.from_str("AcAdAhAs6d").value[0])
        self.assertEquals(poker.hand_value("Full house"), poker.Hand.from_str("AcAdAc6s6d").value[0])
        self.assertEquals(poker.hand_value("Full house"), poker.Hand.from_str("6c6d6cAsAd").value[0])
        self.assertEquals(poker.hand_value("Flush"), poker.Hand.from_str("AcKcQcJc9c").value[0])
        self.assertEquals(poker.hand_value("Straight"), poker.Hand.from_str("AcKcQdJc10c").value[0])
        self.assertEquals(poker.hand_value("Three of a kind"), poker.Hand.from_str("AcAdAs7d6d").value[0])
        self.assertEquals(poker.hand_value("Two pair"), poker.Hand.from_str("AcAd8c8d6d").value[0])
        self.assertEquals(poker.hand_value("One pair"), poker.Hand.from_str("AcAd8d7d6d").value[0])
        self.assertEquals(poker.hand_value("High card"), poker.Hand.from_str("AcJd8d7d6d").value[0])
    
    def testHandValue(self):
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcKcQcJc10c").value[1][0]) # straight flush
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcAdAhAs6d").value[1][0]) # four of a kind
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcAdAc6s6d").value[1][0]) # full house
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("6s6dAcAdAc").value[1][0]) # full house
        self.assertEquals(poker.card_value("6"), poker.Hand.from_str("6s6d6cAcAd").value[1][0]) # full house
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcKcQcJc9c").value[1][0]) # flush
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcAdAs7d6d").value[1][0]) # 3 of a kind
        self.assertEquals(poker.card_value("7"), poker.Hand.from_str("Ac7d7s7d6d").value[1][0]) # 3 of a kind
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcAd8c8d6d").value[1][0]) # two pair
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("8c8dAcAd6d").value[1][0]) # two pair
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcAd8d7d6d").value[1][0]) # 1 pair
        self.assertEquals(poker.card_value("A"), poker.Hand.from_str("AcJd8d7d6d").value[1][0]) # high card
    
    def testKicker(self):
        self.assertEquals([], poker.Hand.from_str("AcKcQcJc10c").value[1][1:]) # straight flush
        self.assertEquals([poker.card_value("6")], poker.Hand.from_str("AcAdAhAs6d").value[1][1:]) # four of a kind
        self.assertEquals([poker.card_value("6")], poker.Hand.from_str("AcAdAc6s6d").value[1][1:]) # full house
        self.assertEquals([poker.card_value("6")], poker.Hand.from_str("6s6dAcAdAc").value[1][1:]) # full house
        self.assertEquals([poker.card_value("A")], poker.Hand.from_str("6s6d6cAcAd").value[1][1:]) # full house
        self.assertEquals([poker.card_value(c) for c in "KQJ9"], poker.Hand.from_str("AcKcQcJc9c").value[1][1:]) # flush
        self.assertEquals([poker.card_value(c) for c in "76"], poker.Hand.from_str("AcAdAs7d6d").value[1][1:]) # 3 of a kind
        self.assertEquals([poker.card_value(c) for c in "A6"], poker.Hand.from_str("Ac7d7s7d6d").value[1][1:]) # 3 of a kind
        self.assertEquals([poker.card_value(c) for c in "86"], poker.Hand.from_str("AcAd8c8d6d").value[1][1:]) # two pair
        self.assertEquals([poker.card_value(c) for c in "6A"], poker.Hand.from_str("Ac8d8c6c6d").value[1][1:]) # two pair
        self.assertEquals([poker.card_value(c) for c in "86"], poker.Hand.from_str("8c8dAcAd6d").value[1][1:]) # two pair
        self.assertEquals([poker.card_value(c) for c in "876"], poker.Hand.from_str("AcAd8d7d6d").value[1][1:]) # 1 pair
        self.assertEquals([poker.card_value(c) for c in "J876"], poker.Hand.from_str("AcJd8d7d6d").value[1][1:]) # high card

    def testEdgeCase(self):
        self.assertTrue(poker.Hand.from_str("AcKcQcJc10c") > poker.Hand.from_str("Ac5c4c3c2c")) # high card
        self.assertFalse(poker.Hand.from_str("AcKcQcJc10c") < poker.Hand.from_str("Ac5c4c3c2c")) # high card
        self.assertFalse(poker.Hand.from_str("AcKcQcJc10c") == poker.Hand.from_str("Ac5c4c3c2c")) # high card
        
    def testEquality(self):
        self.assertTrue(poker.Hand.from_str("AcKcQcJc10c").value == poker.Hand.from_str("AdKdQdJd10d").value) # straight flush
        
        
        
class PlayerTest(unittest.TestCase):
    def testHighestHand(self):
        hands = (
            ("AcAd7c5c4c", "Ah", "Ac", "Four of a kind"),
            ("AcAd7c5c4c", "7d", "7h", "Full house"),
            ("AcAd7c5c4c", "8h", "6d", "Straight"),
            ("AcAd7c5c4c", "8c", "6c", "Straight flush"),
            ("AcAd7c5c4c", "8c", "6c", "Straight flush"),
            ("AcAd7c5c4c", "10h", "10d", "Two pair"),
            ("AcAd7c5c4c", "10c", "10d", "Flush"),
        )
        for hand in hands:
            board = poker.Hand.from_str(hand[0]).cards
            player = poker.Player()
            player.deal(poker.Card.from_str(hand[1]))
            player.deal(poker.Card.from_str(hand[2]))
            self.assertEquals(poker.hand_value(hand[3]), player.hand(board).value[0])

        
        
        
if __name__ == '__main__':
    unittest.main()
