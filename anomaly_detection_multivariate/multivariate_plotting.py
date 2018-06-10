from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator
import numpy as np


def create_multi_variate_plot(data, activities):
    ### Subplot the states multi-variate single user - By States
    num_clusters = len(np.unique(data['cluster']))
    hidden_states = data['cluster']
    dates = data['interval_start']

    fig, axs = plt.subplots(num_clusters, sharex=True, sharey=True)
    #colours = cm.rainbow(np.linspace(0, 1, model.n_components))
    colours = cm.rainbow(np.linspace(0, 1, len(activities)))
    # dates=pivoted_data['interval_end']
    i=0
    lines=[]
    for ax in axs:
        # Use fancy indexing to plot data in each state.
        mask = hidden_states == i
        i=i+1
        for j in range(len(activities)):
            Y = data[activities[j]]
            lines.append(ax.plot_date(dates[mask], Y[mask], ".-", c=colours[j], label=activities[j]))

        ax.set_title("{0}. Behaviour".format(i))
        # Format the ticks.
        #ax.xaxis.set_major_locator(YearLocator())
        ax.xaxis.set_minor_locator(MonthLocator())
        ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True)

    fig.subplots_adjust(top=0.85, left=0.1, right=0.9, bottom=0.05, hspace = 0.25)
    plt.suptitle("User_in_role_id: 116", x= 0.1, horizontalalignment = 'left')
    axs.flatten()[1].legend(loc='upper right', bbox_to_anchor=(1, 2.89), ncol=2)
    plt.rcParams["figure.figsize"]=[13.0, 10.0]
    plt.xticks(rotation = 90)
    # plt.savefig( 'Plots/multi_variate/''citizen_id_'  + '.png')
    plt.show()

