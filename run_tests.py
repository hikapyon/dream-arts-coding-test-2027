import subprocess
import glob
import os
import sys

def run_tests():
    # テスト対象のプログラムファイル名
    solver_script = "coding_test.py"
    
    # "test"で始まり".txt"で終わるファイル一覧を取得してソート
    test_files = sorted(glob.glob("tests/test*.txt"))

    if not test_files:
        print("テストファイル(test*.txt)が見つかりません。")
        return

    print(f"=== {len(test_files)}個のテストを実行します ===")

    for test_file in test_files:
        print(f"\n[実行中] {test_file} ...")
        
        try:
            # テストファイルを読み込む
            with open(test_file, 'r') as f:
                input_data = f.read()

            # 別プロセスで 実行し、標準入力を流し込む
            # Windows/Mac両対応のため sys.executable を使用
            result = subprocess.run(
                [sys.executable, solver_script],
                input=input_data,
                capture_output=True,
                text=True,
                encoding='utf-8' 
            )

            if result.returncode != 0:
                print(f"エラーが発生しました:\n{result.stderr}")
            else:
                # 結果の出力（最後の改行を除去して表示）
                output = result.stdout.strip()
                # 見やすくインデントして表示
                print("--- 出力結果 ---")
                print(output)
                
                # 簡単な検証（行数をカウント）
                lines = output.split('\n')
                print(f"-> 経路の長さ(点数): {len(lines)}")

        except Exception as e:
            print(f"実行中に例外が発生: {e}")

    print("\n=== 全テスト終了 ===")

if __name__ == "__main__":
    run_tests()