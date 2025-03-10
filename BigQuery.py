#pip install --upgrade google-cloud-bigquery
import os
from google.cloud import bigquery

# Set the environment variable correctly
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Cloud_service.json'

# Initialize the BigQuery client
client = bigquery.Client()

# Define the query
sql_query = """
WITH MonthlySales AS (
  SELECT 
    DATE_TRUNC(b.`Date`, MONTH) AS `Month_Start`, 
    SUM(b.`Retail Volume`) AS `Total_Retail_Volume_2024`
  FROM DS_sales_data.billing_data b
  WHERE b.`Date` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
  GROUP BY `Month_Start`
), 
PreviousYearSales AS (
  SELECT 
    DATE_TRUNC(b.`Date`, MONTH) AS `Month_Start`, 
    SUM(b.`Retail Volume`) AS `Total_Retail_Volume_2023`
  FROM DS_sales_data.billing_data b
  WHERE b.`Date` BETWEEN DATE('2023-04-01') AND DATE('2024-03-31')
  GROUP BY `Month_Start`
) 
SELECT 
  ms.`Month_Start`, 
  ms.`Total_Retail_Volume_2024`, 
  COALESCE(pys.`Total_Retail_Volume_2023`, 0) AS `Total_Retail_Volume_2023`, 
  (ms.`Total_Retail_Volume_2024` - COALESCE(pys.`Total_Retail_Volume_2023`, 0)) AS `Difference`, 
  SAFE_DIVIDE((ms.`Total_Retail_Volume_2024` - COALESCE(pys.`Total_Retail_Volume_2023`, 0)), 
               COALESCE(pys.`Total_Retail_Volume_2023`, 1)) * 100 AS `Growth_Percentage`
FROM MonthlySales ms 
LEFT JOIN PreviousYearSales pys 
ON ms.`Month_Start` = pys.`Month_Start`
ORDER BY ms.`Month_Start`;
"""
query_job = client.query(sql_query)
results = query_job.result()

# Print the results
for row in results:
    print(row)





