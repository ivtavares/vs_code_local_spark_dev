from app_name.configs.spark_helper import create_delta_lake_session
from pyspark.sql import functions as F

# variable path
bronze_audit_path = "s3://bronze/auditoria_municipal/6-siap-net-orgaos-municipais-autoridades-2016.csv"
silver_audit_path = "s3://silver/auditoria_municipal/"


# bronze to silver function
def audit_bronze_to_silver(bronze_path: str, silver_path: str):
    spark = create_delta_lake_session('auditoria')
    
    # Create df
    auditoria_df = (spark.read.option("delimiter", ";") 
                          .option("header", True)
                          .option('encoding', 'ISO-8859-1') 
                          .csv(bronze_path))
    
    # Change Schema
    auditoria_df_01 = auditoria_df.select(F.col('CodigoMunicipio').cast('int')  
                                         ,F.col('NomeMunicipio')
                                         ,F.col('CodigoTipoOrgao').cast('int')   
                                         ,F.col('NomeTipoOrgao') 
                                         ,F.col('AnoExercicio').cast('int') 
                                         ,F.col('SequenciaOrgao').cast('int') 
                                         ,F.col('NomeOrgao') 
                                         ,F.col('CodigoAutoridade').cast('int')
                                         ,F.col('Trata') 
                                         ,F.col('mentoAutoridade') 
                                         ,F.col('CargoAutoridade') 
                                         ,F.col('SequenciaAutoridade').cast('int') 
                                         ,F.col('Nome') 
                                         ,F.col('Sexo') 
                                         ,F.to_date('InicioMandato', 'dd/MM/yyyy').alias('InicioMandato')
                                         ,F.to_date('FimMandato', 'dd/MM/yyyy').alias('FimMandato'))    
    
    # write df to parquet
    auditoria_df_01.write.parquet(path=silver_path, mode="overwrite", partitionBy="AnoExercicio")
    
    spark.stop()
    
    
if __name__ == '__main__':
    audit_bronze_to_silver(bronze_audit_path, silver_audit_path)

