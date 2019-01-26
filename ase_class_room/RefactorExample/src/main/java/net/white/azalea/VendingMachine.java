package net.white.azalea;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class VendingMachine {

    public static void main(String[] args) throws IOException {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            List<Product> products = List.of(
                    new Product(110, "へ〜いお茶"),
                    new Product(130, "超カテキンなアレ"),
                    new Product(110, "ポーラ"),
                    new Product(120, "練乳珈琲"),
                    new Product(90, "へ〜いお茶")
            );
            IOUtils util = new IOUtils(reader, System.out);

            new VendingMachine(util, products).buy();
        }
    }

    private final List<Product> products;
    private final IOUtils ioUtils;
    private final List<Integer> coins;

    public VendingMachine(IOUtils ioUtils, List<Product> products) {
        this(ioUtils, products, List.of(500, 100, 50, 10));
    }

    public VendingMachine(IOUtils ioUtils, List<Product> products, List<Integer> coins) {
        this.ioUtils = ioUtils;
        this.products = products;
        this.coins = coins;
    }

    /**
     * 起動すると、商品を列挙し、商品選択させる。商品選択後はコインを投入させ、支払い金額を超えたら釣り銭を出力する。
     * というクソコード
     */
    public void buy() {
        try {
            // ジュースリスト表示
            this.ioUtils.println("ジュースの選択");
            this.ioUtils.println(this.getProductsString());

            // 選択したジュース
            Product product = products.get(
                    this.ioUtils.selectNumber(
                            this.getProductIndexes(), "選択出来るジュースを選んでください"));

            // コインの挿入
            this.ioUtils.println("コインを入れてね(使用可能: 500, 100, 50, 10)");
            int insertedCoin = inputPayment(product.getPrice());

            // 釣り計算/表示
            this.ioUtils.println("お釣り硬貨は以下の通りです。");
            List<Integer> changes = Exchanger.exchange(insertedCoin - product.getPrice(), this.coins);
            this.ioUtils.println(this.getExchangesStr(changes));
        } catch (Exception e) {
            this.ioUtils.println(e.toString());
        }
    }

    /**
     * 釣り銭を文字列化する
     * @param changes
     * @return
     */
    String getExchangesStr(List<Integer> changes) {
        return changes.stream()
                .map(i -> String.format("%d円", i))
                .collect(Collectors.joining("\n"));
    }

    /**
     * 目標価格を上回るまでコイン入力を受け付ける.
     *
     * @param price 目標価格
     * @return 支払った合計金額
     * @throws IOException
     */
    int inputPayment(int price) throws IOException {
        int insertedCoin = 0;
        while (insertedCoin < price) {
            insertedCoin += this.ioUtils.selectNumber(this.coins, "その硬貨は使えません");
        }
        return insertedCoin;
    }

    /**
     * 商品のインデックスリストを取得.
     *
     * @return
     */
    List<Integer> getProductIndexes() {
        List<Integer> selectable = new ArrayList<>(products.size());
        for (int k = 0; k < products.size(); k++) {
            selectable.add(k);
        }
        return selectable;
    }

    /**
     * 製品インデックス、製品名と金額を列挙した文字列を取得する.
     *
     * @return
     */
    String getProductsString() {
        List<String> productStrings = new ArrayList<>();
        for (int i = 0; i < products.size(); i++) {
            Product p = products.get(i);
            productStrings.add(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
        }
        return String.join("\n", productStrings);
    }
}

class Exchanger {

    /**
     * 両替による硬貨列挙
     *
     * @param change 釣り銭の金額
     * @param coins  硬貨リスト
     * @return お釣りの硬貨リスト
     */
    public static List<Integer> exchange(int change, List<Integer> coins) {
        List<Integer> changeCoin = new ArrayList<>();
        for (int coin : coins) {
            while (change >= coin) {
                changeCoin.add(coin);
                change -= coin;
            }
        }
        return changeCoin;
    }
}

class Product {
    private int price;
    private String name;

    public int getPrice() {
        return price;
    }

    public String getName() {
        return name;
    }

    public Product(int price, String name) {
        this.price = price;
        this.name = name;
    }
}


class IOUtils {
    private final BufferedReader reader;
    private final PrintStream out;

    public IOUtils(BufferedReader reader, PrintStream out) {
        this.reader = reader;
        this.out = out;
    }

    /**
     * 表示
     *
     * @param v
     */
    public void println(String v) {
        this.out.println(v);
    }

    /**
     * 数字入力の読み取り
     *
     * @return
     * @throws IOException
     */
    public int readInteger() throws IOException {
        while (true) {
            try {
                return Integer.parseInt(reader.readLine());
            } catch (NumberFormatException e) {
                this.out.println("整数を入力してください。");
            }
        }
    }

    /**
     * 選択可能リスト中で指定した数字の入力を促します。選択肢外を指定した場合、エラーメッセージを表示します。
     *
     * @param selectable 選択可能な数字群
     * @param error      選択肢外を指定した時のメッセージ
     * @return 選択された数字
     * @throws IOException
     */
    public int selectNumber(List<Integer> selectable, String error) throws IOException {
        while (true) {
            int input = this.readInteger();
            if (selectable.contains(input)) {
                return input;
            }
            this.println(error);
        }
    }
}
