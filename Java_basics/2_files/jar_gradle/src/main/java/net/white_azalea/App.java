package net.white_azalea;

import java.io.InputStream;
import java.util.Properties;

public class App {
    public static void main(String[] args) throws Exception {
        try (InputStream is = App.class.getResourceAsStream("/example.properties")) {
            Properties props = new Properties();
            props.load(is);
            System.out.println("Read : " + props.getProperty("example"));
        }
    }
}
