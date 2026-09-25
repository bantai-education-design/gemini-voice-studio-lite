"""
Gemini Voice Studio Lite - TTS Service Module
Gemini API (Speech Generation / Audio Output) を利用した音声生成ロジック
"""

import io
import re
import wave
import os
from typing import Optional, Tuple
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-2.5-flash"
SUPPORTED_VOICES = {
    "Puck": "親しみやすく軽快なトーン（中音域）",
    "Charon": "落ち着きと深みのある低音トーン",
    "Kore": "明瞭で自然なトーン（中高音域）",
    "Fenrir": "力強く芯のあるトーン",
    "Aoede": "クリアで聞き取りやすいトーン",
}

def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000, channels: int = 1, sampwidth: int = 2) -> bytes:
    """
    PCM生データに標準WAVヘッダーを付与してバイト列として返す
    """
    # 既にRIFFヘッダーがある場合はそのまま返す
    if pcm_data.startswith(b"RIFF"):
        return pcm_data

    wav_io = io.BytesIO()
    with wave.open(wav_io, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)
    return wav_io.getvalue()

def extract_sample_rate(mime_type: str, default_rate: int = 24000) -> int:
    """
    MIMEタイプ文字列（例: audio/pcm;rate=24000）からサンプリングレートを取得
    """
    match = re.search(r"rate=(\d+)", mime_type)
    if match:
        return int(match.group(1))
    return default_rate

def build_tts_prompt(text: str, style_instruction: str = "") -> str:
    """
    Geminiに余計な解説を挟ませず、指定のトーンで正確に読み上げさせるプロンプトを構築
    """
    cleaned_style = style_instruction.strip()
    cleaned_text = text.strip()

    if cleaned_style:
        return (
            "あなたはプロのナレーターです。\n"
            "以下の【話し方・トーン】の指示に従い、【読み上げ本文】に指定された文章のみを正確に発話してください。\n"
            "前置き、相づち、解説、後書き等の余計な言葉は一切出力せず、本文のみを音声で読み上げてください。\n\n"
            f"【話し方・トーン】\n{cleaned_style}\n\n"
            f"【読み上げ本文】\n{cleaned_text}"
        )
    else:
        return (
            "以下の【読み上げ本文】のみを、自然で聴き取りやすい日本語で正確に音声として読み上げてください。\n"
            "前置きや解説などは含めず、本文のみを発話してください。\n\n"
            f"【読み上げ本文】\n{cleaned_text}"
        )

def generate_speech(
    text: str,
    voice_name: str = "Puck",
    style_instruction: str = "",
    model_name: str = DEFAULT_MODEL,
    api_key: Optional[str] = None
) -> Tuple[bytes, str]:
    """
    Gemini APIを呼び出して音声を生成し、WAVバイト列とMIMEタイプを返す
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError("Gemini APIキーが設定されていません。サイドバーまたは.envファイルで設定してください。")

    client = genai.Client(api_key=key)
    prompt = build_tts_prompt(text, style_instruction)

    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        )
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

    audio_bytes = None
    mime_type = "audio/wav"

    if not response.candidates:
        raise RuntimeError("APIからの応答候補（candidates）が得られませんでした。")

    candidate = response.candidates[0]
    if candidate.content and candidate.content.parts:
        for part in candidate.content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                raw_data = part.inline_data.data
                part_mime = part.inline_data.mime_type or "audio/pcm"
                rate = extract_sample_rate(part_mime, 24000)
                audio_bytes = pcm_to_wav(raw_data, sample_rate=rate)
                mime_type = "audio/wav"
                break

    if not audio_bytes:
        raise RuntimeError("音声データを受信できませんでした。入力内容やモデル設定をご確認ください。")

    return audio_bytes, mime_type
