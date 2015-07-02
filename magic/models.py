class Card:
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name.lstrip(' ').rstrip(' ').lstrip('\n').rstrip('\n')
        self.prices = []

    @property
    def lowest_price(self):
        if not self.prices:
            return 0.0

        return min(self.prices)

    def __str__(self):
        return "%d %s (lowest: %.2f)" % (self.quantity, self.name, self.lowest_price)

    def __repr__(self):
        return str(self)


def read_cards_file():
    with open('./magic/cards.txt', 'r') as cards:
        text = cards.readlines()

    cards = []
    for line in text:
        if line.strip(' ') == '':
            continue
        if line[0] not in ['1', '2', '3', '4']:
            continue

        parts = [card.strip(' ') for card in line.split('\t') if card.strip(' ') != '']
        cards.append(Card(quantity=int(parts[0]), name=parts[1]))

    return cards


def get_card_list(cards, fill_card_prices):
    for card in cards:
        print "Getting prices for %s..." % card.name
        fill_card_prices(card)


