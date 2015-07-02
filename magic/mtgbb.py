import requests
import re

from models import read_cards_file, get_card_list


def main():
    cards = read_cards_file()
    get_card_list(cards, fill_card_prices)

    print
    print "RESULTS - magic bem barato"
    print

    total = 0.0

    for card in cards:
        if card.lowest_price == 0.0:
            print "%s - NOT AVAILABLE" % card
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
