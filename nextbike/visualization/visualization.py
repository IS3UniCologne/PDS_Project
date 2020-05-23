import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from .. import io


# TODO: To think of if the visualize_moment method is not just the helper for the plotting method...
# TODO: Visualize the number of bikes at fixed stations => trace all bikes back? Maybe just because there
def visualize_moment(df):
    """Visualize one moment in time with the most trip starts

    Collect starts at fixed stations, starts at free bikes, unused stations.
    Hand them over to plot_map() method.
    Args:
        df (DataFrame): DataFrame with trip data from nuremberg
    Returns:
        no return
    """

    # TODO: Motivated BEE <3: Search usefull time for this plot
    # For one moment in time, visualize the number of bikes at fixed stations meaningfully.
    most_bookings = df.groupby(by="Start Time").count()["Bike Number"].sort_values().tail(1).index
    # choose Datetime 3

    # ToDo: Stations with no bikes right now visualize in grey

    for time in most_bookings:
        print("Compute Moment at: " + str(time) + " ...")

        df_moment = df[df["Start Time"] == time]
        # get stations without Start Place_id != 0.0
        df_help = pd.DataFrame(df_moment[df_moment["Start Place_id"] != 0.0]["Start Place_id"])
        # get unique long lat for stations
        df_long_lat = df_moment.drop_duplicates("Start Place_id")[
            ["Start Place_id", "Latitude_start", "Longitude_start"]]
        df_long_lat = df_long_lat[df_long_lat["Start Place_id"] != 0.0]
        df_stations = df_help.merge(df_long_lat, how="left", on="Start Place_id")
        # get bikes with with Start Place_id = 0.0
        df_free = df_moment[df_moment["Start Place_id"] == 0.0][["Start Place_id", "Longitude_start", "Latitude_start"]]
        # get unused stations at given date
        df_helper_unused = df.drop_duplicates("Start Place_id")[["Start Place_id", "Latitude_start", "Longitude_start"]]
        df_helper_unused = df_helper_unused[df_helper_unused["Start Place_id"] != 0.0]
        df_unused = df_helper_unused.append(df_stations).drop_duplicates(keep=False)
        plot_map(df_stations, df_free, df_unused, time)


def plot_map(pDf_stations, pDf_free, pDf_unused, pStr_datetime):
    """Plot starts at stations, starts of free bikes and unused stations at given time.

    Args:
        pDf_stations (DataFrame): DataFrame with all bikes at fixed stations at some time
        pDf_free (DataFrame): DataFrame with all free bikes at some time
        pDf_unused (DataFrame): DataFrame with all unused stations at some time
        pStr_datetime (str): datetime of some time
    Returns:
        no return
    """
    # Todo: Class with constants
    north = 49.485
    east = 11.13
    south = 49.425
    west = 11.02

    # read img nuremberg
    # https://www.openstreetmap.org/export#map=12/49.4522/11.0770
    nuremberg_png = plt.imread(io.get_path(filename="nuremberg_v2_hum.png", io_folder="input"))

    fig, ax = plt.subplots(figsize=(10, 10))
    free = ax.scatter(pDf_free["Longitude_start"],
                      pDf_free["Latitude_start"],
                      zorder=1, alpha=0.2, c="r", s=14)

    station = ax.scatter(pDf_stations["Longitude_start"],
                         pDf_stations["Latitude_start"],
                         zorder=1, alpha=0.08, c="b", s=30)

    unused = ax.scatter(pDf_unused["Longitude_start"],
                        pDf_unused["Latitude_start"],
                        zorder=1, alpha=0.5, c="grey", s=30)

    ax.set_title('Bikes at ' + str(pStr_datetime))
    ax.set_xlim(west, east)
    ax.set_ylim(north, south)
    plt.legend((station, free, unused), ("Bikes at Station", "Free Bikes", "Unused Stations"), loc="upper left")
    ax.imshow(nuremberg_png, zorder=0, extent=[west, east, north, south], aspect='equal')
    plt.savefig(io.get_path(filename=(str(pStr_datetime).replace(":", "-") + ".png"), io_folder="output",
                            subfolder="data_plots"), dpi=300)


def visualize_distribution(df):
    """Plots the distribution of trip lengths per month including quantile lines

    Args:
        df (DataFrame): DataFrame with trip data from nuremberg
    Returns:
        no return
    """
    # Visualize the distribution of trip lengths per month. Compare the distributions to normal
    # distributions with mean and standard deviation as calculated before (1.d))

    # TODO: Code to start on
    """
    # histogram of duration

    #data
    duration = df_booking_data['DURATION_MINUTES']
    values, base = np.histogram(duration, bins=120, range=(0,120), weights=np.ones(len(duration))/len(duration))
    quantile_25 = np.quantile(duration, 0.25)
    quantile_50 = np.quantile(duration, 0.5)
    quantile_75 = np.quantile(duration, 0.75)
    quantile_95 = np.quantile(duration, 0.95)

    #plotting
    Fig_Usage = plt.figure(figsize=(20,8),dpi = 240)
    ax = Fig_Usage.add_axes([0,0,0.5,0.5])
    ax.set_xlabel('Duration of Booking [min]')
    ax.set_ylabel('Percentage')
    ax.set_title('Distribution of Duration')
    plt.plot(base[:-1], values, c='blue')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.vlines(quantile_25, 0, 0.07, linestyles='dashed', label='25% Quantile', colors='green')
    plt.vlines(quantile_50, 0, 0.07, linestyles='dashed', label='50% Quantile', colors='yellow')
    plt.vlines(quantile_75, 0, 0.07, linestyles='dashed', label='75% Quantile', colors='red')
    plt.vlines(quantile_95, 0, 0.07, linestyles='dashed', label='95% Quantile')
    plt.legend(loc='upper right')
    plt.show()
    Fig_Usage.savefig("DurationMinutes_Distribution.png", bbox_inches='tight')
    """

    print()


def visualize_more(df):
    """TODO: What else can we visualize?

    Args:
        df (DataFrame): DataFrame with trip data from nuremberg
    Returns:
        no return
    """
    # These visualizations are the minimum requirement.
    # Use more visualizations wherever it makes sense.

    print()
