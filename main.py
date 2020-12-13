import webbrowser
import sys
import pyperclip

if len(sys.argv) > 1:
    address = ' '.join(sys.argv[1:])

else:
    address = pyperclip.paste()
print(address)

webbrowser.open("https://www.google.bg/maps/place/" + address)
