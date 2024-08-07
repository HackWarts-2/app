import weaviate
from weaviate.classes.init import Auth
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import Filter
from weaviate.classes.config import Configure, Property, DataType, Tokenization
import weaviate.classes as wvc
import os

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)

