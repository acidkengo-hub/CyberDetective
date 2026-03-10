# agents/researcher.py
import urllib.parse
from core.state import AgentState
from playwright.sync_api import sync_playwright
from tools.vector_store import add_text_to_db

def research_node(state: AgentState):
    """
    Playwrightを用いてWeb検索を行い、実データを収集してChromaに保存するエージェント
    """
    topic = state.get("research_topic", "")
    print(f"🕵️ [Researcher]: Playwrightを起動し、『{topic}』についてWeb検索を実行中...")
    
    # 【修正】Bot対策が非常に厳しい検索エンジンを避け、Yahoo! JAPAN検索を使用する
    encoded_topic = urllib.parse.quote(topic)
    url = f"https://search.yahoo.co.jp/search?p={encoded_topic}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # User-Agentの偽装と、日本からのアクセスであることを明示（locale設定）
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="ja-JP"
            )
            page = context.new_page()
            
            page.goto(url, timeout=30000)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000)
            
            # Yahoo検索結果のテキストを抽出
            full_text = page.locator("body").inner_text()
            
            browser.close()
            print("   -> 検索結果のデータ抽出に成功しました！")
            
            # 取得した実データをChroma（ベクトルDB）に記憶させる
            add_text_to_db(text=full_text, source_url=url)
            
            return {"raw_data": [f"【保存完了】: {url} からの検索結果を記憶しました。"]}
            
    except Exception as e:
        print(f"❌ [Researcher] スクレイピングまたはDB保存中にエラーが発生しました: {e}")
        return {"raw_data": ["データの取得・保存に失敗しました。"]}