# agents/writer.py
import os
from core.state import AgentState
from tools.vector_store import search_similar_texts
from langchain_google_genai import ChatGoogleGenerativeAI

def write_node(state: AgentState):
    """
    記憶庫（Chroma）から意味検索で情報を引き出し、洗練されたプロンプトで最終レポートを執筆するエージェント
    """
    print("✍️ [Writer]: ベクトルDBから関連情報を検索し、Geminiで最終レポートを執筆中...")
    topic = state.get("research_topic", "テーマなし")
    
    try:
        # 1. RAGの「R（Retrieval: 検索）」
        retrieved_docs = search_similar_texts(query=topic, k=3)
        
        if not retrieved_docs:
            print("⚠️ [Writer] 関連する記憶が見つかりませんでした。")
            context_text = "関連情報なし"
        else:
            context_text = "\n\n".join(retrieved_docs)
            print(f"   -> {len(retrieved_docs)}件の関連記憶をプロンプトに注入します。")
        
        # 2. RAGの「AG（Augmented Generation: 拡張生成）」
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        
        # 【修正】ユーザー考案のプロフェッショナルなプロンプトを適用
        prompt = f"""
# Role
あなたは卓越した分析力を持つリサーチャー兼プロフェッショナルなライターです。
提供された文脈から事実を正確に抽出し、論理的で読みやすいレポートを構築します。

# Rules
1. 厳格な情報制限: 以下の【参考情報】に記載されている事実のみを使用して執筆してください。自身の事前知識による推測や補完は厳禁です。
2. 不足情報の明示: 【調査テーマ】（特に「最新の〇〇」などの要求）に対して、参考情報内に該当する記載が全くない、あるいは部分的にしか分からない場合は、「提供された情報内では〇〇に関する詳細は確認できません」と明確かつ客観的に記載してください。
3. 構造化された出力: 視認性を高めるため、以下の【出力フォーマット】に従い、マークダウン形式で見出しや箇条書きを活用して出力してください。

# 出力フォーマット
## 1. 調査サマリー
（調査テーマに対する結論や全体的な概要を2〜3行で簡潔に記載）

## 2. 詳細報告
（参考情報を論理的に整理し、具体的に記述）

## 3. 情報の限界・不足項目
（調査テーマに対して、参考情報からは判明しなかった要素や不足している観点があれば記載。すべて網羅されている場合は「特になし」で可）

---
【調査テーマ】: {topic}

【参考情報】:
{context_text}
"""
        
        response = llm.invoke(prompt)
        
        return {"final_report": response.content}
        
    except Exception as e:
        print(f"❌ [Writer] レポートの生成中にエラーが発生しました: {e}")
        return {"final_report": f"エラーによりレポートが生成できませんでした。\n詳細: {e}"}