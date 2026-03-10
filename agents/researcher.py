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
    
    encoded_topic = urllib.parse.quote(topic)
    url = f"https://www.bing.com/search?q={encoded_topic}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(url, timeout=30000)
            
            # 【修正箇所】 無限ロードを避けるため、DOM読み込み完了でOKとする
            page.wait_for_load_state("domcontentloaded")
            # 念のため、JavaScriptによるテキストの描画を2秒だけ確実待機する
            page.wait_for_timeout(2000)
            
            paragraphs = page.locator("body").all_inner_texts()
            full_text = "\n".join(paragraphs)
            
            browser.close()
            print("   -> 検索結果のデータ抽出に成功しました！")
            
            add_text_to_db(text=full_text, source_url=url)
            
            return {"raw_data": [f"【保存完了】: {url} からの検索結果を記憶しました。"]}
            
    except Exception as e:
        print(f"❌ [Researcher] スクレイピングまたはDB保存中にエラーが発生しました: {e}")
        return {"raw_data": ["データの取得・保存に失敗しました。"]}