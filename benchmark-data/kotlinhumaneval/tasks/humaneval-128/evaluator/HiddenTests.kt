fun main() {
    var arg10 : Int = 54
    var x1 : Int = digits(arg10);
    var v1 : Int = 5;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 120
    var x2 : Int = digits(arg20);
    var v2 : Int = 1;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 5014
    var x3 : Int = digits(arg30);
    var v3 : Int = 5;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 98765
    var x4 : Int = digits(arg40);
    var v4 : Int = 315;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 5576543
    var x5 : Int = digits(arg50);
    var v5 : Int = 2625;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 2468
    var x6 : Int = digits(arg60);
    var v6 : Int = 0;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

