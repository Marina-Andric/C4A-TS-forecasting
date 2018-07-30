from matplotlib import cm, pyplot as plt
import numpy as np
import itertools

def plot_time_series(data, user, activity):
    plt.figure(figsize=(10, 4))
    X = data['interval_start']
    Y = data[activity]
    plt.grid(True)
    plt.plot(X, Y)
    plt.title("User_in_role_id: " + str(user) + "     Activity: "+ activity)
    plt.show()

def create_single_variate_plot(data, user, clusters, activity):
    figure = plt.figure(figsize=(10, 6))
#     data=data.loc[(data['user_in_role_id'] == user) & (data['detection_variable_name'].isin([activity]))]
#     data.sort_values(by = ['interval_end'])
    hidden_states = clusters[100:450]
    num_clusters = len(np.unique(clusters))
#     dates=pd.to_datetime(data['interval_end'])
    dates = data['interval_start']
    fig, axs = plt.subplots(num_clusters, sharex=True, sharey=True)
    # colours = cm.rainbow(np.linspace(0, 1, num_clusters))
    colours = ["b", "g", "r", "maroon", "lightskyblue", "slategrey", "mediumspringgreen", "hotpink", "gold", "indigo"]
    i=0
    lines=[]
    dates = dates[100:450]
    for ax in axs:
        mask = hidden_states == i
        Y = data[activity][100:450]
        ax.plot_date(dates[mask], Y[mask], ".-", c=colours[i], label =activity)
        i=i+1
        ax.set_title("{0}. Behaviour".format(i))
        # Format the ticks.
        # ax.xaxis.set_major_locator(YearLocator())
#         ax.xaxis.set_minor_locator(MonthLocator())
#         ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True)
        # plt.suptitle("User_in_role_id: " + str(results[0]) + "     Activity: "+str(results[1]))
        # plt.savefig(path_store + 'user_' + str(results[0])+ '_activity_'+str(results[1])+'.png', bbox_inches='tight')
    fig.subplots_adjust(top=0.89, left=0.06, right=0.98, bottom=0.12, hspace = 0.25)
    #axs.flatten()[-1].legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=2)
    # plt.suptitle("User_in_role_id: " + str(user) + "     Activity: "+ activity)
    # plt.rcParams["figure.figsize"]=[25.0, 15.0]
    plt.tight_layout()
    # plt.savefig('citizen_id_' + str(user) + '_activity_' + activity + '.png', dpi=1000)
    plt.show()
#     plt.savefig( 'Plots/single_variate/''citizen_id_' + str(user)+ '_activity_'+ activity +'.png')

def create_oneSeries_single_variate_plot(data, user, clusters, activity):
    figure = plt.figure(figsize=(10, 4))
    plt.clf()
#     data = data.loc[(data['user_in_role_id'] == user) & (data['detection_variable_name'].isin([activity]))]
#     data['interval_end'] = pd.to_datetime(data['interval_end'])
#     data.sort_values(by = ['interval_end'])
    num_clusters = len(np.unique(clusters))
    dates = data['interval_start']
    hidden_states = clusters
    a = hidden_states
    x = dates
    Y = data[activity]

    # colours = cm.rainbow(np.linspace(0, 1, 10))
    colours = ["b", "g", "r", "maroon", "lightskyblue", "slategrey", "mediumspringgreen", "hotpink", "gold", "indigo"]

    for a, x1, x2, y1, y2 in zip(a[1:], x[:-1], x[1:], Y[:-1], Y[1:]):
        plt.plot_date([x2, x1], [y2, y1], "-", c=colours[a])
        plt.grid(True)

    plt.subplots_adjust(top=0.89, left=0.1, right=0.9, bottom=0.12)
    # plt.suptitle("User_in_role_id: " + str(user) + "     Measure: " + activity)
    # plt.rcParams["figure.figsize"] = [25.0, 15.0]
#     plt.savefig('Plots/transitions/''Transition_citizen_id_' + str(user)+ '_activity_'+ activity +'.png')
    plt.tight_layout()
    # plt.savefig('transitions_citizen_id_' + str(user) + '_activity_' + activity + '.png')
    plt.show()
    plt.close()
    #plt.show()

