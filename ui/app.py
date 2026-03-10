# ui/app.py
import customtkinter as ctk
import threading
import os
from dotenv import load_dotenv

# API通信を廃止し、脳みそ（LangGraph）の設計図を直接インポート
from main import build_graph

# 神ルール3: 環境変数の読み込み
load_dotenv()

# UIの全体テーマ設定
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CyberDetectiveUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("電脳探偵局 - 完全ローカル独立版")
        self.geometry("800x700")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_label = ctk.CTkLabel(
            self, text="電脳探偵局システム", font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.topic_entry = ctk.CTkEntry(
            self, placeholder_text="調査したいテーマを入力してください",
            height=40, font=("Helvetica", 14)
        )
        self.topic_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.search_button = ctk.CTkButton(
            self, text="リサーチ開始", height=40, font=("Helvetica", 14, "bold"),
            command=self.start_research
        )
        self.search_button.grid(row=2, column=0, padx=20, pady=10)

        self.result_textbox = ctk.CTkTextbox(
            self, font=("Helvetica", 14), wrap="word"
        )
        self.result_textbox.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # 【重要】アプリ起動時に、自身の内部にAIのワークフロー（脳みそ）を構築して保持する
        try:
            self.agent_workflow = build_graph()
        except Exception as e:
            print(f"初期化エラー: {e}")
            self.agent_workflow = None

    def start_research(self):
        topic = self.topic_entry.get()
        if not topic:
            self.result_textbox.insert("1.0", "⚠️ 調査テーマを入力してください。\n")
            return
        
        if not self.agent_workflow:
            self.result_textbox.insert("1.0", "⚠️ AIエンジンの初期化に失敗しています。\n")
            return

        self.search_button.configure(state="disabled", text="リサーチ中...（画面はフリーズしません）")
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"「{topic}」について調査を開始しました...\n裏側でAIエージェントが自律的にWeb検索と執筆を行っています。\n完了までしばらくお待ちください。\n\n")

        # API通信ではなく、直接ローカルのAIを実行するスレッドを立ち上げる
        threading.Thread(target=self.run_local_research, args=(topic,), daemon=True).start()

    def run_local_research(self, topic):
        """
        別スレッドでAIエージェントを直接実行する関数
        """
        try:
            # LangGraphの初期状態をセットして実行
            initial_state = {"research_topic": topic}
            result = self.agent_workflow.invoke(initial_state)
            
            report = result.get("final_report", "レポートが生成されませんでした。")
            
            # メインスレッド（UI）に結果を渡して安全に更新
            self.after(0, self.update_ui_with_result, report)
            
        except Exception as e:
            # 神ルール2: 堅牢なエラーハンドリング
            error_msg = f"❌ ローカルAIの実行中にエラーが発生しました。\n詳細: {e}"
            self.after(0, self.update_ui_with_result, error_msg)

    def update_ui_with_result(self, report_text):
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", report_text)
        self.search_button.configure(state="normal", text="リサーチ開始")

if __name__ == "__main__":
    app = CyberDetectiveUI()
    app.mainloop()