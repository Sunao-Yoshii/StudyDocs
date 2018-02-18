package net.white_azalea;

import org.apache.commons.lang3.StringUtils;

public class App {
  public static void main(String[] args) {
    if (args.length == 0) {
      System.out.println("Please input arg.");
      return;
    }

    System.out.println("Reverse: " + StringUtils.reverse(args[0]));
  }
}
