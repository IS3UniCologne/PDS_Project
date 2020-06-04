import pandas as pd
from .. import io
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def create_dummies(p_df):
    """Create dummie values for all usefull non numerical features.

    Args:
        p_df (DataFrame): Dataframe of trips in nuremberg
    Returns:
        df_dummies (DataFrame): Dataframe with dummies instead of booleans
    """
    p_spot_start = p_df["p_spot_start"].astype(int)
    p_bike_start = p_df["p_bike_start"].astype(int)
    weekend = p_df["Weekend"].astype(int)
    p_df.drop(["p_spot_start", "p_bike_start", "Weekend"], axis=1, inplace=True)
    df_dummies = pd.concat([p_df, p_spot_start, p_bike_start, weekend], axis=1)
    return df_dummies


def create_new_features(p_X):
    """Create new features which are usefull for prediction performance.

    Example methods for feature engineering could be found here:
    https://de.devoteam.com/blog-post/bedeutung-der-feature-engineering-methoden-2/
    Args:
        p_X (DataFrame): Dataframe of existing features (matrix)
    Returns:
        p_X (DataFrame): Dataframe with existing and new added features (matrix)
    """
    p_X["Hour_squared"] = np.square(p_X["Hour_start"])
    p_X["Day_squared"] = np.square(p_X["Day_start"])
    p_X["Month_squared"] = np.square(p_X["Month_start"])
    p_X["Minute_squared"] = np.square(p_X["Minute_start"])
    p_X["Weekend_squared"] = np.square(p_X["Weekend"])
    return p_X


def drop_end_information(p_df):
    """Drop all information of end of trips which are not used for duration prediction and model training.

    It does not make any sense to use information on trip ends to predict the duration of a trip.
    The idea is to predict the duration of a trip directly after the start/ booking.
    Args:
        p_df (DataFrame): Dataframe of existing features
    Returns:
        df (DataFrame): Dataframe only including start information
    """
    df = p_df.drop(
        ["p_spot_end",
         "p_place_type_end",
         "End_Time",
         "p_uid_end",
         "p_bikes_end",
         "Latitude_end",
         "b_bike_type_end",
         "Place_end",
         "End_Place_id",
         "Longitude_end",
         "p_bike_end",
         "Postalcode_end",
         "Month_end",
         "Day_end",
         "Hour_end",
         "Minute_end",
         "Day_of_year_end",
         "Dist_end",
         "Direction"],
        axis=1
    )
    return df


def drop_features(p_df):
    """Testing method for feature selection which drops features that should not be included in prediction and
    training of the ML models.

    This method is used to influence the performance of prediction on validation set.
    Args:
        p_df (DataFrame): Dataframe of existing features
    Returns:
        df (DataFrame): Dataframe only including start information
    """
    df = p_df
    do_it = True
    if do_it:
        df = p_df.drop(
            ["p_uid_start",
             "p_place_type_start",
             "p_bikes_start",
             "Month_start",
             "Day_start",
             "Start_Place_id",
             "p_spot_start"],
            axis=1
        )
    return df


def scale(p_X_train):
    """Scale all independent variables/ regressors  in DataFrame

    Args:
        p_X_train (DataFrame): DataFrame of independent variables/ regressors (matrix)

    Returns:
        X_train_scaled (DataFrame): DataFrame with scaled independent variables/ regressors (matrix)
    """
    st_scaler = StandardScaler()
    # fit scaler on training set not on test set
    st_scaler.fit(p_X_train)
    io.save_object(st_scaler, "Standard_Scaler.pkl")
    X_train_scaled = st_scaler.transform(p_X_train)
    return X_train_scaled


def do_pca(p_X_scaled_train):
    """Do a PCA to analyse which components to take for further predictions.

    PCA creates components from existing features by analysing the equality of variance.
    Multicolinearity will be nearly eliminated. => unbiasedness of models e.g. linear regression
    Args:
        p_X_scaled_train (DataFrame): DataFrame of scaled data
    Returns:
        X_train_scaled_pca (DataFrame): DataFrame of components
    """
    pca = PCA(n_components=12)
    pca.fit(p_X_scaled_train)
    print("Var explained:", pca.explained_variance_ratio_)
    print("Sum var explained", sum(pca.explained_variance_ratio_))
    io.save_object(pca, "PCA.pkl")
    X_train_scaled_pca = pca.transform(p_X_scaled_train)
    return X_train_scaled_pca
