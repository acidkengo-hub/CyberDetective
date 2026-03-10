# api.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 既存のワークフロー構築関数を main.py からインポート
from main import build_graph

load_dotenv()

app = FastAPI(
    title="電脳探偵局 API",
    description="LangGraphベースの自律型リサーチAIエージェンシー",
    version="1.0.0"
)

agent_workflow = build_graph()

class ResearchRequest(BaseModel):
    topic: str

# 【修正箇所】 `async def` から `def` に変更し、FastAPIに別スレッドで実行させる
@app.post("/api/research")
def run_research(request: ResearchRequest):
    """
    外部から調査テーマを受け取り、LangGraphエージェントを実行してレポートを返すAPI
    """
    print(f"\n📡 [API] 外部からリサーチ要求を受信しました: {request.topic}")
    
    try:
        initial_state = {"research_topic": request.topic}
        
        # ワークフローの実行
        result = agent_workflow.invoke(initial_state)
        
        print("✅ [API] レポートの生成が完了し、クライアントへ返却します。")
        
        return {
            "status": "success",
            "topic": request.topic,
            "report": result.get("final_report", "レポートが生成されませんでした。")
        }
        
    except Exception as e:
        print(f"❌ [API] 実行中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail=str(e))