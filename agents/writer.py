# agents/writer.py
from core.state import AgentState

def write_node(state: AgentState):
    """
    収集された生データを読み込み、最終レポートを執筆するエージェント（のモック）
    """
    print("✍️ [Writer]: 生データを整理し、最終レポートを執筆中...")
    raw_data = state.get("raw_data", [])
    
    # 収集した生データを箇条書きにまとめるモック処理
    data_text = "\n".join([f"- {data}" for data in raw_data])
    
    dummy_report = f"# 最終調査レポート\n\n## 収集されたデータ\n{data_text}\n\n## 結論\nこれはモックによるテストレポートです。"
    
    return {"final_report": dummy_report}