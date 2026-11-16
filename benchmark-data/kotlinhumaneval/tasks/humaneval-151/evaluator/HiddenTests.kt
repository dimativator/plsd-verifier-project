fun main() {
    var arg10 : String = "yello"
    var arg11 : String = "ell"
    var x1 : Boolean = cycpatternCheck(arg10, arg11);
    var v1 : Boolean = true;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "whattup"
    var arg21 : String = "ptut"
    var x2 : Boolean = cycpatternCheck(arg20, arg21);
    var v2 : Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "efef"
    var arg31 : String = "fee"
    var x3 : Boolean = cycpatternCheck(arg30, arg31);
    var v3 : Boolean = true;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "abab"
    var arg41 : String = "aabb"
    var x4 : Boolean = cycpatternCheck(arg40, arg41);
    var v4 : Boolean = false;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "winemtt"
    var arg51 : String = "tinem"
    var x5 : Boolean = cycpatternCheck(arg50, arg51);
    var v5 : Boolean = true;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

