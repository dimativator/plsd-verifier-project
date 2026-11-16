fun main() {
    var arg10 : String = "Mudasir Hanif "
    var x1 : String = fixSpaces(arg10);
    var v1 : String = "Mudasir_Hanif_";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "Yellow Yellow  Dirty  Fellow"
    var x2 : String = fixSpaces(arg20);
    var v2 : String = "Yellow_Yellow__Dirty__Fellow";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "Exa   mple"
    var x3 : String = fixSpaces(arg30);
    var v3 : String = "Exa-mple";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "   Exa 1 2 2 mple"
    var x4 : String = fixSpaces(arg40);
    var v4 : String = "-Exa_1_2_2_mple";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }


}

