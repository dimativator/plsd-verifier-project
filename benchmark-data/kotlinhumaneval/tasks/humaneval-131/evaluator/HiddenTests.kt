fun main() {
    var arg10: String = "apple pi e"
    var x1: Boolean = checkIfLastCharIsALetter(arg10);
    var v1: Boolean = true;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "eeeee"
    var x2: Boolean = checkIfLastCharIsALetter(arg20);
    var v2: Boolean = false;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "A"
    var x3: Boolean = checkIfLastCharIsALetter(arg30);
    var v3: Boolean = true;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "Pumpkin pie "
    var x4: Boolean = checkIfLastCharIsALetter(arg40);
    var v4: Boolean = false;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "Pumpkin pie 1"
    var x5: Boolean = checkIfLastCharIsALetter(arg50);
    var v5: Boolean = false;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = ""
    var x6: Boolean = checkIfLastCharIsALetter(arg60);
    var v6: Boolean = false;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: String = "eeeee e "
    var x7: Boolean = checkIfLastCharIsALetter(arg70);
    var v7: Boolean = false;
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: String = "apple pie"
    var x8: Boolean = checkIfLastCharIsALetter(arg80);
    var v8: Boolean = false;
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: String = "apple pi e "
    var x9: Boolean = checkIfLastCharIsALetter(arg90);
    var v9: Boolean = false;
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }


}

