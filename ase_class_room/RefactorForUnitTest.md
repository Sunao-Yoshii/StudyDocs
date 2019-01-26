<!-- $theme: gaia -->

# テストできる構造入門

## よっしぃ

---
<!-- page_number: true -->

## お品書き

* まずはモックの使い方を知る
* テストできない構造を知る:依存性の排除
* テストしにくい構造を知る:副作用の局所化
* テストしやすい構造を知る:メソッド機能の極小化
* 最後に

---

#### ここで示すサンプルは、
##### [github](https://github.com/Sunao-Yoshii/StudyDocs/blob/feature/RefactorExample/ase_class_room/RefactorExample/src/test/java/net/white/azalea/IOUtilsTest.java) の feature/RefactorExample ブランチに格納している


---

### まずはモックの使い方を知る

---

### まずはモックの使い方を知る

オブジェクトとして機能を切り出し、そのメソッドに依存すれば、その呼び元のメソッドはテストしやすいだろうか？
例えばこんなのだ。

```java
    public int readInteger() throws IOException {
        while(true) {
            try {
                return Integer.parseInt(reader.readLine());
            } catch (NumberFormatException e) {
                this.out.println("整数を入力してください。");
            }
        }
    }
```

---

### まずはモックの使い方を知る

```java
    public int readInteger() throws IOException {
        while(true) {
            try {
                return Integer.parseInt(reader.readLine());
            } catch (NumberFormatException e) {
                this.out.println("整数を入力してください。");
            }
        }
    }
```

* reader の挙動までテストするのはしんどいよ。
* out とか呼び出し確認どうするの？

なんてことになる。そこで、これをモックアップに置き換える。

---

### まずはモックの使い方を知る

