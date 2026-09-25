# Gemini Voice Studio Lite

Gemini APIの音声生成（Text-to-Speech / Speech Generation）機能を活用し、入力したテキストから自然な音声を生成・再生・WAV保存できるシンプルなWebUIアプリケーションです。

## 主な特徴

- 多彩なプリセット音声の選択
  - Puck: 親しみやすく軽快なトーン（中音域）
  - Charon: 落ち着きと深みのある低音トーン
  - Kore: 明瞭で自然なトーン（中高音域）
  - Fenrir: 力強く芯のあるトーン
  - Aoede: クリアで聞き取りやすいトーン
- スタイル・トーンの自然言語指定
  - 「明るく元気なトーンで」「落ち着いたニュースキャスター風に」「絵本朗読のように優しく」など、自然言語のプロンプトで声のニュアンスを自在にコントロール可能。
- リアルタイム試聴とWAVダウンロード
  - 生成された音声データをブラウザ上で即座にプレビュー再生し、非可逆圧縮のない標準WAV形式でローカルに保存可能。
- 生成履歴の管理
  - セッション中に生成した過去の音声をリスト形式で一覧・再試聴可能。
- 柔軟なAPIキー設定
  - `.env` ファイルによる永続設定、および画面上（サイドバー）からの直接入力の両方に対応。

## 必要要件

- Python 3.10 以上
- Google AI Studio の APIキー

## セットアップ手順

### 1. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定（任意）

プロジェクトルートの `.env.example` をコピーして `.env` を作成し、APIキーを記入します。
（アプリ起動後に画面上のサイドバーから直接入力することも可能です）

```bash
cp .env.example .env
```

`.env` 内の記述例:
```env
GEMINI_API_KEY=あなたのGemini_APIキー
```

### 3. アプリケーションの起動

以下のコマンドを実行してStreamlitサーバーを起動します。

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501` でアプリが利用可能になります。

## ファイル構成

- `app.py`: StreamlitによるUI画面と操作ロジック
- `tts_service.py`: Gemini API呼び出しおよびPCMからWAVヘッダー付与・変換ロジック
- `requirements.txt`: 必要なPythonパッケージ一覧
- `.env.example`: 環境変数設定テンプレート
- `.gitignore`: Git除外設定ファイル
- `README.md`: 本ドキュメント

## ライセンス

MIT License
