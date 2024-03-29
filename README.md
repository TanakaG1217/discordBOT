# Discord Bot概要

このプロジェクトは、OpenAI APIを活用したDiscord Botの実装例です。Discord上で自然言語処理を利用したインタラクションを提供し、音楽再生、画像処理応答、およびカスタムコマンドによる様々な機能をサポートします。

## 特徴

- OpenAI APIを使用してテキストベースの質問に答える
- Discordチャンネル内で音楽を再生
- アップロードされた画像に基づいてレスポンスを生成
- 特定のコマンドに基づいて動的にファイルを管理

## 必要条件

- Python 3.8 以上
- discord.py
- openai
- ffmpeg
- asyncio, glob, shutil, subprocess ライブラリ

## セットアップ

追加予定


## 使用方法

Discord上で以下のコマンドを使用:
- `!hello` - ボットが挨拶を返します。
- `!gpt` - OpenAI APIを使用して質問に答えます。
- `!music` - 利用可能な音楽ファイルのリストを表示します。
- `!secret` - シークレットモードで音楽を再生します。
- `!time` - タイマーをセットして時間になるとボイスチャンネルで音楽を再生します。
- その他多数のカスタムコマンド。
