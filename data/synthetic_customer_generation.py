import pandas as pd
import numpy as np
import unidecode


# Get likely data
df_noms = pd.read_csv("data/raw/noms.txt", sep="\t")
noms = list(df_noms.sort_values("_1991_2000").loc[:,"NOM"].values[-100:-1])

df_prenoms = pd.read_csv("data/raw/prenoms.csv")
df_prenoms = df_prenoms[df_prenoms["ANNEE"] < 2000]
df_prenoms = df_prenoms[df_prenoms["ANNEE"] > 1960]
prenoms = list(df_prenoms.set_index(["ENFANT_PRENOM"]).groupby("ENFANT_PRENOM").apply(lambda x: x.loc[:,"NOMBRE_OCCURRENCES"].sum()).sort_values()[-100:].index)

df_entreprises = pd.read_csv("data/raw/entreprises.csv",  error_bad_lines=False, sep=";")
adresses = df_entreprises[['Adresse', 'Code postal', 'Ville', 'Num. dept.',
       'Département', 'Région']].dropna()

adresses = adresses.rename(columns={
    "Région" : "region",
    "Code postal" : "postcode",
    "Département" : "departement",
    "Num. dept." : "departement_number",
    "Ville" : "city"
})

competences = [
    ("Aeronautique", "Ingénieur d'étude", ["Python", "Java"]),
    ("Aeronautique", "Ingénieur d'étude", ["Python"]),
    ("Aéronautique", "Ingénieur en informatique", ["Python", "Java", "C++"]),
    ("Mecanique", "Ingénieur d'étude", ["Java", "Matlab"]),
    ("Mecanique", "Ingénieur conception mécanique", ["Simulink", "Matlab"]),
    ("Mecanique", "Ingénieur conception mécanique", ["Simulink", "Matlab", "Python"]),
    ("Pharma", "Ingénieur en informatique", ["C++", "Java", "Python"]),
    ("Pharma", "Biostatisticien", ["Python", "R"]),
    ("Pharma", "Biostatisticien", ["R"]),
]

logiciels_existant = list(np.unique(np.concatenate([x[2] for x in competences])))

# Compute a customer database

def simulate_customer(noms, prenoms, competences, adresses, logiciels_existant, nom_entreprise, id):

    customer = {}

    nom = np.random.choice(noms, 1)[0]
    prenom = np.random.choice(prenoms, 1)[0]
    telephone = "06"+"".join([str(np.random.randint(0,9)) for i in range(8)])
    adresse = adresses.iloc[np.random.randint(low= 0, high=len(adresses)-1),:].to_dict()
    competence = competences[np.random.randint(low= 0, high=len(competences)-1)]

    customer["cust_id"] = id
    customer["surname"] = nom
    customer["name"] = prenom
    prenom_processed = unidecode.unidecode(prenom.lower())
    nom_processed = unidecode.unidecode(nom.lower().replace(" ",""))
    customer["mail"] = "{}.{}@{}.com".format(prenom_processed, nom_processed , nom_entreprise)
    customer["phone"] = telephone
    customer["firm_name"] = nom_entreprise
    customer["branch"] = competence[0]
    customer["job"] = competence[1]

    for log in logiciels_existant:
        customer[log] = 1 if log in competence[2] else 0

    for key, val in adresse.items():
        customer[key] = val

    return customer

df_customer_database = pd.DataFrame()
for i in range(100):
    customer = simulate_customer(noms, prenoms, competences, adresses, logiciels_existant, nom_entreprise="boite_{}".format(i), id=i)
    df_customer_database = pd.concat([df_customer_database, pd.DataFrame(customer, index=[i])])

df_customer_database.set_index("cust_id").to_csv("data/processed/customer_database.csv")



# Compute a candidate database

def simulate_candidate(noms, prenoms, competences, adresses, logiciels_existant, id):
    candidate = {}

    nom = np.random.choice(noms, 1)[0]
    prenom = np.random.choice(prenoms, 1)[0]
    telephone = "06"+"".join([str(np.random.randint(0,9)) for i in range(8)])
    adresse = adresses.iloc[np.random.randint(low= 0, high=len(adresses)-1),:].to_dict()
    competence = competences[np.random.randint(low= 0, high=len(competences)-1)]
    internet_provider = np.random.choice(["gmail", "yahoo", "outlook"], 1)[0]

    candidate["cand_id"] = id
    candidate["surname"] = nom
    candidate["name"] = prenom
    candidate["mail"] = "{}.{}@{}.com".format(prenom.lower(), nom.lower().replace(" ",""), internet_provider)
    candidate["phone"] = telephone
    candidate["branch"] = competence[0]
    candidate["job"] = competence[1]

    for log in logiciels_existant:
        candidate[log] = 1 if log in competence[2] else 0

    for key, val in adresse.items():
        candidate[key] = val

    return candidate

df_candidate_database = pd.DataFrame()
for i in range(20):
    candidate = simulate_candidate(noms, prenoms, competences, adresses, logiciels_existant, id=i)
    df_candidate_database = pd.concat([df_candidate_database, pd.DataFrame(candidate, index=[i])])

df_candidate_database.set_index("cand_id").to_csv("data/processed/candidate_database.csv")

