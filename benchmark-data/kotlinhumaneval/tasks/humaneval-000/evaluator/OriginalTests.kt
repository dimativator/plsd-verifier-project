fun main() {
    var arg00: List<Double> = mutableListOf(1.0, 2.0, 3.9, 4.0, 5.0, 2.2)
    var arg01: Double = 0.3
    var x0: Boolean = hasCloseElements(arg00, arg01)
    var v0: Boolean = true
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: List<Double> = mutableListOf(1.0, 2.0, 3.9, 4.0, 5.0, 2.2)
    var arg11: Double = 0.05
    var x1: Boolean = hasCloseElements(arg10, arg11)
    var v1: Boolean = false
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Double> = mutableListOf(1.0, 2.0, 5.9, 4.0, 5.0)
    var arg21: Double = 0.95
    var x2: Boolean = hasCloseElements(arg20, arg21)
    var v2: Boolean = true
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Double> = mutableListOf(1.0, 2.0, 5.9, 4.0, 5.0)
    var arg31: Double = 0.8
    var x3: Boolean = hasCloseElements(arg30, arg31)
    var v3: Boolean = false
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Double> = mutableListOf(1.0, 2.0, 3.0, 4.0, 5.0, 2.0)
    var arg41: Double = 0.1
    var x4: Boolean = hasCloseElements(arg40, arg41)
    var v4: Boolean = true
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Double> = mutableListOf(1.1, 2.2, 3.1, 4.1, 5.1)
    var arg51: Double = 1.0
    var x5: Boolean = hasCloseElements(arg50, arg51)
    var v5: Boolean = true
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<Double> = mutableListOf(1.1, 2.2, 3.1, 4.1, 5.1)
    var arg61: Double = 0.5
    var x6: Boolean = hasCloseElements(arg60, arg61)
    var v6: Boolean = false
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

