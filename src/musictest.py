import os
import glob

# 実行中のスクリプトの絶対パスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 一つ下のディレクトリのパスを指定（ここでは'mp3'という名前のディレクトリ）
mp3_dir = os.path.join(script_dir, 'mp3')

# mp3ディレクトリ内の全てのMP3ファイルを検索
mp3_files = glob.glob(os.path.join(mp3_dir, '*.mp3'))

# ファイル名のリストを取得（パスからファイル名のみを抽出）
mp3_file_names = [os.path.basename(mp3) for mp3 in mp3_files]

# 結果を表示
print(mp3_file_names)
