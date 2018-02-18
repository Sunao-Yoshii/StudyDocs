package net.white_azalea;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class App {
    public static void main(String[] srgs) throws IOException {
        try (InputStream is = App.class.getResourceAsStream("/example.properties")) {
            Properties props = new Properties();
            props.load(is);
            System.out.println("Read example: " + props.getProperty("example"));
        }
    }
}
