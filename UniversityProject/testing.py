import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import plotly.graph_objects as go

def al():
    while True:

        try:
            a = float(input('Podaj 1 liczbę: '))
            b = float(input('Podaj 2 liczbę: '))
            break;
        except:
            print('Podaj poprawne liczby!!!')
            al()




    doz = ['podziel', 'pomnoz', 'dodaj', 'odejmij', ]
    print('Dozwolone: ' + str(doz))
    c = input('Wybierz jedna opcje z dozwolonych: ')
    if c in doz:
        if c == 'podziel':
            p = float(a)/float(b)
            print ('Wynik jest rowny: ' + str(round(p, 2)))
        elif c == 'pomnoz':
            po = float(a)*float(b)
            print ('Wynik jest rowny: ' + str(round(po, 2)))
        elif c == 'dodaj':
            dod = float(a)+float(b)
            print('Wynik jest rowny: ' + str(dod))
        elif c == 'odejmij':
            od = float(a)-float(b)
            print('Wynik jest rowny: ' + str(od))
    else:
        print('Podaj poprawna opcje!')
        al()
gas = input('Pi: ')
if gas == '1':
    al()
