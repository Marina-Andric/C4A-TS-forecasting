import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dates_1 = ['2017/06','2017/07','2017/08','2017/09','2017/10', '2017/11', '2017/12', '2018/01', '2018/02', '2018/03', '2018/04', '2018/05', '2018/06']
me_1 = [-0.166970, -0.022727, -0.229574, -0.083725, 0.007670,  0.072039,0.039394,-0.006768,-0.116633,-0.018598,-0.059495,-0.071546,-0.001782]
mea_1 = [0.446364, 0.397475, 0.455106, 0.313333, 0.363981, 0.306019,0.285051,0.329596,0.326020,0.265327,0.287374,0.275464,0.307129]
mape_1 = [15.596935,    13.079493,    17.291122, 12.201216, 11.850450, 9.333789,8.863201,10.892313,12.116353,8.749178,9.647717,9.599589,10.173860]

dates_3 = ['2017/08','2017/09','2017/10','2017/11','2017/12','2018/01', '2018/02', '2018/03', '2018/04', '2018/05', '2018/06']
me_3 = [-0.233830, -0.126569, -0.033883, 0.030485, 0.008586, -0.037576,-0.142449,-0.046822,-0.084949,-0.102371,-0.035347]
mea_3 = [0.461915, 0.326961, 0.374854, 0.308350, 0.310202, 0.342424,0.348571,0.281402,0.298687,0.302577,0.324257]
mape_3 = [17.462635, 12.766415, 12.221456, 9.307043, 9.974090, 11.372862,13.015509,9.306178,10.128281,10.507583,11.032033]

# 24, 25, 24, 26, 26, 26, 25, 25, 25, 27, 25, 25, 26
dates_1 = ['2017/06','2017/07','2017/08','2017/09','2017/10', '2017/11', '2017/12', '2018/01', '2018/02', '2018/03', '2018/04', '2018/05', '2018/06']
me_1_ovl = [-0.184800, -0.044400, -0.256667, -0.100000, 0.018462, 0.081538, 0.035200, -0.010400, -0.117200, -0.024815, -0.072400, -0.052400, 0.000385]
mea_1_ovl = [0.393600, 0.355600, 0.436667, 0.278462, 0.357692, 0.283846, 0.229600, 0.292000, 0.249200,0.231481,0.250800, 0.262000, 0.302692]
mape_1_ovl = [12.979564, 11.286014, 16.230907, 11.249750, 11.486153, 8.633658, 7.323471, 9.133035, 8.772886,7.463710,8.205743,8.754729, 10.048227]

dates_3 = ['2017/08','2017/09','2017/10','2017/11','2017/12','2018/01', '2018/02', '2018/03', '2018/04', '2018/05', '2018/06']
me_3_ovl = [-0.248333, -0.150769, -0.032308, 0.030769, -0.005200,-0.050800, -0.150400, -0.061852, -0.100400, -0.092400, -0.026538]
mea_3_ovl = [0.449167,0.326154, 0.336154, 0.312308, 0.241200, 0.317200, 0.264800, 0.215185, 0.290800, 0.282000,0.265000]
mape_3_ovl = [16.332842,12.883652, 10.730284, 9.616603, 7.691941, 10.046955, 9.088268, 6.988112, 9.594157, 9.402963,8.685974]

# plotting

# mape_3 = [11.372862,13.015509,9.306178,10.128281,10.507583,11.032033]
# mape_3_ovl = [10.046955, 9.088268, 6.988112, 9.594157, 9.402963,8.685974]

# print ('1-month overall accuracy %f' % (100 - np.mean(mape_1)))
# print ('1-month overall accuracy for ovl %f' % (100 - np.mean(mape_1_ovl)))
#
# print ('3-month overall accuracy %f' % (100 - np.mean(mape_3)))
# print ('3-month overall accuracy for ovl %f' % (100 - np.mean(mape_3_ovl)))

