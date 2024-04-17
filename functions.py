def read_and_clean(url="https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file1.csv"):

    """ Cargamos el contenido:
        - Importamos el archivo
        - Modificamos el nombre de las columnas y las formateamos

    """

    import pandas as pd

    df = pd.read_csv(url)

    df.columns = df.columns.str.lower().str.replace(" ","_")

    df = df.rename(columns = {
        "st" : "state"
    })

    """Limpiamos los valores de 'gender':
        - Creamos un nuevo diccionario con los valores.
        - Reemplazamos los valores en 'gender'
    """

    gender_values_to_combine = {
        "Femal" : "F",
        "female" : "F",
        "Male" : "M"
    }

    df["gender"] = df["gender"].replace(gender_values_to_combine)

    """Limpiamos los valores de 'state':
        - Creamos un nuevo diccionario con los valores.
        - Reemplazamos los valores en 'state'
    """

    state_values_to_combine = {
        "AZ" : "Arizona",
        "WA" : "Washington",
        "Cali" : "California"
    }

    df["state"] = df["state"].replace(state_values_to_combine)

    """Limpiamos los valores de 'education':
        - Creamos un nuevo diccionario con los valores.
        - Reemplazamos los valores en 'education'
    """

    education_values_to_combine = {
        "Bachelors" : "Bachelor",
    }

    df["education"] = df["education"].replace(education_values_to_combine)

    #formateamos la columna customer lifetime value para eliminar el '%'
    try:
        df["customer_lifetime_value"] = df["customer_lifetime_value"].str.replace("%","")
    except:
        None

    #crea un nuevo diccionario con los nuevos valores para 'vehicle_class'

    vehicle_class_values_to_combine = {
        "Sports Car" : "Luxury",
        "Luxury SUV" : "Luxury",
        "Luxury Car" : "Luxury"
    }

    #reemplaza los nuevos valores en 'vehicle_class'

    df["vehicle_class"] = df["vehicle_class"].replace(vehicle_class_values_to_combine)

    #modifica el tipo de valor de 'customer_lifetime_value' a float

    df["customer_lifetime_value"] = df[["customer_lifetime_value"]].astype(float)

    try:
        df["number_of_open_complaints"] = df["number_of_open_complaints"].str.split("/").str[1]
    except:
        None
        
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')

    #vemos que las filas que no tienen valor en customer el resto de datos también están vacíos

    df[df["customer"].isnull()].describe(include="all")

    #elimino las filas con todos los valores nulos

    df = df.dropna(subset=["customer"])

    #los nulos de 'customer_lifetime_value' los voy a cambiar por la media 

    df["customer_lifetime_value"] = df[["customer_lifetime_value"]].astype(float)

    df["customer_lifetime_value"] = df["customer_lifetime_value"].fillna(df["customer_lifetime_value"].mean())

    gender_mode = df["gender"].mode()

    df["gender"].fillna(gender_mode[0], inplace=True)

    #veo que el único valor númerico que no es float o int es number_of_complaints, así que lo modifico por int

    df["number_of_open_complaints"] = df[["number_of_open_complaints"]].astype(int)

    return df