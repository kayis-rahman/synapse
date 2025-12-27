import asyncio

from rag.vectorstore import VectorStore
from rag.embedding import EmbeddingService


async def test_vectorstore():
    print("Testing VectorStore...")
    store = VectorStore(":memory:")
    
    docs = ["Test document 1", "Test document 2"]
    vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadata = [{"source": "test1"}, {"source": "test2"}]
    
    store.add(docs, vectors, metadata)
    
    if len(store.docs) == 2 and len(store.vectors) == 2 and len(store.metadata) == 2:
        print("VectorStore test passed!")
        return True
    else:
        print("FAIL: VectorStore test failed")
        return False


async def main():
    print("Testing RAG Core Components")
    print("=" * 60)
    print()
    
    try:
        await test_vectorstore()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
