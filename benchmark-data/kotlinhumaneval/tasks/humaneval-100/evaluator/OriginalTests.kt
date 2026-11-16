fun main() {
    var arg00: Int = 1
    var arg01: Int = 5
    var x0: String = roundedAvg(arg00, arg01);
    var v0: String = "0b11";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: Int = 7
    var arg11: Int = 13
    var x1: String = roundedAvg(arg10, arg11);
    var v1: String = "0b1010";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: Int = 964
    var arg21: Int = 977
    var x2: String = roundedAvg(arg20, arg21);
    var v2: String = "0b1111001010";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: Int = 996
    var arg31: Int = 997
    var x3: String = roundedAvg(arg30, arg31);
    var v3: String = "0b1111100100";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: Int = 560
    var arg41: Int = 851
    var x4: String = roundedAvg(arg40, arg41);
    var v4: String = "0b1011000001";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: Int = 185
    var arg51: Int = 546
    var x5: String = roundedAvg(arg50, arg51);
    var v5: String = "0b101101101";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: Int = 362
    var arg61: Int = 496
    var x6: String = roundedAvg(arg60, arg61);
    var v6: String = "0b110101101";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: Int = 350
    var arg71: Int = 902
    var x7: String = roundedAvg(arg70, arg71);
    var v7: String = "0b1001110010";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: Int = 197
    var arg81: Int = 233
    var x8: String = roundedAvg(arg80, arg81);
    var v8: String = "0b11010111";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90: Int = 7
    var arg91: Int = 5
    var x9: String = roundedAvg(arg90, arg91);
    var v9: String = "-1";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100: Int = 5
    var arg101: Int = 1
    var x10: String = roundedAvg(arg100, arg101);
    var v10: String = "-1";
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110: Int = 5
    var arg111: Int = 5
    var x11: String = roundedAvg(arg110, arg111);
    var v11: String = "0b101";
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

