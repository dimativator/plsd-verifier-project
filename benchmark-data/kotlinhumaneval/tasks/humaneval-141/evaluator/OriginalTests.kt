fun main() {
    var arg00 : String = "1/5"
    var arg01 : String = "5/1"
    var x0 : Boolean = simplify(arg00, arg01);
    var v0 : Boolean = true;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : String = "1/6"
    var arg11 : String = "2/1"
    var x1 : Boolean = simplify(arg10, arg11);
    var v1 : Boolean = false;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "5/1"
    var arg21 : String = "3/1"
    var x2 : Boolean = simplify(arg20, arg21);
    var v2 : Boolean = true;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "7/10"
    var arg31 : String = "10/2"
    var x3 : Boolean = simplify(arg30, arg31);
    var v3 : Boolean = false;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "2/10"
    var arg41 : String = "50/10"
    var x4 : Boolean = simplify(arg40, arg41);
    var v4 : Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "7/2"
    var arg51 : String = "4/2"
    var x5 : Boolean = simplify(arg50, arg51);
    var v5 : Boolean = true;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "11/6"
    var arg61 : String = "6/1"
    var x6 : Boolean = simplify(arg60, arg61);
    var v6 : Boolean = true;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "2/3"
    var arg71 : String = "5/2"
    var x7 : Boolean = simplify(arg70, arg71);
    var v7 : Boolean = false;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "5/2"
    var arg81 : String = "3/5"
    var x8 : Boolean = simplify(arg80, arg81);
    var v8 : Boolean = false;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : String = "2/4"
    var arg91 : String = "8/4"
    var x9 : Boolean = simplify(arg90, arg91);
    var v9 : Boolean = true;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : String = "2/4"
    var arg101 : String = "4/2"
    var x10 : Boolean = simplify(arg100, arg101);
    var v10 : Boolean = true;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : String = "1/5"
    var arg111 : String = "5/1"
    var x11 : Boolean = simplify(arg110, arg111);
    var v11 : Boolean = true;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : String = "1/5"
    var arg121 : String = "1/5"
    var x12 : Boolean = simplify(arg120, arg121);
    var v12 : Boolean = false;
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }


}

