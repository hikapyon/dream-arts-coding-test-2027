import sys

class LongestPathSolver:
    """
    最長片道きっぷの旅（最長経路問題）を解くクラス
    アルゴリズム: 深さ優先探索 (DFS) + バックトラッキング
    """
    def __init__(self):
        # グラフデータ: { 始点ID: [(終点ID, 距離), ...] } の隣接リスト形式
        self.graph = {}
        # 発見された最長距離
        self.max_distance = -1.0
        # 発見された最長経路のリスト
        self.best_path = []

    def parse_input(self):
        """
        標準入力からデータを読み込み、グラフを構築するメソッド。
        - カンマ区切りのデータ (始点, 終点, 距離) を解析
        - 空行（Enterのみ）またはファイルの終わり(EOF)で入力を終了
        """
        while True:
            try:
                # 1行ずつ読み込む
                line = sys.stdin.readline()
                
                # データがなくなる(EOF) か、空行(Enterのみ)なら終了
                if not line or line.strip() == "":
                    break
                
                # カンマで分割して数値に変換
                parts = line.split(',')
                u = int(parts[0].strip())   # 始点
                v = int(parts[1].strip())   # 終点
                dist = float(parts[2].strip()) # 距離

                # グラフに追加（始点 u から 終点 v へ距離 dist）
                if u not in self.graph:
                    self.graph[u] = []
                self.graph[u].append((v, dist))
                
                # 終点 v も、後で「始点」として探索する可能性があるのでキーを作っておく
                if v not in self.graph:
                    self.graph[v] = []
                
                #print(self.graph)  # デバッグ用: 現在のグラフ状態を表示
            except ValueError:
                # 無効な行（空行など）はスキップ
                continue
        

    def solve(self):
        """
        すべての点を始点として試し、全体の最長経路を求めるメインメソッド
        """
        # グラフに存在するすべての駅IDを取得
        all_nodes = list(self.graph.keys())
        
        # すべての駅を「出発点」と仮定して探索を実行 
        for start_node in all_nodes:
            # dfs(現在地, 現在の累積距離, 経路履歴, 訪問済みセット, 最初の出発点)
            self.dfs(
                current_node=start_node, 
                current_dist=0.0, 
                path=[start_node], 
                visited={start_node}, 
                original_start=start_node
            )
        #print(self.max_distance, file=sys.stderr)  # デバッグ用: 最長距離を標準エラー出力に表示

        return self.best_path

    def dfs(self, current_node, current_dist, path, visited, original_start):
        """
        深さ優先探索 (DFS) を行う再帰関数
        - current_node: 今いる駅
        - current_dist: ここまでの合計距離
        - path: 通ってきた駅のリスト
        - visited: 今のルートで既に通った駅（再訪禁止用）
        - original_start: 今回の旅の出発駅（閉路判定用）
        """
        
        # 1. 最長記録の更新チェック
        # 行き止まりでなくても、通るたびにその時点での距離を評価する
        if current_dist > self.max_distance:
            self.max_distance = current_dist
            self.best_path = list(path) # リストをコピーして保存

        # 2. 次の移動先の探索
        if current_node in self.graph:
            for neighbor, weight in self.graph[current_node]:
                
                # パターンA: まだ通っていない駅へ進む場合（通常移動）
                # ルール: 同じ点を2回通ることはできない 
                if neighbor not in visited:
                    # 状態を進める
                    visited.add(neighbor)
                    path.append(neighbor)
                    
                    # 再帰呼び出し（さらに奥へ進む）
                    self.dfs(neighbor, current_dist + weight, path, visited, original_start)
                    
                    # バックトラッキング（探索から戻ってきたら状態を戻す）
                    # これにより、別の分岐ルートの探索が可能になる
                    path.pop()
                    visited.remove(neighbor)

                # パターンB: 出発点に戻ってきた場合（一周してゴール）
                # ルール: 始点と終点を同じ点にしても構わない 
                elif neighbor == original_start:
                    final_dist = current_dist + weight
                    final_path = path + [neighbor]
                    
                    # 記録更新チェック
                    if final_dist > self.max_distance:
                        self.max_distance = final_dist
                        self.best_path = final_path
                    
                    # 始点に戻ったらそれ以上先へは進めないので、このルートはここで終了

if __name__ == "__main__":
    # LongestPathSolverのインスタンスを作成
    solver = LongestPathSolver()
    
    # データの読み込み
    solver.parse_input()
    
    # 計算実行
    result_path = solver.solve()
    
    # 結果出力: IDを改行区切りで表示 
    for node in result_path:
        print(node)