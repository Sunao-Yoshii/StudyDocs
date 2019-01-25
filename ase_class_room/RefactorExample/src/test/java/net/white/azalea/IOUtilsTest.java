package net.white.azalea;

import org.junit.Before;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.PrintStream;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class IOUtilsTest {
    IOUtils ioUtils;
    BufferedReader brMock;
    PrintStream psMock;

    @Before
    public void setUp() {
        this.brMock = mock(BufferedReader.class);
        this.psMock = mock(PrintStream.class);
        this.ioUtils = new IOUtils(brMock, psMock);
    }

    @Test
    public void println() {
        // 実行したら
        this.ioUtils.println("Example!");

        // println が Example! 引数で１回だけ呼ばれた
        verify(this.psMock, times(1))
                .println("Example!");
    }

    @Test
    public void readInteger() throws Exception {
        // 呼び出し設定
        // 初回は "Not a num.", ２回目が "64", 3回目は 128
        when(this.brMock.readLine())
                .thenReturn("Not a num.", "64", "128");

        // 実行したら
        int value = this.ioUtils.readInteger();

        // 64 が返っており
        assertEquals(64, value);

        // 整数入力を促される
        verify(this.psMock, times(1))
                .println("整数を入力してください。");
    }

    @Test
    public void selectNumber() throws Exception {
        // 設定
        when(this.brMock.readLine())
                .thenReturn("64", "128");

        // 2 回目に 128 がヒットする
        int selected = this.ioUtils.selectNumber(
                List.of(32, 128, 256), "エラーテスト");

        // 128 が返り、最初の readLine はエラーメッセージとして格納される
        assertEquals(128, selected);
        verify(this.psMock, times(1))
                .println("エラーテスト");
    }
}