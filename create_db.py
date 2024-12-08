import pandas as pd
import sqlite3

file_path = "diabetes.csv"
data = pd.read_csv(file_path)

con = sqlite3.connect("tutorial.db")
cursor = con.cursor()

create_table_query = """
CREATE TABLE DiabetesData (
    PatientID INTEGER PRIMARY KEY,
    Diabetes_binary INTEGER,  -- 0 = no diabetes, 1 = prediabetes, 2 = diabetes
    HighBP INTEGER,           -- 0 = no high BP, 1 = high BP
    HighChol INTEGER,         -- 0 = no high cholesterol, 1 = high cholesterol
    CholCheck INTEGER,        -- 0 = no cholesterol check in 5 years, 1 = yes cholesterol check in 5 years
    BMI REAL,                 -- Body Mass Index
    Smoker INTEGER,           -- Have you smoked at least 100 cigarettes in your entire life? 0 = no, 1 = yes
    Stroke INTEGER,           -- (Ever told) you had a stroke. 0 = no, 1 = yes
    HeartDiseaseorAttack INTEGER, -- Coronary heart disease (CHD) or myocardial infarction (MI) 0 = no, 1 = yes
    PhysActivity INTEGER,     -- Physical activity in past 30 days - not including job 0 = no, 1 = yes
    Fruits INTEGER,           -- Consume Fruit 1 or more times per day 0 = no, 1 = yes
    Veggies INTEGER,          -- Consume Vegetables 1 or more times per day 0 = no, 1 = yes
    HvyAlcoholConsump INTEGER, -- Adult men >=14 drinks per week and adult women >=7 drinks per week 0 = no, 1 = yes
    AnyHealthcare INTEGER,    -- Have any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc. 0 = no, 1 = yes
    NoDocbcCost INTEGER,      -- Was there a time in the past 12 months when you needed to see a doctor but could not because of cost? 0 = no, 1 = yes
    GenHlth INTEGER,          -- General health rating (1-5) 1 = excellent, 2 = very good, 3 = good, 4 = fair, 5 = poor
    MentHlth INTEGER,         -- Days of poor mental health (1-30 days)
    PhysHlth INTEGER,         -- Physical illness or injury days in past 30 days (1-30 days)
    DiffWalk INTEGER,         -- Do you have serious difficulty walking or climbing stairs? 0 = no, 1 = yes
    Sex INTEGER,              -- 0 = female, 1 = male
    Age INTEGER,              -- 13-level age category (_AGEG5YR see codebook) 1 = 18-24, 9 = 60-64, 13 = 80 or older
    Education INTEGER,        -- Education level (EDUCA see codebook) scale 1-6, 1 = Never attended school or only kindergarten, etc.
    Income INTEGER           -- Income scale (INCOME2 see codebook) scale 1-8, 1 = less than $10,000, 5 = less than $35,000, 8 = $75,000 or more
);
"""
cursor.execute("DROP TABLE IF EXISTS DiabetesData;")
cursor.execute(create_table_query)
con.commit()

def add(data_entry, cursor):
    cursor.execute(
        "INSERT INTO DiabetesData (Diabetes_binary, HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk, Sex, Age, Education, Income) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        data_entry
    )

for index, row in data.iterrows():
    add(tuple(row), cursor)

con.commit()


query = "SELECT * FROM DiabetesData WHERE PatientID = 2;"
result = cursor.execute(query).fetchall()
print(result)