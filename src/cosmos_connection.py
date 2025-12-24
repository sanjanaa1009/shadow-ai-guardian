from gremlin_python.driver import client, serializer

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Use them in your code
COSMOS_ENDPOINT = os.getenv('AZURE_COSMOS_ENDPOINT')
COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')
DATABASE = os.getenv('AZURE_DATABASE_NAME')
GRAPH = os.getenv('AZURE_GRAPH_NAME')

gremlin_client = client.Client(
    COSMOS_ENDPOINT,
    'g',
    username=f"/dbs/{DATABASE}/colls/{GRAPH}",
    password=COSMOS_KEY,
    message_serializer=serializer.GraphSONSerializersV2d0()
)

def run_query(query):
    return gremlin_client.submitAsync(query).result().all().result()
