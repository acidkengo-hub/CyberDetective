# agents/researcher.py
from core.state import AgentState
from playwright.sync_api import sync_playwright

def research_node(state: AgentState):
    """
    Playwrightを用いて、実際にWebページからデータを収集するエージェント
    """
    print("🕵️ [Researcher]: Playwrightを起動し、Webから実データを収集中...")
    
    # 今回はテストとして、特定のWikipediaページから情報を抽出します
    url = "https://ja.wikipedia.org/wiki/正宗白鳥"
    
    try:
        # Playwrightを同期モードで起動
        with sync_playwright() as p:
            # ブラウザを立ち上げる（headless=Trueで見えない裏側で動かします）
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 対象のURLへアクセス（タイムアウトは10秒に設定）
            page.goto(url, timeout=10000)
            
            # ページ内の最初の段落（<p>タグ）のテキストを取得する
            # ※ここでWebスクレイピングのDOM待機・抽出スキルが活きます
            first_paragraph = page.locator("p").first.inner_text()
            
            # ブラウザを閉じる
            browser.close()
            
            print(f"   -> データの抽出に成功しました！")
            
            # 取得した実データを共有バインダー（State）に追記する
            return {"raw_data": [f"【Web抽出データ】: {first_paragraph}"]}
            
    except Exception as e:
        # 先ほどの「神ルール2：堅牢なエラーハンドリング」の実践です
        print(f"❌ [Researcher] スクレイピング中にエラーが発生しました: {e}")
        return {"raw_data": ["データの取得に失敗しました。"]}