fun main() {
    var arg00 : Int = 3
    var x0 : List<Int> = tri(arg00);
    var v0 : List<Int> = mutableListOf(1, 3, 2, 8);
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Int = 4
    var x1 : List<Int> = tri(arg10);
    var v1 : List<Int> = mutableListOf(1, 3, 2, 8, 3);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 5
    var x2 : List<Int> = tri(arg20);
    var v2 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 6
    var x3 : List<Int> = tri(arg30);
    var v3 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15, 4);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 7
    var x4 : List<Int> = tri(arg40);
    var v4 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15, 4, 24);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 8
    var x5 : List<Int> = tri(arg50);
    var v5 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15, 4, 24, 5);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 9
    var x6 : List<Int> = tri(arg60);
    var v6 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15, 4, 24, 5, 35);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 20
    var x7 : List<Int> = tri(arg70);
    var v7 : List<Int> = mutableListOf(1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6, 48, 7, 63, 8, 80, 9, 99, 10, 120, 11);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : Int = 0
    var x8 : List<Int> = tri(arg80);
    var v8 : List<Int> = mutableListOf(1);
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : Int = 1
    var x9 : List<Int> = tri(arg90);
    var v9 : List<Int> = mutableListOf(1, 3);
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

