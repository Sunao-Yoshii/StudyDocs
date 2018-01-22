ES2015(ES6) の基礎的な話
===

Author: azalea （Blog: [謎言語使いの徒然](http://white-azalea.hatenablog.jp/)）

---

## お品書き

1. ES2015 ってなんなん？
2. 機能の一覧
4. 使える環境って？
5. 新機能一覧
6. そして ES2016-2017 へ！

---
<!-- page_number: true -->

# ES2015 って何なん？
#### 〜JavaScript の正当進化〜

---

#### ES2015 って何なん？

始まりは、Google が Chrome にて実装した、JavaScript の高速な実行エンジン V8 エンジン。
その公開を受けて、「あれ？実はJavaScriptだけで色々できんじゃね？」と考えた人たちが、 NodeJs（JavaScript のコンソール実行環境）としたことに端を発します。

そして、それが公開され、人々は気づくようになりました。

**あれ？JavaScriptって何か言語仕様微妙じゃね？**

---

#### ES2015 って何なん？

そう、ブラウザとともに生まれて生きてきた JavaScript (正式には ECMAScript5)はあくまで汎用言語として機能が不足していたのです。

このままでは大規模な開発に耐えれない、そこで言語仕様の見直しが始まりました。

**ECMA Script6 の開発開始です**

---

#### ES2015 って何なん？

そして、2015 年に言語仕様の開発が始まり、それまでのバージョン番号 ES6 から正式に年号を含む [ES2015](http://www.ecma-international.org/ecma-262/6.0/index.html) として策定されました（[正式確定は 2017 年](http://www.ecma-international.org/ecma-262/6.0/index.html)）。

* ES5 (つまりそれまでの JavaScript)の機能を可能な限り引き継ぐこと。
* いくつかの新機能(include modules, class declarations, lexical block scoping, iterators and generators, promises for asynchronous programming, destructuring patterns, and proper tail calls）を含むこと。
* 基本型を拡張すること

などを含んだ大規模アップデートです。

---

# 使える環境って？

---

#### 使える環境って？

コレはレポートが Web 上に上がっています。

[http://kangax.github.io/compat-table/es6/](http://kangax.github.io/compat-table/es6/)

見た目の通りで、どのブラウザがどこまで対応したかが書いてあります。
ぶっちゃけ、最新の NodeJS なら全部対応していますが…

---

# 機能の一覧
#### -新機能目白押し-

---

### 機能の一覧

信じられるか？コレほどの数が一気に入ったんだぜ？

* include/export によるモジュール管理
* class によるクラス定義
* レキシカルスコープの変数
* デフォルト引数
* アロー関数
* 可変長引数
* 配列展開
* テンプレート文字列
* イテレータとジェネレータ
* promises を使った非同期処理
* 末尾再帰最適化

---

### 機能の一覧(include/export によるモジュール管理)

これまで、JavaScript には複数ファイルに JavaScript を分割できませんでした。
HTML 上に複数個 `<script src="xxx.js"></script>` を書いてきた時代が終わったのです。

```js
// example.js
import helloImport from './example1.js';
alert(helloImport());
```

```js
// example1.js
function helloImport() {
	return "Hello import";
}
export default helloImport;
```
ただし、この機能を使うにはブラウザの設定が必要です。

---

### 機能の一覧:class によるクラス定義

今まで、JavaScript でクラスを定義するためにこんな事をしていました。
```js
function Foo () {
  var self = this;
  this.id = 32;
  this.getId = function() { return self.id; }
}
var foo = new Foo();
```
他にもプロトタイプなどを使った実装もあります。
要するに、言語仕様としてクラスという概念がないから、みんな好き勝手にそれっぽく実装していた時代があったのです。

---

### 機能の一覧:class によるクラス定義

ES2015 でそれももう終わり。

```js
class Foo {
  constructor() {
    this.id = 32;
  }
  getId() { return this.id; }
}
var foo = new Foo();
```

これで継承も `extends` で出来る。
素晴らしいの一言です。

---

### 機能の一覧:レキシカルスコープの変数

ES5 までだと、関数スコープの変数しか作ることができず、ローカル変数っぽいものを作るために、わざわざ function を定義していた。
ES2015 からは `{}` が寿命の変数 `let` と定数 `const` が利用できる。

```js
let name = "Hello";
{
  let name = "ageage";
  console.log(name); // ageage
}
console.log(name); // Hello
```
---

### 機能の一覧:デフォルト引数

説明不要の一撃

```js
function multiply(a, b = 1) {
  return a*b;
}
multiply(5); // 5
```

[参考:ES2015 (ES6)についてのまとめ](https://qiita.com/tuno-tky/items/74ca595a9232bcbcd727)

---

### 機能の一覧:アロー関数

ラムダ式とも言います。

```js
// 従来のfunctionを使った書き方
var plus = function(x, y) {
  return x + y;
};

// アロー関数
let plus = (x, y) => {
  return x + y;
};

// 単一式の場合はブラケットやreturnを省略できる
let plus = (x, y) => x + y;
```

[参考:ES2015 (ES6)についてのまとめ](https://qiita.com/tuno-tky/items/74ca595a9232bcbcd727)

---

### 機能の一覧:可変長引数

これも説明不要ですかね？

```js
function f(x, ...ys) {
    console.log(x, ys);
}
f(2, 3, 5);
//=> 2 [ 3, 5 ]
```

[参考:ES2015 (ES6)についてのまとめ](https://qiita.com/tuno-tky/items/74ca595a9232bcbcd727)

---

### 機能の一覧:配列展開

```js
var array = [1, 2, 3]
function f(x, y, z) { }
f(...array);
//f(1, 2, 3)という引数での関数fの呼び出しと同義

[...array, 4, 5, 6]
//[1, 2, 3, 4, 5, 6]となる
var x
var y
var z
var variables = [x, y, z]
[a, b, ...variables] = [1, 2, 3, 4, 5];
// a = 1, b = 2, x = 3, y = 4, z = 5とした場合と同じ
```

[参考:ES2015 (ES6)についてのまとめ](https://qiita.com/tuno-tky/items/74ca595a9232bcbcd727)

---

### 機能の一覧:テンプレート文字列

これも見たままですかね？

```js
let name = "azalea";
let html = `<div>Name: ${name}</div>`;
```

バッククォートで文字列を作ると、変数埋め込みとかができる。

---

### 機能の一覧:イテレータとジェネレータ

繰り返しで利用可能な値をプログラム生成する機能が追加。

```js
let list = {}

// イテレータを定義する
list[Symbol.iterator] = function(){
  let i = 0
  let iter = {
    next: () => {
      return { done: false, value: i++}
    }
  }

  return iter
}
```

---

### 機能の一覧:イテレータとジェネレータ

使い方はこんな感じ。

```js
// forで取得する
let iter = list[Symbol.iterator]()
for(let i=0; i < 10; i++){
    let result = iter.next()
    if(result.done) break
    console.log(result.value)
}

// for-ofで取得
for(let n of list){
  if(n >= 10) break
  console.log(n)
}
```

---

### 機能の一覧:イテレータとジェネレータ

お次はジェネレータ。

```js
let list = {}

// ジェネレータを定義する
const gen = function*(){
  for(let i=0;;)
    yield i++
}

// for-ofで生成する
for(let n of gen()){
  if(n >= 10) break
  console.log(n)
}
```

参考: [ES6(ES2015)チートシート](https://qiita.com/morrr/items/883cb902ccda37e840bc)

---

### 機能の一覧:promises を使った非同期処理

JavaScript はそれまで 1 スレッドでしか動きませんでしたが、等々非同期処理し始めました。
JQuery の最新版で対応が始まってますね。

```js
const promise = new Promise((resolve, reject) => {
  // ...何か非同期的な処理を行う
  // 成功したら呼ぶ
  resolve()
  // 失敗したら呼ぶ
  reject()
});

promise.then(() => {
  console.log('success');
});

promise.catch(err => {
  console.error('failed: ' + err)
});
```

参考: [ES6(ES2015)チートシート](https://qiita.com/morrr/items/883cb902ccda37e840bc)

---

### 機能の一覧:末尾再帰最適化

これは特別なシンタックスがあるわけでなく、再起のスタックオーバーフローが減る思った方がいいでしょう。
再起を使いすぎると、スタックオーバーフローするのはご存知の通り。

コレは要するに

```js
function hoge(x, list) {
  if (x > 10) { return list; }
  return hoge([x, ...list]);
}
```

こんな風に書くと実行時にメモリの中で while 文に書き換えてくれるというヤツです。

---

# そして ES2016-2017 へ！
### -JS はまだまだ続く-

---

### そして ES2016-2017 へ！

ES2016/2017 の仕様に関しては[仕様まとめ記事](https://qiita.com/Yuta_Yamamoto/items/573ecace8d8523c102b0)が存在します。
が、昨今は策定中でもブラウザが実装していたりします。

正式リリースを待たなくても使える場合があるので、確認してみるといいかもしれません。

---

# 追伸

誰か ES2016-2017 やってくれないかなぁ（汗