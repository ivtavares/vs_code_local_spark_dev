from app_name.configs.spark_helper import create_delta_lake_session
from pyspark.sql import functions as F
from pyspark.sql.types import *


# bronze to silver function
def bronze_to_silver(bronze_path: str, silver_path: str, schema:str, partition:str, file_type:str):
    spark = create_delta_lake_session('bronze_to_silver')
    spark.conf.set('spark.sql.sources.partitionOverwriteMode', 'dynamic')  
    
    if file_type=='csv':         
    
        # Create df
        df = (spark.read.option("delimiter", ";") 
                        .option("header", True)
                        .option('encoding', 'ISO-8859-1') 
                        .option('dateFormat', 'dd-MM-yyyy')
                        .schema(schema)
                        .csv(bronze_path))     
        
        # write df to parquet
        df.write.parquet(path=silver_path, mode="overwrite", partitionBy=partition)     
        
        spark.stop()
        
    else:
        print('Error: wrong file type!')