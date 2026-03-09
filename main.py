# main.py
from langgraph.graph import StateGraph, START, END
from core.state import AgentState

# 各担当エージェント（関数）をインポート
from agents.planner import plan_node
from agents.researcher import research_node
from agents.writer import write_node

def build_graph():
    """
    AIエージェントたちの業務ワークフローを構築する関数
    """
    # 1. 共有バインダー（State）を持ったワークフローを初期化
    workflow = StateGraph(AgentState)

    # 2. メンバーを現場監督（ワークフロー）に登録
    workflow.add_node("Planner", plan_node)
    workflow.add_node("Researcher", research_node)
    workflow.add_node("Writer", write_node)

    # 3. 作業の順番（バトンパスの経路：エッジ）を定義
    workflow.add_edge(START, "Planner")        # スタート -> プランナーへ
    workflow.add_edge("Planner", "Researcher") # プランナー -> リサーチャーへ
    workflow.add_edge("Researcher", "Writer")  # リサーチャー -> ライターへ
    workflow.add_edge("Writer", END)           # ライター -> 終了

    # 4. グラフをコンパイル（実行可能な状態に組み立てる）
    app = workflow.compile()
    return app

if __name__ == "__main__":
    print("🚀 電脳探偵局AIエージェンシーを起動します...\n")
    
    # 現場監督（グラフ）の呼び出し
    app = build_graph()
    
    # 最初のユーザー入力（Stateの初期値）
    # ※今回はテストとして、具体的な文学研究のテーマを設定してみます
    initial_state = {"research_topic": "正宗白鳥と自然主義文学に関する最新の評価"}
    
    # ワークフローの実行開始（invoke）
    print(f"🎯 調査テーマ: {initial_state['research_topic']}\n")
    
    # エージェントたちが合議しながらStateを更新していく
    result = app.invoke(initial_state)
    
    # 最終結果の出力
    print("\n✅ 全エージェントの処理が完了しました！")
    print("=" * 40)
    print(result["final_report"])
    print("=" * 40)