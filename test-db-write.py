import lancedb
import getpass
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector

db = lancedb.connect("/tmp/db")
registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("openai").create(name="text-embedding-3-small")

class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()

# table = db.create_table("words", schema=Words, mode ="overwrite")
# table.add(
#     [
#         {"text": "hello world"},
#         {"text": "goodbye world"}
#     ]
#     )
table = db.open_table("words")
query = "hi"
actual = table.search(query).limit(1).to_pydantic(Words)[0]
print(actual.text)