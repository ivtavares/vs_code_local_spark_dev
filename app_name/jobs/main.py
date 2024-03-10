from general_etl import bronze_to_silver
from pyspark.sql.types import *


# variable
bronze_audit_path = "s3://bronze/auditoria_municipal/6-siap-net-orgaos-municipais-autoridades-2016.csv"
silver_audit_path = "s3://silver/auditoria_municipal/"
partition="AnoExercicio"
file_type='csv'

audit_schema=StructType([
    
     StructField('CodigoMunicipio',IntegerType(), True)
    ,StructField('NomeMunicipio',StringType(), True)
    ,StructField('CodigoTipoOrgao',IntegerType(), True)   
    ,StructField('NomeTipoOrgao',StringType(), True) 
    ,StructField('AnoExercicio',IntegerType(), True)
    ,StructField('SequenciaOrgao',IntegerType(), True)
    ,StructField('NomeOrgao',StringType(), True) 
    ,StructField('CodigoAutoridade',IntegerType(), True)
    ,StructField('Trata',StringType(), True) 
    ,StructField('mentoAutoridade',StringType(), True) 
    ,StructField('CargoAutoridade',StringType(), True) 
    ,StructField('SequenciaAutoridade',IntegerType(), True)
    ,StructField('Nome',StringType(), True) 
    ,StructField('Sexo',StringType(), True) 
    ,StructField('InicioMandato',DateType(), True) 
    ,StructField('FimMandato',DateType(), True) 
])


if __name__ == '__main__':
    bronze_to_silver(bronze_audit_path, silver_audit_path, audit_schema, partition, file_type)