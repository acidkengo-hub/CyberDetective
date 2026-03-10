# agents/writer.py
import os
from core.state import AgentState
from tools.vector_store import search_similar_texts
from langchain_google_genai import ChatGoogleGenerativeAI

def write_node(state: AgentState):
    """
    記憶庫（Chroma）から意味検索で情報を引き出し、Geminiで最終レポートを執筆するエージェント
    """
    print("✍️ [Writer]: ベクトルDBから関連情報を検索し、Geminiで最終レポートを執筆中...")
    topic = state.get("research_topic", "テーマなし")
    
    try:
        # 1. RAGの「R（Retrieval: 検索）」: 調査テーマに関連する記憶をChromaから引き出す
        # 文学研究のように文脈が細かく重要な場合、関連度の高い上位3件（k=3）のチャンクを抽出します
        retrieved_docs = search_similar_texts(query=topic, k=3)
        
        if not retrieved_docs:
            print("⚠️ [Writer] 関連する記憶が見つかりませんでした。")
            context_text = "関連情報なし"
        else:
            context_text = "\n\n".join(retrieved_docs)
            print(f"   -> {len(retrieved_docs)}件の関連記憶をプロンプトに注入します。")
        
        # 2. RAGの「AG（Augmented Generation: 拡張生成）」: Geminiに指示を出して執筆させる
        # .envからAPIキーを自動で読み込みます
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        
        prompt = f"""
        あなたは優秀なリサーチャー兼ライターです。
        以下の【参考情報】のみに基づいて、【調査テーマ】に関する詳細なレポートをマークダウン形式で作成してください。
        もし参考情報に答えがない場合は、推測で語らず「情報が不足している」と正直に記載してください。
        
        【調査テーマ】: {topic}
        
        【参考情報】:
        {context_text}
        """
        
        # Gemini APIを呼び出してテキスト生成
        response = llm.invoke(prompt)
        
        # 生成されたレポートを共有バインダーに綴じる
        return {"final_report": response.content}
        
    except Exception as e:
        # 堅牢なエラーハンドリング
        print(f"❌ [Writer] レポートの生成中にエラーが発生しました: {e}")
        return {"final_report": f"エラーによりレポートが生成できませんでした。\n詳細: {e}"}