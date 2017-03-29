import numpy as np
import pandas as pd

def init(context):
	context.firstrun = True
	return 

def before_trading(context):
	if context.firstrun == True:
		context.firstrun = False
		context.current_month = context.now.month
		ourquery = fundamentals.eod_derivative_indicator.market_cap
		nowdate = context.now.date()
		
		pd = get_fundamentals(query(ourquery).entry_date=nowdate)
		context.stocks = list(pd['market_cap'].columns)

		## clean stocks list 
		context.stocks.remove("000787.XSHE")
		to_be_removed = []
		for stk in context.stocks:
			if stk[10]=='G':
				to_be_removed.append(stk)
		for stk in to_be_removed:
			context.stocks.remove(stk)

		context.stocks.append("600000.XSHG")

		context.current_price = pd.Series(index=context.stocks)
		context.last_price = pd.Series(index=context.stocks)
		context.mktcap = pd.Series(index=context.stocks)
		context.bps = pd.Series(index=context.stocks)

	if context.current_price != context.now.month:
		context.current_price = pd.Series(index=context.stocks)
		context.last_price = pd.Series(index=context.stocks)
		context.mktcap = pd.Series(index=context.stocks)
		context.bps = pd.Series(index=context.stocks)

		for stk in context.stocks:
			context.current_price[stk] = get_price(stk,start_date=nowdate)
			dp = get_fundamentals(query(fundamentals.eod_derivative_indicator.market_cap,fundamentals.\
				financial_indicator.book_value_per_share).filter(fundamentals.stockcode==stk,entry_date=nowdate))
			context.mktcap[stk] = dp['fundamentals.eod_derivative_indicator.market_cap'].loc[nowdate]
			context.bps[stk] = dp['fundamentals.financial_indicator.book_value_per_share'].loc[nowdate]
		context.current_mkt_price = get_price('000300.XSHG',nowdate)
		context.last_mkt_price = get_price('000300.XSHG',nowdate-1)

def handle_bar(context, bar_dict):
	if context.current_month==context.now.month:
		return 
	else:
		context.current_month = context.now.month
		where_is_nan = np.isnan(context.bps)
		context.bps[where_is_nan] = 0.
		where_is_nan = np.isnan(context.mktcap)
		context.mktcap[where_is_nan] = 0.

		for stk in context.stocks:
			if context.current_price[stk]==np.nan:
				context.current_price[stk] = 0.
			if context.last_price[stk]==np.nan:
				context.last_price[stk]==0.

		btm = pd.Series(index=context.stocks)
		for stk in context.stocks:
			if context.current_price[stk]!=0:
				btm[stk] = context.bps[stk] /context.current_price[stk]
			else:
				btm[stk] = 0.

		market_cap_median = np.median(context.market_cap)
		low_bps = np.percentile(list(btm),30)
		high_bps = np.percentile(list(btm),70)

		for stk in context.stocks:
			if(context.current_price[stk]==0):
				return_rate[stk] = 0
			else:
				return_rate[stk] = context.current_price[stk]/context.last_price[stk]

		large_market_cap_sum=0
		small_market_cap_sum=0
		high_bps_sum=0
		low_bps_sum=0


		for stk in context.stocks:
			if context.market_cap[stk]>market_cap_median:
				large_market_cap_sum+=context.market_cap[stk]*return_rate[stk]
			else:
				small_market_cap_sum+=context.market_cap[stk]*return_rate[stk]
			if btm[stk]>high_bps:
				high_bps_sum+=context.market_cap[stk]*return_rate[stk]
			else:
				low_bps_sum+=context.market_cap[stk]*return_rate[stk]
		mktcap_total = np.sum(context.market_cap)
		SMB = (small_market_cap_sum - large_market_cap_sum)/mktcap_total
		HMI = (high_bps_sum - low_bps_sum)/mktcap_total
		RM = context.current_mkt_price/context.last_mkt_price - 1 - 0.00375
		ref = RM + SMB + HMI  + 1.0
		ref_price = ref*context.last_price['600000.XSHG']
		today_price = context.current_price['600000.XSHG']

		if (today_price>ref_price*1.05):
			order_target_percent('600000.XSHG',0)
		if (today_price<ref_price*0.95):
			order_target_percent('600000.XSHG',1)

		