f, axs = plt.subplots(3, 1, sharex=True, figsize = (7, 5))

# axs[0].plot(dates_1, me_1, linestyle = '-', label = '1 month forecast')
# axs[0].plot(dates_3, me_3, label = '3 month forecast')

axs[0].plot(dates_1, me_1, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs[0].plot(dates_3, me_3, label = '3 month forecast', color = 'orange' )
axs[0].plot(dates_3, me_3_ovl, linestyle = '-', label = '3 month forecast - OVL', color = 'red')

axs[0].axhline(y = 0, color = 'k', linestyle='dashdot')
axs[0].grid(True)
axs[0].set_yticks(np.arange(-0.30, 0.30, step = 0.1))
axs[0].set_title('Mean Error (ME)')


axs[1].plot(dates_1, mea_1, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs[1].plot(dates_3, mea_3, label = '3 month forecast', color = 'orange')
axs[1].plot(dates_3, mea_3_ovl, linestyle = '-', label = '3 month forecast - OVL', color = 'red')

axs[1].grid(True)
axs[1].set_yticks(np.arange(0.1, 0.5, step = 0.1))
axs[1].set_title('Mean Absolute Error (MAE)')


axs[2].plot(dates_1, mape_1, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs[2].plot(dates_3, mape_3, label = '3 month forecast', color = 'orange')
axs[2].plot(dates_3, mape_3_ovl, linestyle = '-', label = '3 month forecast - OVL', color = 'red')

axs[2].grid(True)
axs[2].set_yticks(np.arange(6, 20, step = 2))
axs[2].set_title('Mean Absolute Percentage Error (MAPE)')

axs.flatten()[2].legend(loc='upper right', bbox_to_anchor=(1, 3.74), ncol=2)
#######################################################

f, axs_ovl = plt.subplots(3, 1, sharex=True, figsize = (7, 5))

axs_ovl[0].plot(dates_1, me_1_ovl, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs_ovl[0].plot(dates_3, me_3_ovl, label = '3 month forecast', color = 'yellowgreen' )

axs_ovl[0].axhline(y = 0, color = 'k', linestyle='dashdot')
axs_ovl[0].grid(True)
axs_ovl[0].set_yticks(np.arange(-0.30, 0.30, step = 0.1))
axs_ovl[0].set_title('Mean Error (ME)')

# axs[1].plot(dates_1, mea_1, linestyle = '-', label = '1 month forecast')
# axs[1].plot(dates_3, mea_3, label = '3 month forecast')
# axs[1].axhline(y = 0, color = 'k', linestyle='dashdot')

axs_ovl[1].plot(dates_1, mea_1_ovl, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs_ovl[1].plot(dates_3, mea_3_ovl, label = '3 month forecast', color = 'yellowgreen')

axs_ovl[1].grid(True)
axs_ovl[1].set_yticks(np.arange(0.1, 0.5, step = 0.1))
axs_ovl[1].set_title('Mean Absolute Error (MAE)')

# axs[2].plot(dates_1, mape_1, linestyle = '-', label = '1 month forecast')
# axs[2].plot(dates_3, mape_3, label = '3 month forecast')
# axs[1].axhline(y = 0, color = 'k', linestyle='dashdot')

axs_ovl[2].plot(dates_1, mape_1_ovl, linestyle = '-', label = '1 month forecast', color = 'forestgreen')
axs_ovl[2].plot(dates_3, mape_3_ovl, label = '3 month forecast', color = 'yellowgreen')

axs_ovl[2].grid(True)
axs_ovl[2].set_yticks(np.arange(6, 20, step = 2))
axs_ovl[2].set_title('Mean Absolute Percentage Error (MAPE)')

axs_ovl.flatten()[2].legend(loc='upper right', bbox_to_anchor=(1, 4.0), ncol=2)

# plt.figlegend(loc = 'lower center', bbox_to_anchor = (0.5, 0.00002))
plt.tight_layout()
plt.show()
