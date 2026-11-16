fun main() {
    var arg10: String = "5 apples and 6 oranges"
    var arg11: Int = 21
    var x1: Int = fruitDistribution(arg10, arg11)
    var v1: Int = 10
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "0 apples and 1 oranges"
    var arg21: Int = 3
    var x2: Int = fruitDistribution(arg20, arg21)
    var v2: Int = 2
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "1 apples and 0 oranges"
    var arg31: Int = 3
    var x3: Int = fruitDistribution(arg30, arg31)
    var v3: Int = 2
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "2 apples and 3 oranges"
    var arg41: Int = 100
    var x4: Int = fruitDistribution(arg40, arg41)
    var v4: Int = 95
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "2 apples and 3 oranges"
    var arg51: Int = 5
    var x5: Int = fruitDistribution(arg50, arg51)
    var v5: Int = 0
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: String = "1 apples and 100 oranges"
    var arg61: Int = 120
    var x6: Int = fruitDistribution(arg60, arg61)
    var v6: Int = 19
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

