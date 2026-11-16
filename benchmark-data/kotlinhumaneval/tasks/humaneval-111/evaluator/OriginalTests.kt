fun main() {
    var arg00 : List<Long> = mutableListOf(2, 3, 4, 1, 2, 4)
    var x0 : Long = minsubarraysum(arg00);
    var v0 : Long = 1;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Long> = mutableListOf(-1, -2, -3)
    var x1 : Long = minsubarraysum(arg10);
    var v1 : Long = -6;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Long> = mutableListOf(-1, -2, -3, 2, -10)
    var x2 : Long = minsubarraysum(arg20);
    var v2 : Long = -14;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Long> = mutableListOf(-9999999999999999)
    var x3 : Long = minsubarraysum(arg30);
    var v3 : Long = -9999999999999999;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Long> = mutableListOf(0, 10, 20, 1000000)
    var x4 : Long = minsubarraysum(arg40);
    var v4 : Long = 0;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Long> = mutableListOf(-1, -2, -3, 10, -5)
    var x5 : Long = minsubarraysum(arg50);
    var v5 : Long = -6;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Long> = mutableListOf(100, -1, -2, -3, 10, -5)
    var x6 : Long = minsubarraysum(arg60);
    var v6 : Long = -6;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Long> = mutableListOf(10, 11, 13, 8, 3, 4)
    var x7 : Long = minsubarraysum(arg70);
    var v7 : Long = 3;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Long> = mutableListOf(100, -33, 32, -1, 0, -2)
    var x8 : Long = minsubarraysum(arg80);
    var v8 : Long = -33;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Long> = mutableListOf(-10)
    var x9 : Long = minsubarraysum(arg90);
    var v9 : Long = -10;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Long> = mutableListOf(7)
    var x10 : Long = minsubarraysum(arg100);
    var v10 : Long = 7;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : List<Long> = mutableListOf(1, -1)
    var x11 : Long = minsubarraysum(arg110);
    var v11 : Long = -1;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

