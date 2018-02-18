package net.white_azalea;

import java.io.File;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;

public class App {
    public static void main(String[] args) throws Exception {
        File classPath = new File("../lib");

        URLClassLoader classLoader =
                URLClassLoader.newInstance(new URL[] {classPath.toURL()});

        Class helloClass = classLoader.loadClass("net.white_azalea.Hello");
        Method addHello = helloClass.getMethod("addHello", String.class);

        System.out.println(
                addHello.invoke(
                        helloClass.newInstance(),
                        "Reflection call."
                )
        );
    }
}
