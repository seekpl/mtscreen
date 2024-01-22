from PIL import Image
import csv


def candle_type(iterate):
    iterator = iter(iterate)
    prev_item = 0
    current_item = next(iterator)
    for next_item in iterator:
        yield (prev_item, current_item, next_item)
        prev_item = current_item
        current_item = next_item
    yield (prev_item, current_item, 0)


image = Image.open("screen-examples/screen-example-1.png")

width, height = image.size
data = image.load()
print(f'Image size: {width} x {height}')

colors_info = sorted(image.getcolors())
# Kolor tła określany na podstawie ilosci wystepowawnia danego koloru.
# Kolor tla ma z zalozenia najwyzsza liczbe.
bg = colors_info[-1]
bg_color = bg[-1]

color1 = colors_info[-2]
candle_color1 = color1[-1]

color2 = colors_info[-3]
candle_color2 = color2[-1]

column = 0
candle_bull = 0
candle_bear = 0

bear_count = []
bull_count = []

trend_all = []
trend_high = []
trend_low = []

trend_bear = []
trend_bull = []
trend = []

with open('candle.csv', 'a+') as candle:
    writer = csv.writer(candle)
    writer.writerow(['trend', 'prev_candle', 'next_candle'])

# Analizujemy kolumny, pixel by pixel (w pionie) w celu sprawdzenia
# jaki kolor pojawia się w danej kolumnie.
# W danej kolumnie może występowac moze tylko jeden kolor świecy
# (poza kolorem czarnym - kolor tła). Jeśli w kolumnie występuje
# tylko kolor czarny, będziemy taką kolumnę ignorować.
try:
    for x in range(width):
        for y in range(height):
            # W tym pliku kontrolujemy sprawdzane kolory i ich kolejnosci porownując output.txt z przeslanym screenem.
            # prev_color sprawdza kolor poprzedniego piksela w osi Y
            current_candle = data[x, y]
            prev_candle = data[x - 2, y]
            next_candle = data[x + 2, y]
            prev_color = data[x, y - 1]

            column += 1

            # Wskazywanie punktu high i low swiecy w celu okreslenia trendu.
            # Do listy trend_all dodawane sa po kolei wspolrzedne x, y aby mozna bylo porownac tablice.
            if current_candle != bg_color and current_candle != prev_color:
                trend_high.append((x, y))
                trend_all.append(x)
                trend_all.append(y)
            elif current_candle == bg_color and prev_color != bg_color:
                trend_low.append((x, y - 1))
            else:
                pass

except IndexError:
    print(f'Reached end of file {image}')

# Okreslenie trendu na podstawie wysokosci punktow high danej swiecy.
# Wyszukuje Y z tablicy w celu okreslenia wysokosci gornego punktu swiecy.
for prev, item, next in candle_type(trend_all[1::2]):
    if prev >= item != 0:
        trend_bull.append((trend_all.index(prev), item))
        trend.append(0)

        color_x_bull = trend_all.index(prev)
        color_y_bull = item

        bull = data[color_x_bull, color_y_bull]
        bull_count.append(bull)
        color_number1 = bull_count.count(candle_color1)
        color_number2 = bull_count.count(candle_color2)

        if color_number1 > color_number2:
            candle_bull = candle_color1
        else:
            candle_bull = candle_color2

    elif prev != 0 <= item:
        trend_bear.append((trend_all.index(prev), item))
        trend.append(1)

        color_x_bear = trend_all.index(prev)
        color_y_bear = item

        bear = data[color_x_bear, color_y_bear]
        bear_count.append(bear)
        color_number3 = bear_count.count(candle_color1)
        color_number4 = bear_count.count(candle_color2)

        if color_number3 > color_number4:
            candle_bear = candle_color1
        else:
            candle_bear = candle_color2
    else:
        pass

print(f'bull {bull_count}')
print(f'bear {bear_count}')


print(f'Background: {bg_color}')
print(f'Bull candle color: {candle_bull}')
print(f'Bear candle color: {candle_bear}')
print(f'All colors: {colors_info}')

print(f'TREND All: {trend_all}')
print(f'CANDLE BULL: {trend_bull}')
print(f'CANDLE BEAR: {trend_bear}')

with open('candle-position.txt', 'a+') as candle_pos:
    print(f'H: {trend_high}', file=candle_pos)
    print(f'L: {trend_low}', file=candle_pos)
    print(f'T:{trend}', file=candle_pos)
    print(f'CANDLE BEAR: {trend_bear}', file=candle_pos)
    print(f'CANDLE BULL: {trend_bull}', file=candle_pos)
