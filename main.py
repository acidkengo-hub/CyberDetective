# main.py
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from core.state import AgentState

# 各担当エージェント（関数）をインポート
from agents.planner import plan_node
from agents.researcher import research_node
from agents.writer import write_node

# 【重要】アプリ起動時に .env ファイルから環境変数（APIキー等）を安全に読み込む
load_dotenv()

def build_graph():
    """
    AIエージェントたちの業務ワークフローを構築する関数
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("Planner", plan_node)
    workflow.add_node("Researcher", research_node)
    workflow.add_node("Writer", write_node)

    workflow.add_edge(START, "Planner")
    workflow.add_edge("Planner", "Researcher")
    workflow.add_edge("Researcher", "Writer")
    workflow.add_edge("Writer", END)

    app = workflow.compile()
    return app

if __name__ == "__main__":
    print("🚀 電脳探偵局AIエージェンシーを起動します...\n")
    
    app = build_graph()
    
    initial_state = {"research_topic": "正宗白鳥と自然主義文学に関する最新の評価"}
    
    print(f"🎯 調査テーマ: {initial_state['research_topic']}\n")
    
    result = app.invoke(initial_state)
    
    print("\n✅ 全エージェントの処理が完了しました！")
    print("=" * 40)
    print(result["final_report"])
    print("=" * 40)