import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import math

import plotly.graph_objs as go
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('marina09', '7Ki6XR0QqZt91vd5xpZm')


# single feature
def scatter_with_color_dimension_graph(feature, target, layout_labels):
    """
    Scatter with color dimension graph to visualize the density of the
    Given feature with target
    :param feature:
    :param target:
    :param layout_labels:
    :return:
    """
    trace1 = go.Scatter(
        y=feature,
        mode='markers',
        marker=dict(
            size='16',
            color=target,
            colorscale='red',
            showscale=True
        )
    )
    layout = go.Layout(
        title=layout_labels[2],
        xaxis=dict(title=layout_labels[0]), yaxis=dict(title=layout_labels[1]))
    data = [trace1]
    fig = Figure(data=data, layout=layout)
    # plot_url = py.plot(fig)
    py.image.save_as(fig, filename='Images\\DensityGraphs_PhysicalActivity\\' + layout_labels[1] + '_Density.png')


# plotting in two dimensions
def plot_decision_regions(X, y, classifier, labels, name, resolution = 0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('lightgreen', 'red', 'orange', 'gray', 'cyan')

    cmap = ListedColormap(colors[:len(np.unique(y))])

    # decision surface
    x1_min, x1_max = X[:, 0].min() -1, X[:, 0].max()-1
    x2_min, x2_max = X[:, 1].min() -1, X[:, 1].max()-1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha = 0.4, cmap = cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    risk_mapping = {'Risk alert': 2, 'Risk warning': 1, 'No risk': 0}
    inv_risk_mapping = {v:k for k,v in risk_mapping.items()}

    # samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], alpha = 0.8, c = cmap(idx), marker = markers[idx], label = inv_risk_mapping.get(cl))
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.legend(loc = 'upper left')
    plt.savefig('Images\\DensityGraphs_conf2310\\decision_regions' + '_' + name + '.png')


def plot_bubble_chart(data, variables, name):
    colors = ['gray', 'orange', 'red']
    cmap = ListedColormap(colors)
    X = data[variables].values
    y = data['risk_status'].values
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl,0], y=X[y==cl, 1], c = cmap(idx))
    plt.xlabel(variables[0])
    plt.ylabel(variables[1])
    plt.grid()
    plt.savefig('Images\\BubbleCharts\\bubble_chart_' + name + '.png')


def plot_density_graph_feature(data):
    for feature in data.columns[2:]:
        labels = ["Number of Observations", feature, feature]
        scatter_with_color_dimension_graph(data[feature], data['risk_status'], labels)


def plot_relative_changes(data, features):
    # for name in features:
    #     fig = plt.figure()
    #     ax = fig.add_subplot(1, 1, 1)
    #     ax.grid()
    #     risk_alert = data[data['risk_status'] == 2]
    #     ax.plot(range(0, len(risk_alert)), risk_alert[name], color = 'red')
    #     risk_warning = data[data['risk_status'] == 1]
    #     ax.plot(range(len(risk_alert), len(risk_alert)+len(risk_warning)), risk_warning[name], color = 'orange')
    #     risk_no = data[data['risk_status'] == 0]
    #     ax.plot(range(len(risk_alert)+len(risk_warning), len(data)), risk_no[name], color = 'green')
    #     fig.savefig("Images//PercChanges//" + name + ".png")
    for feature in features:
        print ('feature: ', feature)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        sorted_vals = sorted(data[feature])
        # sorted_vals = sorted_vals[:-30]
        length = len(sorted_vals)
        splits = 7 # 7
        ax.plot(range(0, len(sorted_vals)), sorted_vals, marker = '+', markeredgecolor = 'blue', linestyle = "")
        # ax.set_yticks([sorted_vals[item] for item in range(0, length, int(length/2))])
        # ax.set_yticks([sorted_vals[item] for item in range(0, length, int(length/splits))])
        # ax.set_yticks(np.arange(math.floor(min(sorted_vals)), math.ceil(max(sorted_vals)), 0.5))
        print ([sorted_vals[item] for item in range(0, length, int(length/splits))])
        # ax.set_yticks(np.arange(math.floor(min(sorted_vals))-0.5, math.ceil(max(sorted_vals))+0.5, 0.5), minor = True)
        ax.set_xticks(np.arange(0, length, int(length/splits)))
        ax.set_ylabel('Percentage Change (from the referent month)')
        ax.set_xlabel('Number of Observations')
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        fig.suptitle("Feature: " + feature)
        fig.savefig("Images//PercChanges//physical_activity//" + feature + "_sorted" + ".png")