**モックアップ:** 実物とほぼ同様に似せて作られた模型のことである。[weblioより](https://www.weblio.jp/content/%E3%83%A2%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)

つまり、こう言った物を偽物に置き換える事で、外側から制御してやれば、

---

### まずはモックの使い方を知る

```java
    public int readInteger() throws IOException {
        while(true) {
            try {
                return Integer.parseInt(reader.readLine());
            } catch (NumberFormatException e) {
                this.out.println("整数を入力してください。");
            }
        }
    }
```

1. 事前に大量の設定をせずとも、reader.readLine動作を指定できる。
2. out.println が意図した通りに呼ばれるか検証できる。

---

### まずはモックの使い方を知る

モックを作る例：①モックオブジェクトを作って置き換える。

```java
    IOUtils ioUtils;
    BufferedReader brMock;
    PrintStream psMock;

    @Before
    public void setUp() {
        // モックを作成
        this.brMock = mock(BufferedReader.class);
        this.psMock = mock(PrintStream.class);
        this.ioUtils = new IOUtils(brMock, psMock);
    }
```


---

### まずはモックの使い方を知る

モックを作る例：②モックを呼び出した時の応答を定義する。

```java
// 呼び出し設定
// 初回は "Not a num.", ２回目が "64", 3回目は 128
when(this.brMock.readLine())
       .thenReturn("Not a num.", "64", "128");
```


---

### まずはモックの使い方を知る

モックを作る例: ③モックが意図した回数、意図した引数で呼び出された事を確認する。

```java
        // 実行したら
        int value = this.ioUtils.readInteger();

        // 整数入力を促される
        verify(this.psMock, times(1))
                .println("整数を入力してください。");
```

ということが出来るようになります。  
大抵の言語で似たようなものがあるので、探して覚えておくとテストが捗ります。

---

#### テストできない構造を知る
### 依存性の排除

---

#### テストできない構造を知る:依存性の排除

まず次のようなコードはテストできない。

```java
BufferedReader reader
    = new BufferedReader(new InputStreamReader(System.in));
try {
    System.out.println("ジュースの選択");
    for (int i = 0; i < products.size(); i++) {
        Product p = products.get(i);
        System.out.println(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
    }
```

理由: `System` という静的なオブジェクトに依存されたら、その動作を制御/キャプチャできない。
**①静的(static)のものはテストしにくい**  
**②その場で new してるとモックにできない**

---

#### テストできない構造を知る:依存性の排除

なので、切り離しを考える。  
コンストラクタで、それらの依存を貰うようにする。

```java
    private final BufferedReader reader;
    private final PrintStream out;
    private final List<Product> products;

    public VendingMachine(BufferedReader reader, PrintStream printer, List<Product> products) {
        this.reader = reader;
        this.out = printer;
        this.products = products;
    }
```


---

#### テストできない構造を知る:依存性の排除

先ほどテストできなかった所も、依存を書き換える。

```java
    try {
        this.out.println("ジュースの選択");
        for (int i = 0; i < products.size(); i++) {
            Product p = products.get(i);
            this.out.println(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
        }
```

こうすれば、テスト時にはモックで置き換えることができる。

知見: **依存は切り離す**

---

#### テストしにくい構造を知る:副作用の局所化

---

#### テストしにくい構造を知る:副作用の局所化

*副作用: メソッドの外に対して、影響を与えること。*

具体的には以下の事を言います。

1. 引数オブジェクトの中身を書き換えること。
2. 自オブジェクトの状態を変更すること。

これがどう言った意味を持つかというと

---

#### テストしにくい構造を知る:副作用の局所化

```java
    try {
        this.out.println("ジュースの選択");
        for (int i = 0; i < products.size(); i++) {
            Product p = products.get(i);
            this.out.println(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
        }
```

この処理を実行すると、`out` の状態が書き換わります。テストに置き換えると、

**最終的な状態が複雑で、どんな期待値(TEST OK条件)になるか予測しにくい。**

---

#### テストしにくい構造を知る:副作用の局所化

まずは、標準(コンソール画面)入出力は、一つのパッケージにして、クラス化してしまう。

```java
class IOUtils {
    private final BufferedReader reader;
    private final PrintStream out;
    public IOUtils(BufferedReader reader, PrintStream out) {
        this.reader = reader;
        this.out = out;
    }
    public void println(String v) {
        this.out.println(v);
    }
    public int readInteger() throws IOException {
        // 尺の理由で省略.整数が入力されるまで入力を促す.
    }
}
```

---

#### テストしにくい構造を知る:副作用の排除

次に、書き込む処理と、文字列の作成を分離する。

```java
public String getProductsString() { // 文字列生成のみ
    List<String> display = new ArrayList<>();
    for (int i = 0; i < products.size(); i++) {
        Product p = products.get(i);
        display.add(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
    }
    return String.join("\n", display);
}
```
```java
this.ioUtils.println("ジュースの選択");// ioUtils をモックに
this.ioUtils.println(this.getProductsString());
```

知見: **副作用を分離すれば、部分部分はやりやすい。**

---

##### テストしやすい構造を知る:メソッド機能の極小化

---

##### テストしやすい構造を知る:メソッド機能の極小化

やれば直ぐにわかるが、メソッド内で複数の処理をしていると、テスト側が煩雑化する。  

```java
this.ioUtils.println("コインを入れてね(使用可能: 500, 100, 50, 10)");
while (n < selected.getPrice()) {
    int coin = this.ioUtils.readInteger();
    if (List.of(500, 100, 50, 10).contains(coin)) {
        n += coin;
    } else {
        this.ioUtils.println("その硬貨は使えません");
    }
}
```

1. 数値入力の妥当性判定
2. 投入金額合計の計算

---

##### テストしやすい構造を知る:メソッド機能の極小化

これも段階分離する。まずは入力制限だけを行う。
```java
public int selectNumber(
    List<Integer> selectable,
    String error) throws IOException {
    while (true) {
        int input = this.ioUtils.readInteger();
        if (selectable.contains(input)) {
            return input;
        }
        this.ioUtils.println(error);
    }
}
```

この部分だけなら単独でテストを書いてもさして苦にならない。


---

##### テストしやすい構造を知る:メソッド機能の極小化

次はそれを利用して、規定金額まで入金させる部分。

```java
private final List<Integer> coins =
    List.of(500, 100, 50, 10);
public int payment(int price) throws IOException {
    int insertedCoin = 0;
    while (insertedCoin < price) {
        int coin = this.selectNumber(
                coins, "その硬貨は使えません");
        insertedCoin += coin;
    }
    return insertedCoin;
}
```

知見: **メソッドの仕様は小さいほど書きやすい。**

---

## 最後に

テストしやすくなるための基本的な設計の勘所を記載してみた。

* オブジェクト依存は、置き換え可能なようにしよう。
* オブジェクト変数は極力書き換えない、書き換えるならそうした処理は局所化する。
* メソッドの機能は小さく単純なほどテストしやすい。