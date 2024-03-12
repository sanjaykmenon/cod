import lancedb
import getpass
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector

uri = "/tmp/db2"
db = lancedb.connect(uri)
table = db.open_table("words")
#table.create_fts_index("text")

print(db["words"].head())