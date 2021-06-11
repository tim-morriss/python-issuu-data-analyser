import matplotlib.pyplot as plt


class HistogramPlot:

    # adapted from python sample simple_histo.py
    def show_histo(self, data, orient="h", xlabel="counts", title="title"):
        """Takes a dictionary of counts and show it as a histogram.

        Parameters
        ----------
        data : dict
            dictionary to graph
        orient : str
            h for horizontal, v for vertical
        xlabel : str
            label for the x-axis
        title : str
            title of the graph
        """

        if data:
            if orient == "h":
                bar_fun = plt.barh  # NB: this assigns a function to bar_fun!
                bar_ticks = plt.yticks
                value_ticks = plt.xticks
                plt.ticklabel_format(axis='x', style='plain')   # avoid sci notation
                bar_label = plt.xlabel
            elif orient == "v":
                bar_fun = plt.bar
                bar_ticks = plt.xticks
                value_ticks = plt.yticks
                plt.ticklabel_format(axis='y', style='plain')   # avoid sci notation
                bar_label = plt.ylabel
            else:
                raise Exception("show_histo: Unknown orientation: %s " % orient)

            n = len(data)
            bar_fun(range(n), list(data.values()), align='center')
            bar_ticks(range(n), list(data.keys()))  # NB: uses a higher-order function
            max_val = max(data.values())
            min_val = min(data.values())
            # # adapted from https://stackoverflow.com/a/22085818
            if min_val != max_val:
                val = max_val - min_val
                val = [i * val / 5 for i in range(1, 6)].append(max_val)
                value_ticks(val)
            bar_label(xlabel)
            plt.title(title)
            plt.show()

        else:
            print("Nothing to plot!")
