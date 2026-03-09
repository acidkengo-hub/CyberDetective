# agents/planner.py
from core.state import AgentState

def plan_node(state: AgentState):
    """
    ユーザーの調査テーマを受け取り、調査計画を立てるエージェント（のモック）
    """
    print("🧠 [Planner]: 調査テーマを確認し、計画を立案中...")
    topic = state.get("research_topic", "テーマなし")
    
    # 将来的にはここでGeminiに計画を立案させますが、今回は固定のダミーテキストを返します
    dummy_plan = f"【計画書】\n1. '{topic}' に関するWikipediaの要約を取得\n2. 関連する最新ニュースを3件検索\n3. 情報を統合してレポート化"
    
    # 更新したい状態（State）のキーと値を辞書で返す
    return {"plan": dummy_plan}