def initialize(context):
    context.jpm = sid(25006)
    schedule_function(check_bands,date_rules.every_day())

def check_bands(context,data):
    current_price = data.current(context.jpm, 'price')
    prices = data.history(context.jpm,'price',30,'1d')
    avg = prices.mean()
    std = prices.std()
    lower_band = avg - 2*std
    upper_band = avg + 2*std
    
    if current_price <=lower_band:
        order_target_percent(context.jpm,1)
        print('Buying')
        print(('Current price is: ' + str(current_price)))
        print(('Lower band is: ' + str(lower_band)))
    elif current_price >= upper_band:
        order_target_percent(context.jpm,-1)
        print('Shorting')
        print(('Current price is: ' + str(current_price)))
        print(('Upper band is: ' +str(upper_band)))
    else:
        pass    
    
    record(upper = upper_band, lower = lower_band,
           mvag_30 = avg, price = current_price)
