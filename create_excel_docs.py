"""
Gemini Voice Studio Lite - Excel 仕様書・計画書生成スクリプト
openpyxlを用いて洗練されたデザインのExcelドキュメントを生成する
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_documentation(output_path: str):
    wb = openpyxl.Workbook()
    # デフォルトシート削除準備
    default_sheet = wb.active

    # スタイル定義
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    sub_header_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    accent_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    zebra_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    font_title = Font(name="Yu Gothic", size=16, bold=True, color="1F497D")
    font_section = Font(name="Yu Gothic", size=12, bold=True, color="FFFFFF")
    font_header = Font(name="Yu Gothic", size=11, bold=True, color="FFFFFF")
    font_sub_header = Font(name="Yu Gothic", size=10, bold=True, color="1F497D")
    font_body = Font(name="Yu Gothic", size=10, color="000000")
    font_body_bold = Font(name="Yu Gothic", size=10, bold=True, color="000000")
    font_caption = Font(name="Yu Gothic", size=9, color="555555")

    thin_border_side = Side(border_style="thin", color="D9D9D9")
    table_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    thick_bottom = Border(bottom=Side(border_style="medium", color="1F497D"))

    # ----------------------------------------------------
    # シート1: 表紙・プロジェクト概要
    # ----------------------------------------------------
    ws1 = wb.create_sheet(title="表紙・プロジェクト概要")
    ws1.views.sheetView[0].showGridLines = True

    ws1.column_dimensions["A"].width = 4
    ws1.column_dimensions["B"].width = 24
    ws1.column_dimensions["C"].width = 50
    ws1.column_dimensions["D"].width = 20

    ws1["B2"] = "簡易Gemini TTSアプリ開発計画書・システム仕様書"
    ws1["B2"].font = font_title

    ws1["B3"] = "Gemini Voice Studio Lite プロジェクト総合ドキュメント"
    ws1["B3"].font = font_caption

    meta_info = [
        ("項目", "内容"),
        ("システム名称", "Gemini Voice Studio Lite"),
        ("バージョン", "1.1.0（完成版）"),
        ("作成日", "2026年9月25日"),
        ("開発組織", "Ban.Tai Education Design"),
        ("リポジトリ", "https://github.com/bantai-education-design/gemini-voice-studio-lite"),
        ("プロジェクト目的", "テキストを入力し、指定した声のトーンやスタイルで自然な日本語音声を高速生成・試聴・WAV保存・Excel管理できる直感的なデスクトップWebUIの提供。"),
        ("主要技術スタック", "Python 3.13, Streamlit, Google GenAI SDK (google-genai), openpyxl, pandas"),
        ("利用AIモデル", "Gemini 2.5 Flash / Gemini 2.0 Flash (Speech Generation対応)"),
        ("対応プラットフォーム", "Windows, macOS, Linux (Webブラウザ環境)"),
    ]

    start_row = 5
    for i, (k, v) in enumerate(meta_info):
        row = start_row + i
        ws1[f"B{row}"] = k
        ws1[f"C{row}"] = v
        if i == 0:
            ws1[f"B{row}"].fill = header_fill
            ws1[f"C{row}"].fill = header_fill
            ws1[f"B{row}"].font = font_header
            ws1[f"C{row}"].font = font_header
        else:
            ws1[f"B{row}"].fill = sub_header_fill
            ws1[f"B{row}"].font = font_body_bold
            ws1[f"C{row}"].font = font_body
            ws1[f"C{row}"].fill = white_fill if i % 2 == 1 else zebra_fill
        ws1[f"B{row}"].border = table_border
        ws1[f"C{row}"].border = table_border
        ws1[f"B{row}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws1[f"C{row}"].alignment = Alignment(vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # シート2: 機能要件一覧
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="機能要件定義")
    ws2.views.sheetView[0].showGridLines = True

    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 18
    ws2.column_dimensions["C"].width = 24
    ws2.column_dimensions["D"].width = 45
    ws2.column_dimensions["E"].width = 10
    ws2.column_dimensions["F"].width = 12

    ws2["A1"] = "機能要件一覧"
    ws2["A1"].font = font_title
    ws2.row_dimensions[1].height = 28

    headers2 = ["機能ID", "大分類", "機能名", "詳細仕様・要件", "重要度", "実装状態"]
    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = table_border
    ws2.row_dimensions[3].height = 24

    req_data = [
        ("REQ-01", "テキスト入力", "読み上げ本文入力", "任意の日本語・多言語テキストを入力可能なテキストエリアを提供。文字数を自動カウント表示。", "高", "完了"),
        ("REQ-02", "テキスト入力", "例文クイックセット", "日常挨拶、館内アナウンス、物語朗読の各プリセット文をワンクリックで入力欄に反映。", "中", "完了"),
        ("REQ-03", "音声設定", "プリセット音声選択", "Google AI Studioでサポートされている5種（Puck, Charon, Kore, Fenrir, Aoede）の選択UIを提供。", "高", "完了"),
        ("REQ-04", "音声設定", "トーン指示プロンプト", "「明るく元気に」「落ち着いた低音で」等の自然言語によるスタイル調整、およびクイックプリセット選択。", "高", "完了"),
        ("REQ-05", "音声生成", "Gemini Speech API連携", "google-genai SDKを用いてGemini APIにAUDIOモダリティリクエストを発行し、音声データを取得。", "高", "完了"),
        ("REQ-06", "音声変換", "PCM to WAV変換", "Geminiから返されるraw PCMストリーム（24kHz/16bit/Mono）にRIFFヘッダーを付与してWAVバイト列に変換。", "高", "完了"),
        ("REQ-07", "出力・再生", "ブラウザ試聴プレイヤー", "生成したWAV音声を画面上で即座に再生可能なオーディオコンポーネントを配置。", "高", "完了"),
        ("REQ-08", "出力・保存", "WAVダウンロード", "生成音声をファイル名付き（キャラクター名、タイムスタンプ含む）でローカルに保存可能。", "高", "完了"),
        ("REQ-09", "履歴管理", "セッション生成履歴", "過去に生成した音声をリスト化し、一覧表示、再試聴、個別ダウンロードを提供。", "中", "完了"),
        ("REQ-10", "データ連携", "Excelファイル出力", "セッション中の生成履歴データ（テキスト、音声、トーン、日時、サイズ等）をExcel形式で一括保存。", "中", "完了"),
        ("REQ-11", "セキュリティ", "APIキー安全管理", "サイドバーでの動的入力と、.envファイル経由の秘匿読み込みの両方に対応。.gitignoreで情報漏洩防止。", "高", "完了"),
        ("REQ-12", "バージョン管理", "GitHub連携", "Gitによる履歴管理およびGitHub公開リポジトリ（bantai-education-design/gemini-voice-studio-lite）への反映。", "高", "完了"),
    ]

    for r_idx, row_values in enumerate(req_data, 4):
        fill_color = zebra_fill if r_idx % 2 == 0 else white_fill
        ws2.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_values, 1):
            cell = ws2.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_body
            cell.fill = fill_color
            cell.border = table_border
            align_h = "center" if c_idx in [1, 5, 6] else "left"
            cell.alignment = Alignment(horizontal=align_h, vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # シート3: 画面・UI設計書
    # ----------------------------------------------------
    ws3 = wb.create_sheet(title="画面・UI設計")
    ws3.views.sheetView[0].showGridLines = True

    ws3.column_dimensions["A"].width = 12
    ws3.column_dimensions["B"].width = 20
    ws3.column_dimensions["C"].width = 22
    ws3.column_dimensions["D"].width = 48
    ws3.column_dimensions["E"].width = 25

    ws3["A1"] = "画面・UI設計書"
    ws3["A1"].font = font_title
    ws3.row_dimensions[1].height = 28

    headers3 = ["画面エリア", "コンポーネント名", "項目名", "UI仕様・挙動詳細", "設定値・バリデーション"]
    for col_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = table_border
    ws3.row_dimensions[3].height = 24

    ui_data = [
        ("サイドバー", "パスワード入力", "Gemini API キー", "Google AI StudioのAPIキーを入力。.envからの初期値自動補完あり。マスク表示。", "必須入力（未入力時エラー警告）"),
        ("サイドバー", "セレクトボックス", "使用モデル", "音声生成に対応したGeminiモデルを選択。", "gemini-2.5-flash（初期値）, gemini-2.0-flash"),
        ("サイドバー", "セレクトボックス", "プリセット音声", "声質キャラクターを選択。選択時に特徴説明文をガイドカードで表示。", "Puck, Charon, Kore, Fenrir, Aoede"),
        ("メイン（左列）", "ボタン群", "例文サンプル", "日常の挨拶、館内アナウンス、物語朗読をクリックするとテキストエリアに瞬時にセット。", "3種類のプリセットテキスト"),
        ("メイン（左列）", "テキストエリア", "読み上げ本文", "読み上げさせたい文章を入力。文字数をリアルタイムカウント表示。", "1000文字超の場合に警告メッセージ表示"),
        ("メイン（左列）", "セレクトボックス", "トーンのクイック選択", "明るく元気、落ち着いて、アナウンス風などの定型指示をワンクリック選択。", "選択内容が自由入力欄に同期反映"),
        ("メイン（左列）", "テキスト入力", "トーン自由入力", "自然言語で話し方のニュアンスを自由に指示。", "空欄時は標準の読み上げプロンプトを適用"),
        ("メイン（左列）", "実行ボタン", "音声を生成する", "APIへ非同期通信を行い音声を生成。生成中はローディングスピナーを表示。", "Primaryスタイルボタン"),
        ("メイン（右列）", "プレビューカード", "最新音声試聴", "直近で生成された音声をブラウザのHTML5オーディオで再生。", "再生、シーク、ボリューム調整可能"),
        ("メイン（右列）", "ダウンロードボタン", "WAVファイルを保存", "生成音声をWAV形式で即時ローカルダウンロード。", "MIME: audio/wav"),
        ("履歴タブ", "テーブル表示", "履歴データ一覧", "生成日時、キャラクター、トーン、文字数、サイズを一覧テーブル表示。", "pandas DataFrame連動"),
        ("履歴タブ", "エクスポートボタン", "Excel保存ボタン", "セッション内の全生成履歴をExcelファイル（.xlsx）としてダウンロード。", "MIME: application/vnd.openxmlformats..."),
        ("履歴タブ", "クリアボタン", "履歴クリアボタン", "セッション中の履歴データをリセット。", "確認後リセット実行"),
    ]

    for r_idx, row_values in enumerate(ui_data, 4):
        fill_color = zebra_fill if r_idx % 2 == 0 else white_fill
        ws3.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_values, 1):
            cell = ws3.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_body
            cell.fill = fill_color
            cell.border = table_border
            align_h = "center" if c_idx == 1 else "left"
            cell.alignment = Alignment(horizontal=align_h, vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # シート4: Gemini API・音声仕様
    # ----------------------------------------------------
    ws4 = wb.create_sheet(title="API・音声仕様")
    ws4.views.sheetView[0].showGridLines = True

    ws4.column_dimensions["A"].width = 16
    ws4.column_dimensions["B"].width = 24
    ws4.column_dimensions["C"].width = 26
    ws4.column_dimensions["D"].width = 46

    ws4["A1"] = "Gemini API・音声パラメータ仕様"
    ws4["A1"].font = font_title
    ws4.row_dimensions[1].height = 28

    headers4 = ["分類", "パラメータ名 / キャラクター", "設定値 / 型", "機能説明・特徴"]
    for col_idx, h in enumerate(headers4, 1):
        cell = ws4.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = table_border
    ws4.row_dimensions[3].height = 24

    voice_specs = [
        ("音声キャラクター", "Puck", "PrebuiltVoiceConfig", "親しみやすく軽快なトーン（中音域）。日常会話や対話型アシスタントに最適。"),
        ("音声キャラクター", "Charon", "PrebuiltVoiceConfig", "落ち着きと深みのある低音トーン。ニュース、学術解説、ドキュメンタリー朗読に最適。"),
        ("音声キャラクター", "Kore", "PrebuiltVoiceConfig", "明瞭で自然なトーン（中高音域）。案内ガイダンスや教材コンテンツに最適。"),
        ("音声キャラクター", "Fenrir", "PrebuiltVoiceConfig", "力強く芯のある男性的なトーン。物語のナレーションや重厚なプレゼンテーションに最適。"),
        ("音声キャラクター", "Aoede", "PrebuiltVoiceConfig", "クリアで透明感のある聞き取りやすいトーン。公共アナウンスや明るい解説に最適。"),
        ("API設定", "response_modalities", "['AUDIO']", "Geminiモデルからの応答として音声ストリームを明示的に指定。"),
        ("API設定", "speech_config", "SpeechConfig(voice_config=...)", "希望する音声キャラクター名を指定する設定構造体。"),
        ("音声フォーマット", "PCMサンプリングレート", "24000 Hz", "Gemini TTSの標準PCMサンプリング周波数（24kHz）。"),
        ("音声フォーマット", "ビット深度", "16 bit (2 bytes)", "リニアPCM標準解像度。"),
        ("音声フォーマット", "チャンネル数", "1 (モノラル)", "単一オーディオストリーム。"),
        ("音声変換", "RIFF WAVヘッダー", "waveモジュール付与", "ブラウザおよび主要プレイヤーで即座に互換性を持つ標準WAVコンテナにラッピング。"),
    ]

    for r_idx, row_values in enumerate(voice_specs, 4):
        fill_color = zebra_fill if r_idx % 2 == 0 else white_fill
        ws4.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_values, 1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_body
            cell.fill = fill_color
            cell.border = table_border
            align_h = "center" if c_idx == 1 else "left"
            cell.alignment = Alignment(horizontal=align_h, vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # シート5: テスト仕様書・検証結果
    # ----------------------------------------------------
    ws5 = wb.create_sheet(title="テスト仕様書・検証結果")
    ws5.views.sheetView[0].showGridLines = True

    ws5.column_dimensions["A"].width = 12
    ws5.column_dimensions["B"].width = 18
    ws5.column_dimensions["C"].width = 28
    ws5.column_dimensions["D"].width = 32
    ws5.column_dimensions["E"].width = 28
    ws5.column_dimensions["F"].width = 10

    ws5["A1"] = "テスト仕様書・検証結果一覧"
    ws5["A1"].font = font_title
    ws5.row_dimensions[1].height = 28

    headers5 = ["テストID", "テスト区分", "確認項目", "操作手順", "期待される結果", "判定"]
    for col_idx, h in enumerate(headers5, 1):
        cell = ws5.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = table_border
    ws5.row_dimensions[3].height = 24

    test_data = [
        ("TC-01", "構文・環境", "Python構文検証", "py_compileでapp.py, tts_service.pyを実行", "コンパイルエラーなしで正常終了すること", "合格"),
        ("TC-02", "SDK整合性", "google-genai型定義検証", "types.SpeechConfig等の属性存在確認", "該当フィールドが正常にロードされること", "合格"),
        ("TC-03", "UI初期表示", "画面起動検証", "streamlit run app.pyを実行", "サイドバーおよびメインコンポーネントが正常描画されること", "合格"),
        ("TC-04", "入力操作", "例文サンプルボタン動作", "各例文ボタンをクリック", "テキストエリアに該当文章が即時入力されること", "合格"),
        ("TC-05", "入力操作", "トーンプリセット動作", "トーンセレクトボックスを変更", "自然言語指定欄に選択したトーン文章が自動代入されること", "合格"),
        ("TC-06", "エラー系", "APIキー未入力テスト", "APIキー空欄の状態で生成ボタンを押下", "適切なエラー警告が表示され処理が中断すること", "合格"),
        ("TC-07", "エラー系", "本文空欄テスト", "本文空欄の状態で生成ボタンを押下", "警告メッセージが表示され無駄なAPI呼び出しが抑止されること", "合格"),
        ("TC-08", "音声変換", "PCMからWAVへの変換", "生PCMバイト列をpcm_to_wav関数に入力", "RIFFヘッダーが付与された正常なWAVデータが返ること", "合格"),
        ("TC-09", "ダウンロード", "WAVダウンロード動作", "生成後にWAVダウンロードボタンを押下", "指定したファイル名でローカル保存が可能なこと", "合格"),
        ("TC-10", "データ連携", "Excelエクスポート動作", "履歴画面でExcelダウンロードボタンを押下", "生成日時、文字数、トーンを含む.xlsxファイルが出力されること", "合格"),
        ("TC-11", "履歴操作", "履歴クリア動作", "履歴クリアボタンを押下", "セッション中の履歴が正常に消去され画面が更新されること", "合格"),
        ("TC-12", "バージョン管理", "GitHubプッシュ確認", "git statusおよびgh repo view確認", "mainブランチに正常にコミットが反映されていること", "合格"),
    ]

    for r_idx, row_values in enumerate(test_data, 4):
        fill_color = zebra_fill if r_idx % 2 == 0 else white_fill
        ws5.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_values, 1):
            cell = ws5.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_body
            cell.fill = fill_color
            cell.border = table_border
            align_h = "center" if c_idx in [1, 2, 6] else "left"
            cell.alignment = Alignment(horizontal=align_h, vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # シート6: WBS・開発工程進捗
    # ----------------------------------------------------
    ws6 = wb.create_sheet(title="WBS・開発工程")
    ws6.views.sheetView[0].showGridLines = True

    ws6.column_dimensions["A"].width = 10
    ws6.column_dimensions["B"].width = 16
    ws6.column_dimensions["C"].width = 28
    ws6.column_dimensions["D"].width = 14
    ws6.column_dimensions["E"].width = 12
    ws6.column_dimensions["F"].width = 30

    ws6["A1"] = "WBS・開発工程管理表"
    ws6["A1"].font = font_title
    ws6.row_dimensions[1].height = 28

    headers6 = ["WBS ID", "フェーズ", "タスク内容", "担当", "進捗率", "成果物"]
    for col_idx, h in enumerate(headers6, 1):
        cell = ws6.cell(row=3, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = table_border
    ws6.row_dimensions[3].height = 24

    wbs_data = [
        ("1.1", "要件定義", "アプリ概要および目的の策定", "設計", "100%", "開発計画書"),
        ("1.2", "要件定義", "主要機能要件・技術スタック選定", "設計", "100%", "要件定義書"),
        ("2.1", "環境構築", "Python環境およびGit/GitHub CLI確認", "開発", "100%", "環境構築完了"),
        ("2.2", "環境構築", "必要パッケージ導入 (google-genai, streamlit)", "開発", "100%", "requirements.txt"),
        ("2.3", "環境構築", "リポジトリ初期化および.gitignore設定", "開発", "100%", ".gitignore, .env.example"),
        ("3.1", "バックエンド", "Gemini Speech API呼び出しロジック実装", "開発", "100%", "tts_service.py"),
        ("3.2", "バックエンド", "PCMからWAVヘッダー付与・変換処理実装", "開発", "100%", "pcm_to_wav関数"),
        ("4.1", "フロントエンド", "Streamlit UI基本構造・サイドバー構築", "開発", "100%", "app.py"),
        ("4.2", "フロントエンド", "スタイル指定・例文プリセットUI実装", "開発", "100%", "トーン・例文機能"),
        ("4.3", "フロントエンド", "プレビュー試聴およびWAVダウンロード実装", "開発", "100%", "オーディオUI"),
        ("4.4", "機能拡張", "生成履歴管理およびExcelエクスポート機能", "開発", "100%", "Excel出力モジュール"),
        ("5.1", "テスト・検証", "構文検証およびAPIパラメータ整合性テスト", "検証", "100%", "テスト仕様書・合格"),
        ("5.2", "リリース", "GitHub公開リポジトリへのプッシュ", "運用", "100%", "GitHubリポジトリ"),
        ("5.3", "ドキュメント", "総合開発計画書・仕様書Excelファイル生成", "文書", "100%", "本Excelファイル"),
    ]

    for r_idx, row_values in enumerate(wbs_data, 4):
        fill_color = zebra_fill if r_idx % 2 == 0 else white_fill
        ws6.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_values, 1):
            cell = ws6.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_body
            cell.fill = fill_color
            cell.border = table_border
            align_h = "center" if c_idx in [1, 2, 4, 5] else "left"
            cell.alignment = Alignment(horizontal=align_h, vertical="center", wrap_text=True)

    # 初期シート削除
    if default_sheet in wb.worksheets:
        wb.remove(default_sheet)

    wb.save(output_path)
    print(f"Excelファイルを正常に保存しました: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\User\.gemini\antigravity\scratch\gemini-voice-studio-lite\Gemini_Voice_Studio_Lite_開発計画・仕様書.xlsx"
    build_excel_documentation(out_file)
