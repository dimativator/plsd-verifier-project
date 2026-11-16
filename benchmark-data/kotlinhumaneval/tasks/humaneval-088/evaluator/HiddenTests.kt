fun main() {
    var arg10: String = "Is the sky blue?"
    var x1: Int = isBored(arg10)
    var v1: Int = 0
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "I love It !"
    var x2: Int = isBored(arg20)
    var v2: Int = 1
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: String = "bIt"
    var x3: Int = isBored(arg30)
    var v3: Int = 0
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: String = "I feel good today. I will be productive. will kill It"
    var x4: Int = isBored(arg40)
    var v4: Int = 2
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: String = "You and I are going for a walk"
    var x5: Int = isBored(arg50)
    var v5: Int = 0
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

