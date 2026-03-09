# core/state.py
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    """
    複数のAIエージェント間で共有される「状態（State）」の定義
    これが全員の共有ホワイトボードになります。
    """
    
    # ユーザーが入力する最初の調査テーマ（例：「特定のイデオロギーを含む児童文学の歴史」など）
    research_topic: str
    
    # プランナーAIが作成する「どのように調査を進めるか」の計画書
    plan: str
    
    # リサーチャーAIが収集した生データ（WebやベクトルDBから取得したテキスト）
    # ※Annotatedとoperator.addを使うことで、データが上書きされず「どんどん追記（リスト結合）される」設定になります
    raw_data: Annotated[list[str], operator.add]
    
    # ライターAIが最終的に生成する構造化されたマークダウンレポート
    final_report: str