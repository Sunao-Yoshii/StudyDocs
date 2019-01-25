package net.white.azalea;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

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

    public VendingMachine(IOUtils ioUtils, List<Product> products) {
        this.ioUtils = ioUtils;
        this.products = products;
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

            // ジュース選択
            int n = 999;
            while (n >= products.size()) {
                n = this.ioUtils.readInteger();
                if (n >= products.size()) {
                    this.ioUtils.println("選択出来るジュースを選んでください");
                }
            }

            // 選択したジュース
            Product selected = products.get(n);

            // コインの挿入
            this.ioUtils.println("コインを入れてね(使用可能: 500, 100, 50, 10)");
            while (n < selected.getPrice()) {
                int coin = this.ioUtils.readInteger();
                if (List.of(500, 100, 50, 10).contains(coin)) {
                    n += coin;
                } else {
                    this.ioUtils.println("その硬貨は使えません");
                }
            }

            // 釣り計算
            int r = n - selected.getPrice();
            this.ioUtils.println("お釣り硬貨は以下の通りです。");
            while (r > 0) {
                if (r > 500) {
                    this.ioUtils.println("500円");
                    r -= 500;
                    continue;
                }
                if (r > 100) {
                    this.ioUtils.println("100円");
                    r -= 500;
                    continue;
                }
                if (r > 50) {
                    this.ioUtils.println("50円");
                    r -= 500;
                    continue;
                }
                if (r > 10) {
                    this.ioUtils.println("10円");
                    r -= 500;
                }
            }
        } catch (Exception e) {
            this.ioUtils.println(e.toString());
        }
    }

    public String getProductsString() {
        List<String> productStrings = new ArrayList<>();
        for (int i = 0; i < products.size(); i++) {
            Product p = products.get(i);
            productStrings.add(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
        }
        return String.join("\n", productStrings);
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

    public void println(String v) {
        this.out.println(v);
    }

    public int readInteger() throws IOException {
        while(true) {
            try {
                return Integer.parseInt(reader.readLine());
            } catch (NumberFormatException e) {
                this.out.println("整数を入力してください。");
            }
        }
    }
}
