package net.white.azalea;

import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class VendingMachineTest {

    List<Product> products = List.of(
            new Product(60, "テスト1"),
            new Product(500, "テスト2"),
            new Product(100, "テスト3")
    );

    List<Integer> coins = List.of(100, 50, 10);
    IOUtils ioUtils;
    VendingMachine vendingMachine;

    @Before
    public void setUp() {
        this.ioUtils = mock(IOUtils.class);
        this.vendingMachine = new VendingMachine(this.ioUtils, this.products, this.coins);
    }

    @Test
    public void getExchangesStr() {
        assertEquals(
                "100円\n50円\n10円",
                this.vendingMachine.getExchangesStr(List.of(100, 50, 10)));
    }

    @Test
    public void inputPayment() throws Exception {
        // 選択をモックで処理する。
        when(this.ioUtils.selectNumber(this.coins, "その硬貨は使えません"))
                .thenReturn(100);

        // 実行
        int paid = this.vendingMachine.inputPayment(420);

        assertEquals("100 円しか応答しないのだから、500 円まで支払うはず", 500, paid);

        // 5 回の 100 円入金があったはず
        verify(this.ioUtils, times(5))
                .selectNumber(eq(this.coins), anyString());
    }

    @Test
    public void getProductIndexes() {
        // 商品のインデックスリストなので、このクラスの products から予測できる
        assertEquals(
                List.of(0, 1, 2),
                this.vendingMachine.getProductIndexes()
        );
    }

    @Test
    public void getProductsString() {
        // 商品を列挙するだけなので、このクラスの products から予測できる
        assertEquals(
                "0: Item: テスト1 (60)\n1: Item: テスト2 (500)\n2: Item: テスト3 (100)",
                this.vendingMachine.getProductsString()
        );
    }

    @Test
    public void buy() throws IOException {
        // 60 円商品を選択し
        when(this.ioUtils.selectNumber(eq(List.of(0, 1, 2)), anyString())).thenReturn(0);

        // 100 円支払う
        when(this.ioUtils.selectNumber(eq(this.coins), anyString())).thenReturn(100);

        // そうしたとき
        this.vendingMachine.buy();

        // お釣りとして、10 円 * 4 が表示される
        verify(this.ioUtils, times(1))
                .println("10円\n10円\n10円\n10円");
    }
}