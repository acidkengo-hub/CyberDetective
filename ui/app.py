# ui/app.py
import customtkinter as ctk
import threading
import asyncio
import httpx

# UIの全体テーマ設定（モダンなダークモード）
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CyberDetectiveUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウの基本設定
        self.title("電脳探偵局 - AI Research Agency")
        self.geometry("800x700")
        
        # UIパーツの配置（グリッドレイアウト）
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. タイトルラベル
        self.title_label = ctk.CTkLabel(
            self, text="電脳探偵局システム", font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. 検索テーマ入力フィールド
        self.topic_entry = ctk.CTkEntry(
            self, placeholder_text="調査したいテーマを入力してください（例：正宗白鳥の自然主義における評価）",
            height=40, font=("Helvetica", 14)
        )
        self.topic_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # 3. リサーチ開始ボタン
        self.search_button = ctk.CTkButton(
            self, text="リサーチ開始", height=40, font=("Helvetica", 14, "bold"),
            command=self.start_research
        )
        self.search_button.grid(row=2, column=0, padx=20, pady=10)

        # 4. レポート表示用テキストボックス
        self.result_textbox = ctk.CTkTextbox(
            self, font=("Helvetica", 14), wrap="word"
        )
        self.result_textbox.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

    def start_research(self):
        """
        検索ボタンが押された時の処理
        """
        topic = self.topic_entry.get()
        if not topic:
            self.result_textbox.insert("1.0", "⚠️ 調査テーマを入力してください。\n")
            return

        # UIの状態を「処理中」に変更し、ボタンを無効化（連打防止）
        self.search_button.configure(state="disabled", text="リサーチ中...（画面はフリーズしません）")
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"「{topic}」について調査を開始しました...\n裏側でAIエージェントがWeb検索と執筆を行っています。\n完了まで30秒〜1分ほどお待ちください。\n\n")

        # 【超重要】UIをフリーズさせないため、API通信を「別のスレッド（裏方の作業員）」に任せる
        threading.Thread(target=self.run_async_api_call, args=(topic,), daemon=True).start()

    def run_async_api_call(self, topic):
        """
        別スレッドで実行される非同期通信の準備関数
        """
        # asyncioループを新しく作って非同期関数を呼び出す
        result = asyncio.run(self.fetch_report_from_api(topic))
        
        # 通信が終わったら、安全にメインのUIを更新する
        self.after(0, self.update_ui_with_result, result)

    async def fetch_report_from_api(self, topic):
        """
        FastAPIサーバーへ非同期でリクエストを送る関数
        """
        url = "http://127.0.0.1:8000/api/research"
        try:
            # タイムアウトを120秒（2分）と長めに設定（AIの思考時間を考慮）
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json={"topic": topic})
                response.raise_for_status() # エラーがあれば例外を投げる
                
                data = response.json()
                return data.get("report", "レポートが見つかりませんでした。")
                
        except Exception as e:
            # 神ルール2: 堅牢なエラーハンドリング
            return f"❌ サーバーとの通信中にエラーが発生しました。\nFastAPIサーバーが起動しているか確認してください。\n詳細: {e}"

    def update_ui_with_result(self, report_text):
        """
        取得したレポートを画面に表示し、ボタンを元に戻す処理
        """
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", report_text)
        self.search_button.configure(state="normal", text="リサーチ開始")

if __name__ == "__main__":
    app = CyberDetectiveUI()
    app.mainloop()