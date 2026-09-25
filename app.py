"""
Gemini Voice Studio Lite - Main Streamlit Application
"""

import os
import datetime
from dotenv import load_dotenv
import streamlit as st
from tts_service import generate_speech, SUPPORTED_VOICES, DEFAULT_MODEL

# 環境変数の読み込み (.env)
load_dotenv()

st.set_page_config(
    page_title="Gemini Voice Studio Lite",
    page_icon="🎙️",
    layout="wide"
)

# カスタムCSS（見やすさとデザインの向上）
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1a73e8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .card {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 4px;
        background-color: #e8f0fe;
        color: #1967d2;
        margin-right: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if "history" not in st.session_state:
    st.session_state.history = []

if "text_input" not in st.session_state:
    st.session_state.text_input = "こんにちは。Gemini Voice Studio Liteへようこそ。自然な音声合成をお試しください。"

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 設定・環境")

    # APIキー設定
    env_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    api_key_input = st.text_input(
        "Gemini API キー",
        value=env_api_key,
        type="password",
        help="Google AI Studioで取得したAPIキーを入力してください。.envファイルにも保存可能です。"
    )

    st.divider()

    # モデル選択
    st.subheader("🤖 モデル設定")
    model_option = st.selectbox(
        "使用モデル",
        options=["gemini-2.5-flash", "gemini-2.0-flash"],
        index=0,
        help="通常は応答速度と品質に優れた gemini-2.5-flash を推奨します。"
    )

    st.divider()

    # 音声キャラクター選択
    st.subheader("🗣️ 声（Voice）の選択")
    voice_options = list(SUPPORTED_VOICES.keys())
    selected_voice = st.selectbox(
        "プリセット音声",
        options=voice_options,
        index=0,
        format_func=lambda v: f"{v} - {SUPPORTED_VOICES[v]}"
    )

    st.info(f"選択中: {selected_voice}\n特徴: {SUPPORTED_VOICES[selected_voice]}")

    st.divider()
    st.caption("Gemini Voice Studio Lite v1.0.0")


# メインコンテンツ
st.markdown('<div class="main-header">🎙️ Gemini Voice Studio Lite</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">テキストを入力し、声のトーンやスタイルを指定して自然な日本語音声を素早く生成・試聴・WAV保存できます。</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.subheader("1. 読み上げテキストの入力")

    # 例文サンプルボタン
    st.caption("例文サンプルをクリックして入力欄にセットできます:")
    sample_cols = st.columns(3)
    if sample_cols[0].button("👋 日常の挨拶"):
        st.session_state.text_input = "みなさん、おはようございます。今日も素晴らしい一日を過ごしていきましょう！"
    if sample_cols[1].button("📢 館内アナウンス"):
        st.session_state.text_input = "ご来館のお客様にご案内申し上げます。本日の営業時間は午後八時までとなっております。お忘れ物のないようお気をつけてお帰りください。"
    if sample_cols[2].button("📖 物語の朗読"):
        st.session_state.text_input = "むかしむかし、深い森の奥深くに、小さな時計塔がひっそりと佇んでいました。その時計は、夜空の星が満ちた時にだけ、美しい音色を響かせるのでした。"

    user_text = st.text_area(
        "読み上げ本文",
        value=st.session_state.text_input,
        height=160,
        placeholder="ここに読み上げさせたい日本語テキストを入力してください..."
    )
    char_count = len(user_text)
    st.caption(f"文字数: {char_count} 文字")

    st.subheader("2. 話し方・トーンの指示（スタイルプロンプト）")

    # トーンプリセット
    tone_preset = st.selectbox(
        "よく使うトーンのクイック選択",
        options=[
            "カスタム入力（自由入力）",
            "明るく元気で親しみやすいトーンで",
            "落ち着いていて上品で静かなトーンで",
            "ニュースキャスターのように明瞭で正確に",
            "優しく温かみのある絵本朗読風に",
            "ビジネス向けの信頼感のあるプレゼン風に"
        ],
        index=0
    )

    default_style = "" if tone_preset == "カスタム入力（自由入力）" else tone_preset
    style_instruction = st.text_input(
        "自然言語によるニュアンス指定（自由入力）",
        value=default_style,
        placeholder="例: 明るく楽しそうに、少し早めのテンポで話してください。"
    )

    st.write("")
    generate_btn = st.button("🚀 音声を生成する", type="primary", use_container_width=True)

with col2:
    st.subheader("3. 生成結果・プレビュー")

    if generate_btn:
        active_api_key = api_key_input.strip()
        if not active_api_key:
            st.error("Gemini APIキーを入力してください。左側のサイドバーで設定できます。")
        elif not user_text.strip():
            st.warning("読み上げるテキストを入力してください。")
        else:
            with st.spinner("Geminiが音声を生成中です。少々お待ちください..."):
                try:
                    wav_data, mime_type = generate_speech(
                        text=user_text,
                        voice_name=selected_voice,
                        style_instruction=style_instruction,
                        model_name=model_option,
                        api_key=active_api_key
                    )

                    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = f"gemini_voice_{selected_voice}_{now_str}.wav"

                    # 履歴に保存
                    history_item = {
                        "time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "text": user_text,
                        "voice": selected_voice,
                        "style": style_instruction or "指定なし",
                        "audio": wav_data,
                        "filename": file_name
                    }
                    st.session_state.history.insert(0, history_item)

                    st.success("音声の生成が完了しました！")

                except Exception as e:
                    st.error(f"音声生成中にエラーが発生しました:\n{str(e)}")

    # 最新の音声表示
    if st.session_state.history:
        latest = st.session_state.history[0]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<span class="badge">声: {latest["voice"]}</span><span class="badge">トーン: {latest["style"]}</span>', unsafe_allow_html=True)
        st.caption(f"生成時刻: {latest['time']}")
        st.audio(latest["audio"], format="audio/wav")

        st.download_button(
            label="💾 WAVファイルをダウンロード",
            data=latest["audio"],
            file_name=latest["filename"],
            mime="audio/wav",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("左側のフォームにテキストを入力し、「音声を生成する」ボタンを押すとここにプレビューとダウンロードリンクが表示されます。")

# 生成履歴セクション
if len(st.session_state.history) > 1:
    st.divider()
    st.subheader("📜 生成履歴（セッション中）")

    for idx, item in enumerate(st.session_state.history[1:], start=2):
        with st.expander(f"履歴 #{idx} [{item['time']}] 声: {item['voice']} - 「{item['text'][:30]}...」"):
            st.write(f"テキスト: {item['text']}")
            st.write(f"トーン指定: {item['style']}")
            st.audio(item["audio"], format="audio/wav")
            st.download_button(
                label=f"WAVを保存 ({item['filename']})",
                data=item["audio"],
                file_name=item["filename"],
                mime="audio/wav",
                key=f"dl_{idx}"
            )
