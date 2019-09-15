defmodule TestProjectTest do
  use ExUnit.Case
  doctest TestProject

  test "greets the world" do
    assert TestProject.hello() == :world
  end

  test "Result of addition" do
    assert TestProject.add(4, 5) == 9
  end

  test "hahaha" do
    assert fire() == 123
  end

  def fire do
    t1 = "hoge"
    t1 = 123
    t1
  end
end
