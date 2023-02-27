#define CATCH_CONFIG_MAIN

#include "catch.hpp"
#include "Stack.h"

TEST_CASE("Exceptions on empty stack", "[stack]")
{
    Stack stack(3);
    REQUIRE_THROWS_AS(stack.top(), std::out_of_range);
    REQUIRE_THROWS_AS(stack.pop(), std::out_of_range);
    stack.push(17);
    stack.pop();
    REQUIRE_THROWS_AS(stack.top(), std::out_of_range);
}

TEST_CASE("Lifo order", "[stack]")
{
    Stack stack(3);
    stack.push(1);
    stack.push(2);
    REQUIRE(stack.top() == 2);
    REQUIRE(stack.pop() == 2);
    REQUIRE(stack.top() == 1);
    REQUIRE(stack.pop() == 1);
    REQUIRE_THROWS_AS(stack.top(), std::out_of_range);
}

TEST_CASE("3-element stack", "[stack]")
{
    // common initialization part
    Stack stack(3);
    stack.push(11);
    stack.push(12);
    stack.push(13);

    SECTION("Stack is full") {
        REQUIRE_THROWS_AS(stack.push(14), std::out_of_range);
    };

    SECTION("Multiple top calls") {
        REQUIRE(stack.top() == 13);
        REQUIRE(stack.top() == 13);
    };
}
