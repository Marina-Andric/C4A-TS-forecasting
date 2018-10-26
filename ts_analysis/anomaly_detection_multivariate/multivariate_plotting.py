from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler

def create_multi_variate_plot(data):
    ### Subplot the states multi-variate single user - By States

    hidden_states = data['cluster']
    num_clusters = len(np.unique(hidden_states))
    dates = data['interval_start']
    activities = data.columns.tolist()
    activities.remove('cluster')
    activities.remove('interval_start')

    fig, axs = plt.subplots(num_clusters, sharex=True, sharey=True)
    #colours = cm.rainbow(np.linspace(0, 1, model.n_components))
    colours = cm.rainbow(np.linspace(0, 1, len(activities)))
    # dates=pivoted_data['interval_end']
    i=0
    for ax in axs:
        # Use fancy indexing to plot data in each state.
        ax.grid(True)
        mask = hidden_states == i
        i=i+1
        for j in range(0, len(activities)):
            Y = data[activities[j]]
            ax.plot(dates[mask], Y[mask], ".-", c=colours[j], label=activities[j])

        ax.set_title("{0}. Behaviour".format(i))
        # Format the ticks.
        # ax.xaxis.set_major_locator(YearLocator())
        # ax.xaxis.set_minor_locator(MonthLocator())
        # ax.xaxis.set_minor_locator(DayLocator())

    fig.subplots_adjust(top=0.85, left=0.1, right=0.9, bottom=0.05, hspace = 0.25)
    plt.suptitle("User_in_role_id: 116", x= 0.1, horizontalalignment = 'left')
    axs.flatten()[1].legend(loc='upper right', bbox_to_anchor=(1, 2.89), ncol=2)
    plt.rcParams["figure.figsize"]=[13.0, 10.0]
    plt.xticks(rotation = 90)
    # plt.savefig( 'Plots/multi_variate/''citizen_id_'  + '.png')
    plt.show()


def create_multivariate_plot2(data):
    '''
    :param data: data with cluster assignments
    :return:
    '''
    # activities = data.columns.tolist()
    # activities.remove('cluster')
    # activities.remove('interval_start')
    # activities = list(data.columns)[1:-1]
    activities = ['walk_distance', 'physicalactivity_calories', 'physicalactivity_moderate_time', 'physicalactivity_soft_time', 'sleep_deep_time', 'sleep_wakeup_num']
    num_activities = len(np.unique(activities))

    hidden_states = data['cluster']
    num_clusters = len(np.unique(hidden_states))
    colours = cm.rainbow(np.linspace(0, 1, num_clusters))
    f, axarr = plt.subplots(num_activities, sharex=True)

    x = data['interval_start']
    i = 0
    for ax in axarr:
        Y = data[activities[i]]
        ax.set_title(activities[i])
        for a, x1, x2, y1, y2 in zip(hidden_states[1:], x[:-1], x[1:], Y[:-1], Y[1:]):
            ax.plot([x1, x2], [y1, y2], "-", c=colours[a])
            # if i!=0 and i!=1:
            #     ax.set_ylim([0, 30000])
            # ax.grid(True)
        i = i+1
    # plt.xticks(rotation = 90)
    plt.tick_params(labelbottom=False)
    plt.show()


def create_many_singlevariate_plots(data):
    f, axarr = plt.subplots(2, sharex = True)
    axarr[0].plot(data['interval_start'], data['walk_distance'])
    axarr[0].set_title('Walk_distance')
    axarr[1].plot(data['interval_start'], data['physicalactivity_calories'])
    axarr[1].set_title('Physicalactivity_calories')
    plt.show()


def plot_feature_distributions(data):
    plt.style.use('ggplot')
    # activities = ['walk_distance', 'physicalactivity_calories', 'sleep_deep_time']
    activities = list(data.columns)[1:]
    data[activities].hist(stacked=False, figsize=(20, 20), layout=(4,3), bins=20)
    plt.savefig('features_hist.png')
    plt.show()


# def plot_feature_normalized(data):
#     sc = StandardScaler()
#     for activity in list(data.columns)[1:]:
#         sc = sc.fit(data[activity].reshape(-1, 1))
#         data[activity] = sc.transform(data[activity].reshape(-1, 1))
#     plot_feature_distributions2(data)



def plot_feature_distributions2(data):
    f, axs = plt.subplots(4, 3, figsize = (8, 6))
    # sns.distplot(data['walk_distance'], ax=axs[0,0])
    # plt.show()
    indices = [list([i, j]) for i in range(4) for j in range(3)]
    for activity, idx in zip(list(data.columns)[1:], indices[0:11]):
        # axs[idx[0],idx[1]].set_title(activity)
        sns.distplot(data[activity], ax=axs[idx[0],idx[1]])
    f.delaxes(axs[3,2])
    plt.tight_layout()
    plt.savefig('feature distplots.png')
    plt.show()


def plot_cluster_distribution(data):
    '''
    :param data: data with cluster assignments
    :return:
    '''
    f, axs = plt.subplots(1, 1)
    sns.distplot(data['cluster'], ax=axs)
    plt.show()

def pca(data):
    '''
    :param data: data with cluster assignments
    :return:
    '''
    sc = StandardScaler()
    x = data.iloc[:, 1:-1].values
    y = data.iloc[:,-1].values
    x = sc.fit_transform(x) # data is standardized (x - mean)/std
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    print (pca.explained_variance_ratio_)
    print (np.sum(pca.explained_variance_ratio_))
    principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2'])
    finalDf = pd.concat([principalDf, data['cluster']], axis='columns')
    # print(finalDf)

    # visualization
    f, axs = plt.subplots()
    clusters = np.unique(data['cluster'])
    colors = ['r', 'g', 'b', 'black', 'yellow', 'pink']
    for cluster, color in zip(clusters, colors):
        plt.scatter(finalDf[finalDf['cluster'] == cluster]['pc1'], finalDf[finalDf['cluster'] == cluster]['pc2'], c=color, s=40)
    plt.legend(clusters)
    plt.title('2 Component PCA')
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.grid()
    plt.savefig('two principal components.png')
    plt.show()


def visualize_clustering(model, data):
    clusters = np.unique(data['cluster'])
    colors = ['r', 'g', 'indigo', 'yellow', 'black', 'lightblue']
    probabs = model.predict_proba(data.iloc[:, 1:-1])
    probabs_np = np.array(probabs)
    max_probab = np.amax(probabs_np, 1)
    data['max_probab'] = max_probab
    # data.to_csv('data with probabs.csv', sep = '\t')
    activityX = 'physicalactivity_soft_time'
    activityY = 'sleep_deep_time'
    for cluster, color in zip(clusters, colors):
        plt.scatter(data[data['cluster'] == cluster][activityX], data[data['cluster'] == cluster][activityY], c=color, s=data['max_probab']*100)
    plt.legend(clusters)
    plt.title('2 activities')
    plt.xlabel(activityX)
    plt.ylabel(activityY)
    plt.grid()
    plt.show()

