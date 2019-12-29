from PIL import Image
import csv

image = Image.open("screen-1.png")

colors_info = image.getcolors()
print(colors_info)

width, height = image.size
data = image.load()
print(width, height)

column = 0

with open('candle.csv', 'a+') as candle:
    writer = csv.writer(candle)
    writer.writerow(['trend', 'prev_candle', 'next_candle'])

# Analizujemy kolumny, pixel za pixelem (w pionie) w celu sprawdzenia
# jaki kolor pojawia się w danej kolumnie.
# W danej kolumnie może występowac moze tylko jeden kolor świecy
# (poza kolorem czarnym - kolor tła). Jeśli w kolumnie występuje
# tylko kolor czarny, będziemy taką kolumnę ignorować.

for x in range(width):
    for y in range(height):
        with open('output.txt', 'a+') as result:

            color = data[x, y]
            prev_color = data[x, y-1]
            prev_candle = data[x-2, y]
            column += 1

            if color == (60, 176, 250, 255) and prev_color != color or color == (255, 255, 255, 255) and prev_color != color:
                print(prev_candle, color, file=result)

                with open('candle.csv', 'a+') as candle:
                    writer = csv.writer(candle)
                    candle_writer = csv.writer(candle, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    # Kolejność w pliku CSV - (trend, poprzednia swieca, następna świeca - aktualna)
                    # Znaczenie prev_candle: 0 (zero) - bear, 1 (jeden) - bull
                    # Znaczenie trend: 0 (zero) - brak trendu, 1 (jeden) - trend
                    if color == (60, 176, 250, 255) and prev_candle == (60, 176, 250, 255):
                        candle_writer.writerow(['1', '1', 'bull'])
                    elif color == (60, 176, 250, 255) and prev_candle == (255, 255, 255, 255):
                        candle_writer.writerow(['0', '1', 'bear'])
                    elif color == (255, 255, 255, 255) and prev_candle == (60, 176, 250, 255):
                        candle_writer.writerow(['1', '0', 'bull'])
                    elif color == (255, 255, 255, 255) and prev_candle == (255, 255, 255, 255):
                        candle_writer.writerow(['0', '0', 'bear'])
                    else:
                        pass

                candle.close()
        result.close()
