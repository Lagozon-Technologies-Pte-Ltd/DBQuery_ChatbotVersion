examples = [
 {
    "input": "show total retail volume in financial year 2024",
    "query": """
        SELECT 
            SUM(b.`Retail Volume`) AS `Total Retail Volume`
        FROM DS_sales_data.billing_data b
        WHERE b.`Date` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31');   
        """,
    "contexts": " | ".join([
        "Table: DS_sales_data.billing_data",
        "Columns: Date, Retail Volume",
        "Description: This table contains vehicle retail volume data categorized by date."
    ])
},
 {
    "input": "get monthly test drives for 2024",
    "query": """
        SELECT 
            FORMAT_DATE('%B %Y', b.`Date`) AS `Month`, 
            SUM(b.`Test Drive`) AS `Total Test Drives`
        FROM DS_sales_data.billing_data b
        WHERE b.`Date` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
        GROUP BY `Month`
        ORDER BY MIN(b.`Date`);
    """,
    "contexts": " | ".join([
        "Table: DS_sales_data.billing_data",
        "Columns: Date, Test Drive",
        "Description: This table records test drive data, including the number of test drives conducted."
    ])
},
 {
    "input": "show total bookings and billings for model XUV700",
    "query": """
        SELECT 
            p.`Model Name`, 
            SUM(b.`Open Booking`) AS `Total Bookings`, 
            SUM(b.`Billing Volume`) AS `Total Billings`
        FROM DS_sales_data.billing_data b
        JOIN DS_sales_data.product_hierarchy p ON b.`Model ID` = p.`Model ID`
        WHERE LOWER(p.`Model Name`) = LOWER('XUV700') 
        AND b.`Date` BETWEEN DATE('2024-04-01') AND DATE('2025-03-31')
        GROUP BY p.`Model Name`;
        """,
    "contexts": " | ".join([
        "Table: DS_sales_data.billing_data, DS_sales_data.product_hierarchy",
        "Columns: Model ID, Open Booking, Billing Volume, Model Name",
        "Description: This query retrieves the total bookings and billings for a given vehicle model."
    ])
}



]



from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings


def get_example_selector():
    """
    Returns a SemanticSimilarityExampleSelector object initialized with the given examples.
    """
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,  # Ensure `examples` is a list of dictionaries
        OpenAIEmbeddings(),
        Chroma,
        k=1,
        input_keys=["input"],  # Ensure that 'input' is a key in the examples
    )

    return example_selector

