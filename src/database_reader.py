
import pandas as pd


def customer_query(**kwargs):

    # Import Data
    df_customer_database = pd.read_csv("data/processed/customer_Database.csv")

    binary_kwargs = {key: val for key, val in kwargs.items() if key in [
        "software_skills"]}
    feature_kwargs = {key: val for key, val in kwargs.items() if key not in [
        "software_skills"]}

    # Check the kwargs
    for key in feature_kwargs:
        if key not in df_customer_database:
            raise ValueError("{} not present in customer database".format(key))

    for key, val in binary_kwargs.items():
        for x in val:
            if x not in df_customer_database:
                raise ValueError(
                    "{} not present in customer database".format(key))

    # Instanciate dataframe to subselect
    df = df_customer_database.copy(deep=True)

    # Binary (e.g. software)
    for key, val in binary_kwargs.items():
        for x in val:
            df = df[df[x] == 1]

    # Others
    for key, val in feature_kwargs.items():
        df = df[df[key] == val]

    # Get list of customer # TODO change customer data type ?
    customers = []
    for _, customer in df.iterrows():
        customers.append(customer)

    return customers
