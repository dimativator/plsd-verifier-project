fun main() {
    var arg10 : Int = 1
    var arg11 : Int = 2
    var arg12 : Int = 3
    var x1 : Boolean = rightAngleTriangle(arg10, arg11, arg12);
    var v1 : Boolean = false;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 10
    var arg21 : Int = 6
    var arg22 : Int = 8
    var x2 : Boolean = rightAngleTriangle(arg20, arg21, arg22);
    var v2 : Boolean = true;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 2
    var arg31 : Int = 2
    var arg32 : Int = 2
    var x3 : Boolean = rightAngleTriangle(arg30, arg31, arg32);
    var v3 : Boolean = false;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 7
    var arg41 : Int = 24
    var arg42 : Int = 25
    var x4 : Boolean = rightAngleTriangle(arg40, arg41, arg42);
    var v4 : Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 10
    var arg51 : Int = 5
    var arg52 : Int = 7
    var x5 : Boolean = rightAngleTriangle(arg50, arg51, arg52);
    var v5 : Boolean = false;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 5
    var arg61 : Int = 12
    var arg62 : Int = 13
    var x6 : Boolean = rightAngleTriangle(arg60, arg61, arg62);
    var v6 : Boolean = true;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 15
    var arg71 : Int = 8
    var arg72 : Int = 17
    var x7 : Boolean = rightAngleTriangle(arg70, arg71, arg72);
    var v7 : Boolean = true;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : Int = 48
    var arg81 : Int = 55
    var arg82 : Int = 73
    var x8 : Boolean = rightAngleTriangle(arg80, arg81, arg82);
    var v8 : Boolean = true;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : Int = 1
    var arg91 : Int = 1
    var arg92 : Int = 1
    var x9 : Boolean = rightAngleTriangle(arg90, arg91, arg92);
    var v9 : Boolean = false;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : Int = 2
    var arg101 : Int = 2
    var arg102 : Int = 10
    var x10 : Boolean = rightAngleTriangle(arg100, arg101, arg102);
    var v10 : Boolean = false;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }


}

