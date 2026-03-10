# tools/vector_store.py
import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ※神ルール3により、Pythonコード内にAPIキーは直書きしません。
# langgraph等の内部処理が、自動的に .env の GEMINI_API_KEY を読み込みます。

def get_vector_store():
    """
    Chromaベクトルデータベースのインスタンスを生成・取得する関数
    """
    try:
        # 【修正箇所】Geminiの最新の埋め込みモデル（text-embedding-004）に変更
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        
        # データベースの保存先ディレクトリ（ローカルに chroma_db フォルダが自動作成されます）
        persist_directory = "./chroma_db"
        
        # Chromaインスタンスの作成
        vector_store = Chroma(
            collection_name="cyber_detective_knowledge",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        return vector_store
    except Exception as e:
        # 神ルール2: 堅牢なエラーハンドリング
        print(f"❌ [VectorDB] データベースの初期化に失敗しました: {e}")
        raise e

def add_text_to_db(text: str, source_url: str):
    """
    長文テキストを分割（チャンク化）してベクトルDBに保存する関数
    """
    try:
        if not text:
            print("⚠️ [VectorDB] 保存するテキストが空です。")
            return

        # 1. チャンク化（テキストを適切なサイズに分割する処理）
        # ※AIが文脈を失わないよう、500文字で区切りつつ、前後の50文字をあえて重複（オーバーラップ）させます
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_text(text)
        
        vector_store = get_vector_store()
        
        # 2. メタデータの付与（どこから取得した情報かを記録）
        metadatas = [{"source": source_url} for _ in chunks]
        
        # 3. データベースへの保存
        vector_store.add_texts(texts=chunks, metadatas=metadatas)
        
        print(f"💾 [VectorDB]: {len(chunks)}個のチャンクに分割し、ChromaDBに記憶しました。")
        
    except Exception as e:
        print(f"❌ [VectorDB] データの保存中にエラーが発生しました: {e}")

def search_similar_texts(query: str, k: int = 2):
    """
    質問（query）に対して、意味が近いテキストをデータベースから検索して返す関数
    """
    try:
        vector_store = get_vector_store()
        
        # セマンティック検索（意味検索）の実行
        # k=2 は「最も意味が近い上位2つのチャンクを返す」という指定です
        results = vector_store.similarity_search(query, k=k)
        
        print(f"🔍 [VectorDB]: '{query}' に関する関連記憶を{len(results)}件抽出しました。")
        return [doc.page_content for doc in results]
        
    except Exception as e:
        print(f"❌ [VectorDB] 検索中にエラーが発生しました: {e}")
        return []