# fichier de connexion au bucket S3 avec boto3

import boto3
import psycopg2
import pandas as pd
import sys
import io
import os
import dotenv
from dotenv import load_dotenv, find_dotenv

# on utilise un env pour masquer les identifiants de connexion.


# on crée une fonction qui va nous permettre de se connecter au bucket S3 et de récupérer les données csv


# la fonction renverra un dataframe pandas pour chaque csv.

def session_boto3():
    # avec load_dotenv je charge un .env que j etrouve avec la fonction find_dotenv
    load_dotenv(find_dotenv("/home/gregoirek/Documents/JEDHA/2_Fullstack/x_projet_final/dotenv/.env"))
    # je créer une session avec boto3 dans laquel je passe mes key (du fihcier .env)
    # la .session() de boto" meconnecte à AWS
    session = boto3.Session(aws_access_key_id=os.environ.get("AWS_S3_ACCESS_KEY_ID"), 
                            aws_secret_access_key=os.environ.get("AWS_S3_SECRET_ACCESS_KEY"),
                            region_name='eu-west-3')   
    return session

def connexion_s3(session_boto3):
    os.environ.clear()

 
     # avec load_dotenv je charge un .env que j etrouve avec la fonction find_dotenv
    load_dotenv(find_dotenv("/home/gregoirek/Documents/JEDHA/2_Fullstack/x_projet_final/dotenv/.env"))

    
    # la variable session contient la session de connexion 
    # avec .resosurce() je précise que je veux acceder à s3
    s3 = session_boto3.resource("s3")

    # se connecter à un bucket avec la fonction .Bucket()
    bucket = s3.Bucket("bucketprojetfinal")

    return "Connexion réussie au bucket S3."

def connexion_rds(session_boto3):
    os.environ.clear()
    ENDPOINT= "database-1.cxpuckismlkx.eu-west-3.rds.amazonaws.com"
    PORT = "5432"
    USER= "postgres"
    REGION="eu-west-3a"
    DBNAME = "postgres"


    # avec load_dotenv je charge un .env que j etrouve avec la fonction find_dotenv
    load_dotenv(find_dotenv("/home/gregoirek/Documents/JEDHA/2_Fullstack/x_projet_final/dotenv/.env"))
    # je créer une session avec boto3 dans laquel je passe mes key (du fihcier .env)
    # la .session() de boto" meconnecte à AWS

    rds_client = session_boto3.client('rds')
    #token = rds_client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
    #print(token, type(token))
    try:
        connexion = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=os.environ.get("AWS_RDS_PASSWORD"), sslrootcert="SSLCERTIFICATE")
        cursor = connexion.cursor()
        cursor.execute("""SELECT now()""")
        query_results = cursor.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e)) 

    return "Connexion réussie au bucket rds."




