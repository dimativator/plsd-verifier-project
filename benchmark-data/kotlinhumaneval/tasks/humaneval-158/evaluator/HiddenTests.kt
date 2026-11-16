fun main() {
    var arg10 : String = "1234"
    var x1 : String = solve(arg10);
    var v1 : String = "4321";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "ab"
    var x2 : String = solve(arg20);
    var v2 : String = "AB";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "#a@C"
    var x3 : String = solve(arg30);
    var v3 : String = "#A@c";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "#AsdfW^45"
    var x4 : String = solve(arg40);
    var v4 : String = "#aSDFw^45";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "#6@2"
    var x5 : String = solve(arg50);
    var v5 : String = "2@6#";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "#\$a^D"
    var x6 : String = solve(arg60);
    var v6 : String = "#\$A^d";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "#ccc"
    var x7 : String = solve(arg70);
    var v7 : String = "#CCC";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }


}

