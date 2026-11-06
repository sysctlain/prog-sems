import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm

# Не нейрослопный opinionated модуль для лаб и визуализации
p = plt.rcParams
p["figure.figsize"] = 6, 2.5
p["figure.edgecolor"] = "black"
p["figure.facecolor"] = "#f9f9f9"

p["axes.linewidth"] = 1
p["axes.facecolor"] = "#f9f9f9"
p["axes.ymargin"] = 0.1
p["axes.spines.bottom"] = True
p["axes.spines.left"] = True
p["axes.spines.right"] = False
p["axes.spines.top"] = False
p["font.sans-serif"] = ["Roboto"]

p["axes.grid"] = False
p["grid.color"] = "black"
p["grid.linewidth"] = 0.1

p["xtick.bottom"] = True
p["xtick.top"] = False
p["xtick.direction"] = "out"
p["xtick.major.size"] = 5
p["xtick.major.width"] = 1
p["xtick.minor.size"] = 3
p["xtick.minor.width"] = 0.5
p["xtick.minor.visible"] = True

p["ytick.left"] = True
p["ytick.right"] = False
p["ytick.direction"] = "out"
p["ytick.major.size"] = 5
p["ytick.major.width"] = 1
p["ytick.minor.size"] = 3
p["ytick.minor.width"] = 0.5
p["ytick.minor.visible"] = True

p["lines.linewidth"] = 2
p["lines.marker"] = "o"
p["lines.markeredgewidth"] = 1.5
p["lines.markeredgecolor"] = "auto"
p["lines.markerfacecolor"] = "white"
p["lines.markersize"] = 6


# def read_file_into_dataframe


def plot_df(df: DataFrame, **kwargs):
    if len(df.columns) == 4:
        xl, yl, dxl, dyl = df.columns
        dx = df[dxl]
        dy = df[dyl]
    elif len(df.columns) == 3:
        xl, yl, dyl = df.columns
        dx = np.zeros(df.size)
        dy = df[dyl]
    elif len(df.columns) == 2:
        xl, yl = df.columns
        dx = []
        dy = []
    else:
        raise Exception("Invalid DataFrame provided")

    plot(df[xl], df[yl], xerr=dx, yerr=dy, title=f"{yl}({xl})", xlabel=xl, ylabel=yl, **kwargs)


def plot(x: Series, y: Series, xerr:Series = Series(), yerr:Series = Series(), title="Крутой график", \
         xlabel=r"$X$", ylabel=r"$Y$", show_zero=False, linearize=True):
    fig, ax = plt.subplots(figsize=(5, 5))

    ax.set_title(title)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":")
    ax.grid(True, which="major", linestyle="--")

    if show_zero:
        ax.set_xlim([0, x.max()])
        ax.set_ylim([0, y.max()])

    # ax.scatter(x, y, marker='^', c="red", alpha=0.8)
    print(xerr, yerr)

    errors = (not xerr.empty) and (not yerr.empty)
    if errors:
        ax.errorbar(x, y, marker="o", xerr=xerr, yerr=yerr)

    ax.plot(x, y, c="black", linestyle='-', marker='o')


    if linearize:
        if errors:
            #only yerr

            (k, b), cov = np.polyfit(x, y, deg=1, w=1/yerr, cov='unscaled')
            k_err, b_err = np.sqrt(np.diag(cov))

            print(ax.get_xlim(), ax.get_ylim())
            xx = np.arange(*ax.get_xlim())
            print(xx)
            ax.plot(x, k * x + b, label=rf"МНК: $k=({k:.2f}\pm{k_err:.2f})$, $b=({b:.2f}\pm{b_err:.2f})$", linestyle="--")
        else:
            k, b = np.polyfit(x, y, deg=1)
            ax.plot(x, k * x + b, label=f"МНК: k={k:.2f}, b={b:.2f}", linestyle="--")

    
    ax.legend()

    # return fig, ax

    plt.show()

# histograms
# 2d
# 3d