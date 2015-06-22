import requests
import re


class Card:
    def __init__(self, quantity, name):
        self.quantity = quantity
        self.name = name
        self.prices = []

    @property
    def lowest_price(self):
        return min(self.prices)

    def __str__(self):
        return "%d %s (lowest: %.2f)" % (self.quantity, self.name, self.lowest_price)

    def __repr__(self):
        return str(self)


def main():
    cards = read_cards_file()
    get_card_list(cards)

    print
    print "RESULTS"
    print

    total = 0.0

    for card in cards:
        total_for_card = card.quantity * card.lowest_price
        total += total_for_card

        print "%d %s (Each R$ %.2f, Total %.2f)" % (
            card.quantity,
            card.name,
            card.lowest_price,
            total_for_card
        )

    print
    print "Cheapest card: %s" % min(cards, key=lambda card: card.lowest_price)
    print "Most Expensive card: %s" % max(cards, key=lambda card: card.lowest_price)
    print
    print
    print "Total for decklist: R$ %.2f" % total


def read_cards_file():
    with open('cards.txt', 'r') as cards:
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


def get_card_list(cards):
    for card in cards:
        print "Getting prices for %s..." % card.name
        fill_card_prices(card)


def fill_card_prices(card):
    # curl 'http://www.magicbembarato.com.br/buscar.php'
    # -H 'Cookie: PHPSESSID=66a78cgmqr6dk7ou5r35cei9r1; _gat=1; _ga=GA1.3.294652854.1434980319'
    # -H 'Origin: http://www.magicbembarato.com.br'
    # -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4'
    # -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/43.0.2357.124 Safari/537.36'
    # -H 'Content-Type: application/x-www-form-urlencoded'
    # -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    # -H 'Cache-Control: max-age=0'
    # -H 'Referer: http://www.magicbembarato.com.br/buscar.php'
    # -H 'Connection: keep-alive'
    # --data 'nomec=Lan%C3%A7a+Veloz+do+Monast%C3%A9rio' --compressed
    headers = {
        'Origin': 'http://www.magicbembarato.com.br',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': 'http://www.magicbembarato.com.br/buscar.php',
        'Connection': 'keep-alive',
    }

    payload = {
        'nomec': card.name
    }
    req = requests.post("http://www.magicbembarato.com.br/buscar.php", data=payload, headers=headers)
    text = req.text
    result = re.findall(r'[<]b[>]R\$\s*\d+[.]\d+\s*[<][/]b[>]', text)

    for price_txt in result:
        price = float(price_txt.replace('<b>', '').replace('</b>', '').replace('R$', '').strip(' '))
        card.prices.append(price)


if __name__ == "__main__":
    main()
