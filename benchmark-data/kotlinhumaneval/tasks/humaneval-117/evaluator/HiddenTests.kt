fun main() {
    var arg10 : List<Int> = mutableListOf(4, -4, 4)
    var arg11 : Int = 2
    var x1 : List<Any> = maximum(arg10, arg11);
    var v1 : List<Any> = mutableListOf(4, 4);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(-3, 2, 1, 2, -1, -2, 1)
    var arg21 : Int = 1
    var x2 : List<Any> = maximum(arg20, arg21);
    var v2 : List<Any> = mutableListOf(2);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(123, -123, 20, 0, 1, 2, -3)
    var arg31 : Int = 3
    var x3 : List<Any> = maximum(arg30, arg31);
    var v3 : List<Any> = mutableListOf(2, 20, 123);
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(-123, 20, 0, 1, 2, -3)
    var arg41 : Int = 4
    var x4 : List<Any> = maximum(arg40, arg41);
    var v4 : List<Any> = mutableListOf(0, 1, 2, 20);
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(5, 15, 0, 3, -13, -8, 0)
    var arg51 : Int = 7
    var x5 : List<Any> = maximum(arg50, arg51);
    var v5 : List<Any> = mutableListOf(-13, -8, 0, 0, 3, 5, 15);
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf(-1, 0, 2, 5, 3, -10)
    var arg61 : Int = 2
    var x6 : List<Any> = maximum(arg60, arg61);
    var v6 : List<Any> = mutableListOf(3, 5);
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Int> = mutableListOf(1, 0, 5, -7)
    var arg71 : Int = 1
    var x7 : List<Any> = maximum(arg70, arg71);
    var v7 : List<Any> = mutableListOf(5);
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Int> = mutableListOf(4, -4)
    var arg81 : Int = 2
    var x8 : List<Any> = maximum(arg80, arg81);
    var v8 : List<Any> = mutableListOf(-4, 4);
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Int> = mutableListOf(-10, 10)
    var arg91 : Int = 2
    var x9 : List<Any> = maximum(arg90, arg91);
    var v9 : List<Any> = mutableListOf(-10, 10);
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Int> = mutableListOf(1, 2, 3, -23, 243, -400, 0)
    var arg101 : Int = 0
    var x10 : List<Any> = maximum(arg100, arg101);
    var v10 : List<Any> = mutableListOf();
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }


}

