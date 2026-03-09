# agents/researcher.py
from core.state import AgentState

def research_node(state: AgentState):
    """
    計画書に基づいて、Web等から生データを収集するエージェント（のモック）
    """
    print("🕵️ [Researcher]: 計画書に基づき、ダミーの生データを収集中...")
    plan = state.get("plan", "")
    
    # 将来的にはPlaywrightでスクレイピングしますが、今回はダミーの検索結果を返します
    # Stateで `operator.add` を指定したので、リスト形式で返すと自動的に既存のリストに追記（Append）されます
    dummy_data = [
        "ダミーデータ1: 〇〇という概念は1980年代に普及し始めました。",
        "ダミーデータ2: 最新の調査では、約60%のユーザーが〇〇を支持しています。"
    ]
    
    return {"raw_data": dummy_data}