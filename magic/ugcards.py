import requests
import lxml.html

from models import read_cards_file, get_card_list


def main():
    cards = read_cards_file()
    get_card_list(cards, fill_card_prices)

    print
    print "RESULTS - ugcardshop"
    print

    total = 0.0

    unavailable = []

    for card in cards:
        if card.lowest_price == 0.0:
            unavailable.append(card)
            continue

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

    print

    print "UNAVAILABLE CARDS:"
    for card in unavailable:
        print "%s - NOT AVAILABLE" % card


def fill_card_prices(card):
    url = "http://www.ugcardshop.com.br/?action=cardSearch&search%%5Bname%%5D=%s&search%%5Bexact%%5D=0&search%%5Bedition%%5D=&search%%5Border%%5D=nome&search%%5Bway%%5D=ASC&pg=0" % card.name  # NOQA
    req = requests.get(url)
    root = lxml.html.fromstring(req.text)
    cards = root.cssselect('div.card-content > table > tr')

    for card_row in cards:
        rows = card_row.cssselect('tr')

        name = card_row.cssselect('tr')[0].getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].text  # NOQA
        names = [name_part.lower().strip(' ') for name_part in name.split('/')]
        if card.name.lower() not in names:
            continue

        cells = rows[5].cssselect('td')
        price_text = cells[1].cssselect('p')[0].text
        price = float(price_text.split('(')[0].replace('R$', '').replace('\t', '').replace(u'\xa0', '').strip(' ').replace(',', '.'))  # NOQA

        qty = int(rows[7].cssselect('td p')[1].text.split('(')[0].replace('R$', ''))
        if qty > 0:
            card.prices.append(price)


if __name__ == "__main__":
    main()
