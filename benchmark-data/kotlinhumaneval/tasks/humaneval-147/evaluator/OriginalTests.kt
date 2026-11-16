fun main() {
    var arg00 : Int = 7
    var arg01 : Int = 34
    var arg02 : Int = 12
    var x0 : Int = xOrY(arg00, arg01, arg02);
    var v0 : Int = 34;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Int = 15
    var arg11 : Int = 8
    var arg12 : Int = 5
    var x1 : Int = xOrY(arg10, arg11, arg12);
    var v1 : Int = 5;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 3
    var arg21 : Int = 33
    var arg22 : Int = 5212
    var x2 : Int = xOrY(arg20, arg21, arg22);
    var v2 : Int = 33;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 1259
    var arg31 : Int = 3
    var arg32 : Int = 52
    var x3 : Int = xOrY(arg30, arg31, arg32);
    var v3 : Int = 3;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 7919
    var arg41 : Int = -1
    var arg42 : Int = 12
    var x4 : Int = xOrY(arg40, arg41, arg42);
    var v4 : Int = -1;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 3609
    var arg51 : Int = 1245
    var arg52 : Int = 583
    var x5 : Int = xOrY(arg50, arg51, arg52);
    var v5 : Int = 583;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 91
    var arg61 : Int = 56
    var arg62 : Int = 129
    var x6 : Int = xOrY(arg60, arg61, arg62);
    var v6 : Int = 129;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 6
    var arg71 : Int = 34
    var arg72 : Int = 1234
    var x7 : Int = xOrY(arg70, arg71, arg72);
    var v7 : Int = 1234;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : Int = 1
    var arg81 : Int = 2
    var arg82 : Int = 0
    var x8 : Int = xOrY(arg80, arg81, arg82);
    var v8 : Int = 0;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : Int = 2
    var arg91 : Int = 2
    var arg92 : Int = 0
    var x9 : Int = xOrY(arg90, arg91, arg92);
    var v9 : Int = 2;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

