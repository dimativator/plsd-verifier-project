fun main() {
    var arg10 : Int = 6
    var x1 : Boolean = isEqualToSumEven(arg10);
    var v1 : Boolean = false;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 8
    var x2 : Boolean = isEqualToSumEven(arg20);
    var v2 : Boolean = true;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 10
    var x3 : Boolean = isEqualToSumEven(arg30);
    var v3 : Boolean = true;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Int = 11
    var x4 : Boolean = isEqualToSumEven(arg40);
    var v4 : Boolean = false;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Int = 12
    var x5 : Boolean = isEqualToSumEven(arg50);
    var v5 : Boolean = true;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Int = 13
    var x6 : Boolean = isEqualToSumEven(arg60);
    var v6 : Boolean = false;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Int = 16
    var x7 : Boolean = isEqualToSumEven(arg70);
    var v7 : Boolean = true;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

