fun main() {
    var arg00 : List<Double> = mutableListOf(1.0, 2.0, 3.0)
    var x0 : Int = sumSquares(arg00);
    var v0 : Int = 14;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Double> = mutableListOf(1.0, 2.0, 3.0)
    var x1 : Int = sumSquares(arg10);
    var v1 : Int = 14;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Double> = mutableListOf(1.0, 3.0, 5.0, 7.0)
    var x2 : Int = sumSquares(arg20);
    var v2 : Int = 84;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Double> = mutableListOf(1.4, 4.2, 0.0)
    var x3 : Int = sumSquares(arg30);
    var v3 : Int = 29;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Double> = mutableListOf(-2.4, 1.0, 1.0)
    var x4 : Int = sumSquares(arg40);
    var v4 : Int = 6;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Double> = mutableListOf(100.0, 1.0, 15.0, 2.0)
    var x5 : Int = sumSquares(arg50);
    var v5 : Int = 10230;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Double> = mutableListOf(10000.0, 10000.0)
    var x6 : Int = sumSquares(arg60);
    var v6 : Int = 200000000;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<Double> = mutableListOf(-1.4, 4.6, 6.3)
    var x7 : Int = sumSquares(arg70);
    var v7 : Int = 75;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<Double> = mutableListOf(-1.4, 17.9, 18.9, 19.9)
    var x8 : Int = sumSquares(arg80);
    var v8 : Int = 1086;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<Double> = mutableListOf(0.0)
    var x9 : Int = sumSquares(arg90);
    var v9 : Int = 0;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<Double> = mutableListOf(-1.0)
    var x10 : Int = sumSquares(arg100);
    var v10 : Int = 1;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : List<Double> = mutableListOf(-1.0, 1.0, 0.0)
    var x11 : Int = sumSquares(arg110);
    var v11 : Int = 2;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

