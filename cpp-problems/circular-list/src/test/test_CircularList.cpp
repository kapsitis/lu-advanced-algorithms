//#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "CircularList.h"

using namespace ds_course;
TEST_CASE("circular_lists insert stuff in reverse order", "[circlelist]")
{
    CircularList cL;
    REQUIRE(cL.toString() == "[]");
    cL.pushFront(2);
    REQUIRE(cL.getSize() == 1);
    REQUIRE(cL.toString() == "[2]");
    cL.pushFront(4);
    REQUIRE(cL.getSize() == 2);
    REQUIRE(cL.toString() == "[4, 2]");
    cL.pushFront(6);
    REQUIRE(cL.getSize() == 3);
    REQUIRE(cL.toString() == "[6, 4, 2]");
}

TEST_CASE("On 6-number list:", "[circlelist]")
{
    CircularList cl;
    cl.pushFront(11);
    cl.moveNext();
    cl.pushFront(12);
    cl.moveNext();
    cl.pushFront(13);
    cl.moveNext();
    cl.pushFront(14);
    cl.moveNext();
    cl.pushFront(15);
    cl.moveNext();
    cl.pushFront(16);
    cl.moveNext();
    REQUIRE(cl.toString() == "[11, 12, 13, 14, 15, 16]");

    SECTION("Can advance 4 times") {
        for (int j = 0; j < 4; j++) 
            cl.moveNext();
        REQUIRE(cl.toString() == "[15, 16, 11, 12, 13, 14]");
    }

    SECTION("Insert at position 2") {
        cl.moveNext();
        cl.moveNext();
        REQUIRE(cl.toString() == "[13, 14, 15, 16, 11, 12]");
        cl.pushFront(1000);
        REQUIRE(cl.toString() == "[1000, 13, 14, 15, 16, 11, 12]");
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        REQUIRE(cl.toString() == "[11, 12, 1000, 13, 14, 15, 16]");
    }

    SECTION("Delete at position 2") {
        cl.moveNext();
        cl.moveNext();
        REQUIRE(cl.toString() == "[13, 14, 15, 16, 11, 12]");
        cl.popFront();
        REQUIRE(cl.toString() == "[14, 15, 16, 11, 12]");
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        REQUIRE(cl.toString() == "[11, 12, 14, 15, 16]");
    }

    SECTION("insert, then delete") {
        cl.pushFront(100);
        REQUIRE(cl.toString() == "[100, 11, 12, 13, 14, 15, 16]");
        cl.moveNext();
        cl.moveNext();
        cl.popFront();
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        cl.moveNext();
        REQUIRE(cl.toString() == "[100, 11, 13, 14, 15, 16]");
    }

    SECTION("ability to delete everything")
    {
        cl.popFront();
        cl.popFront();
        cl.popFront();
        REQUIRE(cl.toString() == "[14, 15, 16]");
        cl.popFront();
        cl.popFront();
        cl.popFront();
        REQUIRE(cl.toString() == "[]");
        cl.pushFront(17);
        REQUIRE(cl.toString() == "[17]");
    }
}
