fun main() {
    var arg10 : Int = 6
    var x1 : Int = getMaxTriples(arg10);
    var v1 : Int = 4;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 10
    var x2 : Int = getMaxTriples(arg20);
    var v2 : Int = 36;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 100
    var x3 : Int = getMaxTriples(arg30);
    var v3 : Int = 53361;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

