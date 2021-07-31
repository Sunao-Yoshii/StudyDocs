# FP やろうぜ FP (Fuctional Programming)

---

# そもそも FP ってなんやねん？

---

# そもそも FP ってなんやねん？
# 関数が第一級オブジェクトである言語のことです。（超狭義ではそういうことになってます）

---

# 第一級オブジェクト？

---

# 第一級オブジェクト？
# 要するに変数や返値にできることです。

---

# で？

---

# で？
# カリー化とか、高階関数とか作れます

---

# カリー化？食べ物か？
# 引数を分割して渡せます。

---

# カリー化の例

```scala
def plusName(familyName: String)(personalName: String) = {
  familyName + personalName
}

// 吉井 牧意
val fullName = plusName("吉井")("牧意")
```

---

# これの何がうれしいねん？
# 返すものが関数なので、変数に入れておけます

---

# カリー化の例

部分的に初期化しといて使いまわせます。


```scala
val withName = plusName("吉井")

// 吉井 牧意
val fullName1 = withName("牧意");
// 吉井 温
val fullName1 = withName("温");
```

関数を変数に入れれる(第一級オブジェクトだ)からできる手段ですね。

---

# Java で似たようなコード

```java
Function<String, String> addPlus(String familyName) {
  return (personalName) -> familyName + personalName;
}

// 吉井 温
String fullName = plusName("吉井").apply("温");
```

Java だろ関数を返せないので、あくまで「似たような」コードです。  
Function はインターフェースですね。

---

# んじゃ高階関数て？
# 関数を return する関数です。

---

# 例えば

さっき見たと思いますが

```scala
def plusName(familyName: String)(personalName: String) = {
  familyName + personalName
}

// withName には文字列一つを受け取る関数が入ります
val withName = plusName("吉井")
```

なので、これも高階関数です。

---

# Java って関数型？


```java
Function<String, String> addPlus(String familyName) {
  return (personalName) -> familyName + personalName;
}
```

# 誤解を承知して言えば、疑似的に関数型っぽいとは言えます。

---

# なんかハッキリしないね？

---

# 真面目に関数型とか言い出すと、さらに色んな単語が出てくるんです。

* 参照透過性
* 純粋関数
* 副作用
* 遅延評価


---

# じゃぁ関数型言語ってそれ全部守らないとダメなの？

---

# いいえ、関数型言語でも副作用書けるものはものとかいくらでもあります。
# JavaScript も関数型なんですよ？
# 理由は、「関数が第一級オブジェクト」だからです。

---

# じゃぁ Java が関数型言語といわないのって…
# 関数型っぽく書けても、return してるのが、Function 型のオブジェクトだからです。

```java
// 内部的にこうコンパイルされています
Function<String, String> addPlus(String familyName) {
  return new Function<String, String> {
    String apply(String personalName) {
      return familyName + personalName;
    }
}
```

---

# つまり

関数型言語を名乗るには

* 関数を return したり、変数に突っ込んだりできなければならない。
* しかも、言語仕様として関数がオブジェクトでなければならない。
  * 関数自体がオブジェクトであるべきで、Java のようにFunction のインスタンス返すとかは微妙に違う。
  * C# の Delegate は厳密には関数への参照（ポインタ）なので、これも関数が引数へ入っているのとは違う。

---

# 終わり

関数型を貴方は理解した。  
単純で、しかも強力な概念をどう応用するだろうか？  
オブジェクト指向にはデザインパターンがある、関数型のデザインパターンを考えるのはあなただ。