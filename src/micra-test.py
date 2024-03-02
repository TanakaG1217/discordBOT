import subprocess

# シェルスクリプトを実行し、標準出力を受け取る
result = subprocess.run('cd /home/tanaka/minecraft-server/Ars3 && ./dsc_stop.sh', shell=True, capture_output=True, text=True)

# 標準出力の内容を表示
print("The shell script said:", result.stdout.strip())
