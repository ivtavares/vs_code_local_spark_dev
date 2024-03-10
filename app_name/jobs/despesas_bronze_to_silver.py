from app_name.configs.spark_helper import create_delta_lake_session
from pyspark.sql import functions as F


# variable path
bronze_despesas_path = "s3://bronze/despesas/despesas-2023.csv"
silver_despesas_path = "s3://silver/despesas/"


# bronze to silver function
def despesas_bronze_to_silver(bronze_path: str, silver_path: str):
    spark = create_delta_lake_session('auditoria')
    spark.conf.set('spark.sql.sources.partitionOverwriteMode', 'dynamic')
    
    # Create df
    despesas_df = (spark.read.option("delimiter", ";") 
                             .option("header", True)
                             .option('encoding', 'ISO-8859-1') 
                             .csv(bronze_path))
    
    # Change Schema
    despesas_df_01 = despesas_df.select(F.col('id_despesa_detalhe')  
                                       ,F.col('ano_exercicio').cast('int') 
                                       ,F.col('ds_municipio')  
                                       ,F.col('codigo_municipio_ibge').cast('int')  
                                       ,F.col('ds_orgao')
                                       ,F.col('mes_referencia').cast('int') 
                                       ,F.col('mes_ref_extenso') 
                                       ,F.col('tp_despesa')
                                       ,F.col('nr_empenho') 
                                       ,F.col('tp_identificador_despesa') 
                                       ,F.col('nr_identificador_despesa').cast('bigint') 
                                       ,F.col('ds_despesa')
                                       ,F.to_date('dt_emissao_despesa', 'dd/MM/yyyy').alias('dt_emissao_despesa')
                                       ,F.regexp_replace(F.col('vl_despesa'), ",", ".").cast('decimal(9,2)').alias('vl_despesa') 
                                       ,F.col('ds_funcao_governo')       
                                       ,F.col('ds_subfuncao_governo')       
                                       ,F.col('cd_programa').cast('int')        
                                       ,F.col('ds_programa')       
                                       ,F.col('cd_acao').cast('int')  
                                       ,F.col('ds_fonte_recurso')        
                                       ,F.col('ds_cd_aplicacao_fixo')        
                                       ,F.col('ds_modalidade_lic')        
                                       ,F.col('ds_elemento')        
                                       ,F.col('historico_despesa'))    
    
    # write df to parquet
    despesas_df_01.write.parquet(path=silver_path, mode="overwrite", partitionBy="ano_exercicio")
    
    spark.stop()
    
    
if __name__ == '__main__':
    despesas_bronze_to_silver(bronze_despesas_path, silver_despesas_path)

