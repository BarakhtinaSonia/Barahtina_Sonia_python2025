def format(n):
    print( '{:*^30}'.format('{:,.3f}'.format(n).replace(',', ' ')))

format(10000056.123943243)