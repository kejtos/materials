ORANGE = '#E69F00'
TEAL = '#56B4E9'
GREEN = '#009E73'
YELLOW = '#F0E442'
BLUE = '#0072B2'
RED = '#D55E00'
PINK = '#CC79A7'

def beauty_altair(chart):
  final_chart = (
    chart
    .configure_title(fontSize=16, anchor='middle')
    .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
    .configure_legend(titleFontSize=12, labelFontSize=10)
  )
  return final_chart