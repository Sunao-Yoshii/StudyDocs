package net.white.azalea;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public class VendingMachine {

    public static void main(String[] args) throws IOException {
        new VendingMachine().buy();
    }

    private List<Product> products = List.of(
            new Product(110, "へ〜いお茶"),
            new Product(130, "超カテキンなアレ"),
            new Product(110, "ポーラ"),
            new Product(120, "練乳珈琲"),
            new Product(90, "へ〜いお茶")
    );

    private void buy() throws IOException {
        // 入力用
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = null;
        try {

            // ジュース選択
            System.out.println("ジュースの選択");
            for (int i = 0; i < products.size(); i++) {
                Product p = products.get(i);
                System.out.println(String.format("%d: Item: %s (%d)", i, p.getName(), p.getPrice()));
            }
            int n = 999;
            while (n >= products.size()) {
                n = Integer.parseInt(reader.readLine());
                if (n >= products.size()) {
                    System.out.println("選択出来るジュースを選んでください");
                }
            }

            // 選択したジュース
            Product selected = products.get(n);

            // コインの挿入
            line = null;
            System.out.println("コインを入れてね(使用可能: 500, 100, 50, 10)");
            while (n < selected.getPrice()) {
                int coin = Integer.parseInt(reader.readLine());
                if (List.of(500, 100, 50, 10).contains(coin)) {
                    n += coin;
                } else {
                    System.out.println("その硬貨は使えません");
                }
            }

            // 釣り計算
            int r = n - selected.getPrice();
            System.out.println("お釣り硬貨は以下の通りです。");
            while (r > 0) {
                if (r > 500) {
                    System.out.println("500円");
                    r -= 500;
                    continue;
                }
                if (r > 100) {
                    System.out.println("500円");
                    r -= 500;
                    continue;
                }
                if (r > 50) {
                    System.out.println("500円");
                    r -= 500;
                    continue;
                }
                if (r > 10) {
                    System.out.println("500円");
                    r -= 500;
                }
            }
        } catch (Exception e) {
            System.out.println(e.toString());
        } finally {
            reader.close();
        }
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

