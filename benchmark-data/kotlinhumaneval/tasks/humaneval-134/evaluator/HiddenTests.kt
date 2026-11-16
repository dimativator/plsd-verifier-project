fun main() {
    var arg10 : Any = 1
    var arg11 : Any = 2.5
    var x1 : Any? = compareOne(arg10, arg11);
    var v1 : Any? = 2.5;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Any = 2
    var arg21 : Any = 3
    var x2 : Any? = compareOne(arg20, arg21);
    var v2 : Any? = 3;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Any = 5
    var arg31 : Any = 6
    var x3 : Any? = compareOne(arg30, arg31);
    var v3 : Any? = 6;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : Any = 1
    var arg41 : Any = "2,3"
    var x4 : Any? = compareOne(arg40, arg41);
    var v4 : Any? = "2,3";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : Any = "5,1"
    var arg51 : Any = "6"
    var x5 : Any? = compareOne(arg50, arg51);
    var v5 : Any? = "6";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : Any = "1"
    var arg61 : Any = "2"
    var x6 : Any? = compareOne(arg60, arg61);
    var v6 : Any? = "2";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : Any = "1"
    var arg71 : Any = 1
    var x7 : Any? = compareOne(arg70, arg71);
    var v7 : Any? = null;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

