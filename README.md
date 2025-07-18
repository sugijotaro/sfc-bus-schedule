# SFC Bus Schedule API

慶應義塾大学 湘南藤沢キャンパス(SFC)と、電車最寄駅である湘南台駅の間を運行するバスの時刻表を、APIライクに利用できる形式で提供するプロジェクトです。

## 特徴

- **シンプルなデータ管理**: YAMLとCSVファイルで時刻表を管理
  - YAML: バス路線の基本情報（停留所、経由地など）
  - CSV: 時刻表データ
- **自動JSON生成**: 管理用ファイルから自動的にJSONを生成
- **コントリビューションしやすさ**: プログラミングの知識がなくても時刻表の更新が可能

## データ構造

### ルート情報 (YAML)
`config/routes.yaml`に以下の情報を管理:
- 路線名
- 行き先
- 経由地
- 停留所情報
- 時刻表CSVファイルのパス

### 時刻表データ (CSV)
各路線の時刻表をCSVファイルで管理:
- 平日
- 土曜日
- 日曜日・祝日

### 生成されるJSON

#### 路線別JSON (`data/v1/route/`)
各路線の詳細情報と時刻表を提供します。

例: `sho19_from_saturday.json`
```json
{
  "route_id": "sho19",
  "path_id": "sho19_from",
  "name": "湘南台駅西口行",
  "origin": "慶応大学",
  "destination": "湘南台駅西口",
  "via": "宮原・慶応大学",
  "stops": [
    {
      "name": "慶応大学",
      "cumulative_time": 0
    },
    // ... その他の停留所
  ],
  "timetable": [
    {
      "time": 7,
      "minute": 18
    },
    // ... その他の時刻
  ]
}
```

#### フラットJSON (`data/v1/flat/`)
各バス便の詳細情報を提供します。停留所ごとの到着時刻も含まれます。

例: `from_sfc_saturday.json`
```json
[
  {
    "id": "sho190718",
    "time": 7,
    "minute": 18,
    "scheduleType": "saturday",
    "routeCode": "sho19",
    "routeName": "湘19",
    "name": "湘南台駅西口行",
    "origin": "慶応大学",
    "destination": "湘南台駅西口",
    "via": "宮原・慶応大学",
    "metadata": {
      "stops": [
        {
          "name": "慶応大学",
          "cumulative_time": 0,
          "arrival": {
            "time": 7,
            "minute": 18
          }
        },
        // ... その他の停留所と到着時刻
      ]
    }
  },
  // ... その他のバス便
]
```

### 臨時ダイヤの情報 (YAML)
`config/special_schedules.yaml`で特定の日付に適用する臨時ダイヤを管理します。

- `date`: 臨時ダイヤを適用する日付 (YYYY-MM-DD)
- `description`: 臨時ダイヤの説明（例：オープンキャンパスダイヤ）
- `type`: 臨時ダイヤのユニークID
- `routes`: その日に運行する路線情報（`routes.yaml`と同じ形式）

#### 臨時ダイヤのメタデータ (`data/v1/special_schedules.json`)
適用されるすべての臨時ダイヤの情報を一覧で提供します。クライアント側はまずこのファイルを参照し、当日に適用される臨時ダイヤがあるか確認します。
```json
[
  {
    "date": "2025-07-05",
    "description": "慶應義塾大学湘南藤沢キャンパス「七夕祭」開催に伴う臨時便の運行および起終点の変更",
    "type": "special_20250705"
  }
]
```

#### 臨時ダイヤの時刻表JSON (`data/v1/special/{type}/`)
臨時ダイヤが適用される日は、専用ディレクトリ内に時刻表JSONが生成されます。
- `to_sfc.json`: SFC行きの全便
- `from_sfc.json`: SFC発の全便

例: `data/v1/special/special_20250705/to_sfc.json`

## APIの利用方法

生成されたJSONは以下のURLで直接アクセス可能です：

### 通常ダイヤ
- 路線別JSON: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/route/{route_id}_{direction}_{schedule_type}.json`
  - 例: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/route/sho19_from_saturday.json`

- フラットJSON: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/flat/{direction}_{schedule_type}.json`
  - 例: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/flat/from_sfc_saturday.json`

### 臨時ダイヤ
- 臨時ダイヤメタデータ: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/special_schedules.json`
- 臨時ダイヤ時刻表: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/special/{type}/{direction}_sfc.json`
  - 例: `https://sugijotaro.github.io/sfc-bus-schedule/data/v1/special/special_20250705/to_sfc.json`

これらのURLに直接アクセスすることで、JSONデータを取得できます。CORSも有効になっているため、Webアプリケーションから直接利用可能です。

## ブランチ構成

- `main`: 安定版のリリースブランチ
- `develop`: 開発用ブランチ
- `feature/*`: 新機能開発用ブランチ
- `hotfix/*`: 緊急バグ修正用ブランチ

## コントリビューション方法

1. 時刻表の更新
   - 該当するCSVファイルを編集
   - 時刻の追加・修正は簡単なCSV編集で可能

2. 路線情報の更新
   - `config/routes.yaml`を編集
   - 新しい停留所の追加や経路変更を反映

3. 新しい路線の追加
   - 新しいYAMLエントリの追加
   - 対応するCSVファイルの作成

## 使用方法

1. リポジトリのクローン
```bash
git clone https://github.com/sugijotaro/sfc-bus-schedule.git
```

2. JSONの生成
```bash
python generate_json_v1.py
```

## ライセンス

MIT License

## コントリビュータ

[コントリビュータ一覧](CONTRIBUTORS.md) 