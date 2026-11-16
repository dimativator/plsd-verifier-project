fun main() {
    var arg10 : String = "15-01-2012"
    var x1 : Boolean = validDate(arg10);
    var v1 : Boolean = false;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "04-0-2040"
    var x2 : Boolean = validDate(arg20);
    var v2 : Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "06-04-2020"
    var x3 : Boolean = validDate(arg30);
    var v3 : Boolean = true;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "01-01-2007"
    var x4 : Boolean = validDate(arg40);
    var v4 : Boolean = true;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "03-32-2011"
    var x5 : Boolean = validDate(arg50);
    var v5 : Boolean = false;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = ""
    var x6 : Boolean = validDate(arg60);
    var v6 : Boolean = false;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "04-31-3000"
    var x7 : Boolean = validDate(arg70);
    var v7 : Boolean = false;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "06-06-2005"
    var x8 : Boolean = validDate(arg80);
    var v8 : Boolean = true;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : String = "21-31-2000"
    var x9 : Boolean = validDate(arg90);
    var v9 : Boolean = false;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : String = "04-12-2003"
    var x10 : Boolean = validDate(arg100);
    var v10 : Boolean = true;
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : String = "04122003"
    var x11 : Boolean = validDate(arg110);
    var v11 : Boolean = false;
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }

    var arg120 : String = "20030412"
    var x12 : Boolean = validDate(arg120);
    var v12 : Boolean = false;
    if (x12 != v12) {
        throw Exception("Exception -- test case 12 did not pass. x12 = " + x12)
    }

    var arg130 : String = "2003-04"
    var x13 : Boolean = validDate(arg130);
    var v13 : Boolean = false;
    if (x13 != v13) {
        throw Exception("Exception -- test case 13 did not pass. x13 = " + x13)
    }

    var arg140 : String = "2003-04-12"
    var x14 : Boolean = validDate(arg140);
    var v14 : Boolean = false;
    if (x14 != v14) {
        throw Exception("Exception -- test case 14 did not pass. x14 = " + x14)
    }

    var arg150 : String = "04-2003"
    var x15 : Boolean = validDate(arg150);
    var v15 : Boolean = false;
    if (x15 != v15) {
        throw Exception("Exception -- test case 15 did not pass. x15 = " + x15)
    }


}

