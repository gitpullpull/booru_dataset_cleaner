import os
import glob
import json

# ここにクリーニングしたいフォルダのディレクトリを書いてください

dir_path = r"D:\hoge"


# JSON パスをカレントディレクトリに設定
json_dir_path = "." 

# 指定されたディレクトリ内のテキストとキャプションファイルを検索
text_files = glob.glob(os.path.join(dir_path, "*.[tT][xX][tT]")) + glob.glob(os.path.join(dir_path, "*.[cC][aA][pP][tT][iI][oO][nN]"))

# 外部のJSONファイルからキーワードを読み込み、現在のディレクトリ内を検索
keywords_file_path = os.path.join(json_dir_path, 'keywords.json')
with open(keywords_file_path, 'r') as f:
    keywords = json.load(f)

# キーワードリストから空文字列を削除
keywords = [keyword for keyword in keywords if keyword]

# キーワードマッチングのためのフラグを "and" または "or" に設定
flag = "or"  # いずれかのキーワードが一致したら削除
deleted_files = []

for text_file in text_files:
    with open(text_file, 'r') as f:
        contents = f.read()
    
    # フラグに基づいてファイルがキーワードにマッチするかチェック
    match = False
    if flag == "and" and all(keyword in contents for keyword in keywords):
        match = True
    elif flag == "or" and any(keyword in contents for keyword in keywords):
        match = True
    
    # マッチが見つかった場合、該当する全ファイルを削除リストに追加
    if match:
        base_name = os.path.splitext(text_file)[0]
        matching_files = glob.glob(base_name + ".*")
        first_tag = contents.split(',', 1)[0] if contents else ""
        
        deleted_files.extend([{"file_path": file, "file_name": os.path.basename(file), "first_tag": first_tag} for file in matching_files])

        # 実際にファイルを削除する場所
        for file in matching_files:
             os.remove(file)

# 削除されたファイルのリストをJSONに保存、現在のディレクトリに保存
json_file_path = os.path.join(json_dir_path, 'deleted_files.json')
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
else:
    data = []

data.append({"keywords": keywords, "deleted_files": deleted_files})

with open(json_file_path, 'w') as f:
    json.dump(data, f, indent=4)
