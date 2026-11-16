fun main() {
    var arg00 : Long = 4
    var x0 : Long = specialFactorial(arg00);
    var v0 : Long = 288;
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : Long = 5
    var x1 : Long = specialFactorial(arg10);
    var v1 : Long = 34560;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Long = 7
    var x2 : Long = specialFactorial(arg20);
    var v2 : Long = 125411328000;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Long = 1
    var x3 : Long = specialFactorial(arg30);
    var v3 : Long = 1;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

