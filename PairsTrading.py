import numpy as np

def initialize(context):
    
    schedule_function(check_pairs,date_rules.every_day(),time_rules.market_close(minutes=60))
    context.ua=sid(28051)
    context.aa=sid(45971)
    
    context.long_spread=False
    context.short_spread=False
    
def check_pairs(context,data):
    ua=context.ua
    aa=context.aa
    prices = data.history([ua,aa],'price',30,'1d')
    daily_prices = prices.iloc[-1:]
    ma30 = np.mean(prices[ua]-prices[aa])
    std30 = np.std(prices[ua]-prices[aa])
    ma1 = np.mean (daily_prices[ua]-daily_prices[aa])
    if std30 > 0:
        zscore = (ma1 - ma30)/std30
        if zscore > 2 and not context.short_spread:
            order_target_percent(ua,-0.5)
            order_target_percent(aa,0.5)
            context.short_spread = True 
            context.long_spread = False 
        elif zscore < -2 and not context.long_spread:
            order_target_percent(ua,0.5)
            order_target_percent(aa,-0.5)
            context.short_spread = False 
            context.long_spread = True    
        elif abs(zscore) < 0.1:
            order_target_percent(ua,0)
            order_target_percent(aa,0)
            context.short_spread = False 
            context.long_spread = False
        else:
            pass
        record(z_score = zscore)
