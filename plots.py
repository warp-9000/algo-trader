import plotly.graph_objects as go
from plotly.subplots import make_subplots

import os
from _config import *
from strategies import *


def plot_graph(stock_plot_df, trade_plot_df, broke_plot_df, 
	stock, strategy, indicator_1_name, indicator_2_name, save_results_choice=False):
	'''TODO: describe this function


	'''

	# ----------------------------------------------------------------------------------------------
	'''
		TODO: plot the graphs
		TODO: combine the graphs into a single graph

		NOTE: adding <extra></extra> to the end of the hovertemplate will remove the NAME of the line / plotted thing!
	'''

	fig = go.Figure()

	fig = make_subplots(
		rows=3, cols=1,
		shared_xaxes=True,
		vertical_spacing=0.005,
		specs=[
			[{"type": "xy"}],
			[{"type": "xy"}],
			# [{"type": "xy"}],
			[{"type": "xy","secondary_y": True}]
		]
	)




	# ----------------------------------------------------------------------------------------------
	# plot the stock data over time

	# plot the first indicator (High/Fast)
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date, 
			y=stock_plot_df.Indicator_1, 
			name=indicator_1_name,
			hoverinfo='text+name',
			line_shape='linear',
			line=dict(color='rgba(204,204,204,0.95)'),
			# hovertemplate='<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)

	# plot the second indicator (Low/Slow)
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date,
			y=stock_plot_df.Indicator_2,
			name=indicator_2_name,
			hoverinfo='text+name',
			line_shape='linear',
			line=dict(color='rgba(204,204,204,0.95)'),
			# hovertemplate='<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)



	# ----------------------------------------------------------------------------------------------
	# # plot the Close
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date, 
			y=stock_plot_df.Close, 
			name=stock,
			hoverinfo='text+name',
			line_shape='linear',
			line=dict(color="#4F4F4F"),
			hovertemplate='<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)

	# plot the Buy signals
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date,
			y=stock_plot_df.BuySignal,
			name="Buy",
			hoverinfo='text+name',
			mode='markers',
			marker_symbol='triangle-up',
			marker_size=12,
			marker_color="green",
			hovertemplate='Buy<br>Price: $%{y:.2f}'+'<br>Date: %{x}<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)

	# plot the Sell signals
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date,
			y=stock_plot_df.SellSignal,
			name="Sell",
			hoverinfo='text+name',
			mode='markers',
			marker_symbol='triangle-down',
			marker_size=12,
			marker_color="red",
			hovertemplate='Sell<br>Price: $%{y:.2f}'+'<br>Date: %{x}<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)



	# plot candlesticks using open-high-low-close
	# fig.add_trace(
	# 	go.Candlestick(
	# 		x=stock_plot_df.Date,
	# 		open=stock_plot_df.Open,
	# 		high=stock_plot_df.High,
	# 		low=stock_plot_df.Low,
	# 		close=stock_plot_df.Close,
	# 		name="SPY",
	# 		# yaxis='y1',
	# 	),
	# 	row=3, col=1,
	# 	# secondary_y=True
	# )

	# fig.add_trace(
	# 	go.Bar(
	# 		x=stock_plot_df.Date,
	# 		y=stock_plot_df.Volume,
	# 		name='Volume',
	# 		yaxis='y2',
	# 		marker={'color': 'rgba(128,128,128,0.85)'},
	# 	),
	# 	# row=3, col=1,
	# 	secondary_y=False,
	# )	



	# ----------------------------------------------------------------------------------------------
	# plot the trading profit over time

	# plot the positive trades
	fig.add_trace(
		go.Scatter(
			x=trade_plot_df.Date, 
			y=trade_plot_df.Positive, 
			name="Positive",
			# hoverinfo='text+name',
			# line_shape='linear',
			mode='markers',
			marker_symbol='circle',
			marker_size=12,
			marker_color="blue",
			hovertemplate='Realized Gain: $%{y:.2f}'+'<br>Date: %{x}<extra></extra>'
		),
		row=2,col=1
	)

	# plot the negative trades
	fig.add_trace(
		go.Scatter(
			x=trade_plot_df.Date, 
			y=trade_plot_df.Negative, 
			name="Negative",
			# hoverinfo='text+name',
			# line_shape='linear',
			mode='markers',
			marker_symbol='circle',
			marker_size=12,
			marker_color="red",
			hovertemplate='Realized Loss: $%{y:.2f}'+'<br>Date: %{x}<extra></extra>'
		),
		row=2,col=1
	)



	# ----------------------------------------------------------------------------------------------
	# plot the brokerage values over time

	# plot the positive trades
	fig.add_trace(
		go.Scatter(
			x=broke_plot_df.Date, 
			y=broke_plot_df.TotalCash, 
			name="Total Cash",
			# hoverinfo='text+name',
			line_shape='linear',
			# mode='markers',
			# marker_symbol='circle',
			# marker_size=12,
			# marker_color="blue",
			hovertemplate='Cash: $%{y:.2f}'+'<extra></extra>',
			line=dict(color="red"),
		),
		row=1,col=1
	)

	# plot the negative trades
	fig.add_trace(
		go.Scatter(
			x=broke_plot_df.Date, 
			y=broke_plot_df.TotalValue, 
			name="Total Value",
			# hoverinfo='text+name',
			line_shape='linear',
			# mode='markers',
			# marker_symbol='circle',
			# marker_size=12,
			# marker_color="red",
			hovertemplate='Value: $%{y:.2f}'+'<extra></extra>',
			line=dict(color="blue"),
		),
		row=1,col=1
	)

	fig.update_xaxes(rangeslider=dict(visible=False))
	fig.update_yaxes(autorange=True)
	fig.update_layout(
		title=stock+" - "+strategy,
		width=PLOT_WIDTH, 
		height=PLOT_HEIGHT,
		yaxis = dict(range=[0,1000000000]),
		# yaxis2 = dict(range=[0,500]),
		# hovermode='x',
	)
	fig.update(
		# layout_xaxis_rangeslider_visible=False,
	)

	fig.show()

	# save the results as a PNG if wanted
	if save_results_choice:
		if not os.path.exists('images'):
			os.mkdir('images')
		
		fig.write_image('images/'+stock+'_'+STRATEGIES[strategy]['name']+'_strat.png')

	return None
