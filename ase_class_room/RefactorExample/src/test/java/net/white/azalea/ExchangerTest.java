package net.white.azalea;

import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class ExchangerTest {

    @Test
    public void exchange() {
        // 使えるコインは 100, 50 ,10 円硬貨まで
        List<Integer> coins = List.of(100, 50, 10);

        // 実行したら
        List<Integer> exchanged = Exchanger.exchange(460, coins);

        // 460 円 = 100, 1000, 100, 100, 50, 10
        assertEquals(List.of(100, 100, 100, 100, 50, 10), exchanged);
    }
}