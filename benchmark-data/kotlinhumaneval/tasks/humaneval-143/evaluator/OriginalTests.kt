fun main() {
    var arg00 : List<Int> = mutableListOf(5, -2, 1, -5)
    var x0 : Int = specialfilter(arg00);
    var v0 : Int = 0;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : List<Int> = mutableListOf(15, -73, 14, -15)
    var x1 : Int = specialfilter(arg10);
    var v1 : Int = 1;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Int> = mutableListOf(33, -2, -3, 45, 21, 109)
    var x2 : Int = specialfilter(arg20);
    var v2 : Int = 2;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Int> = mutableListOf(43, -12, 93, 125, 121, 109)
    var x3 : Int = specialfilter(arg30);
    var v3 : Int = 4;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Int> = mutableListOf(71, -2, -33, 75, 21, 19)
    var x4 : Int = specialfilter(arg40);
    var v4 : Int = 3;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Int> = mutableListOf(1)
    var x5 : Int = specialfilter(arg50);
    var v5 : Int = 0;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Int> = mutableListOf()
    var x6 : Int = specialfilter(arg60);
    var v6 : Int = 0;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

