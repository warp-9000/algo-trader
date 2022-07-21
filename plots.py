import plotly.graph_objects as go
from plotly.subplots import make_subplots



def generate_graph(stock_plot_df, trade_plot_df, broke_plot_df):
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
			# y=stock_plot_df.RollingHigh, 
			# name="4 Week High",
			y=stock_plot_df.FastSMA, 
			name="Fast SMA",
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
			# y=stock_plot_df.RollingLow,
			# name="4 Week Low",
			y=stock_plot_df.SlowSMA,
			name="Slow SMA",
			hoverinfo='text+name',
			line_shape='linear',
			line=dict(color='rgba(204,204,204,0.95)'),
			# hovertemplate='<extra></extra>',
		),
		row=3, col=1,
		# secondary_y=True,
	)

	# # plot the Close
	fig.add_trace(
		go.Scatter(
			x=stock_plot_df.Date, 
			y=stock_plot_df.Close, 
			name="SPY",
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
		yaxis = dict(range=[0,1000000000]),
		# yaxis2 = dict(range=[0,500]),
		# hovermode='x',
	)
	fig.update(
		# layout_xaxis_rangeslider_visible=False,
	)

	fig.show()

	return None

(
# fig = go.Figure(go.Scatter(
# 	mode="markers", 
# 	x=namevariants, 
# 	y=namestems, 
# 	marker_symbol=symbols,                       
# 	marker_line_color="midnightblue", 
# 	marker_color="lightskyblue",
#     marker_line_width=2,
# 	marker_size=15,
# #    hovertemplate="name: %{y}%{x}<br>number: %{marker.symbol}<extra></extra>"
# ))

# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# fig.update_traces(marker=dict(size=12,
#                               line=dict(width=2,
#                                         color='DarkSlateGrey')),
#                   selector=dict(mode='markers'))

# fig.add_trace(go.Scatter(x=x, y=y + 10, name="vhv",
#                     line_shape='vhv'))
# fig.add_trace(go.Scatter(x=x, y=y + 15, name="hvh",
#                     line_shape='hvh'))
# fig.add_trace(go.Scatter(x=x, y=y + 20, name="vh",
#                     line_shape='vh'))
# fig.add_trace(go.Scatter(x=x, y=y + 25, name="hv",
#                     line_shape='hv'))

# fig.update_traces(
# 	yaxis title,
# 	xaxis title,
# 	hoverinfo='text+name',
# 	mode='lines+markers'
# )

# fig.update_layout(
# 	legend=dict(
# 		y=0.5, traceorder='reversed', font_size=16
# 	)
# )
)
