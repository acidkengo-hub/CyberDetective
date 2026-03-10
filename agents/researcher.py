# agents/researcher.py
from core.state import AgentState
from playwright.sync_api import sync_playwright
from tools.vector_store import add_text_to_db

def research_node(state: AgentState):
    """
    Playwrightを用いてWebから実データを収集し、Chroma（記憶庫）に保存するエージェント
    """
    print("🕵️ [Researcher]: Playwrightを起動し、Webから実データを収集中...")
    topic = state.get("research_topic", "")
    
    url = "https://ja.wikipedia.org/wiki/正宗白鳥"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)
            
            # ページ内のすべての段落（<p>タグ）のテキストを結合して取得する
            paragraphs = page.locator("p").all_inner_texts()
            full_text = "\n".join(paragraphs)
            
            browser.close()
            print(f"   -> {len(paragraphs)}個の段落データの抽出に成功しました！")
            
            # 取得した大量の実データをChroma（ベクトルDB）にチャンク分割して記憶させる
            add_text_to_db(text=full_text, source_url=url)
            
            # Stateの更新（生データは重いためDBに入れ、バインダーにはログだけを残す）
            return {"raw_data": [f"【保存完了】: {url} からのデータをベクトルDBに記憶しました。"]}
            
    except Exception as e:
        # 堅牢なエラーハンドリング
        print(f"❌ [Researcher] スクレイピングまたはDB保存中にエラーが発生しました: {e}")
        return {"raw_data": ["データの取得・保存に失敗しました。"]}