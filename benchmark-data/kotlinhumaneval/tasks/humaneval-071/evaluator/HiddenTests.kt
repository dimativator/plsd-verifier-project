fun main() {
    var arg10: List<String> = mutableListOf("hi", "admin")
    var arg11: List<String> = mutableListOf("hi", "hi")
    var x1: List<String> = totalMatch(arg10, arg11)
    var v1: List<String> = mutableListOf("hi", "hi")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<String> = mutableListOf("hi", "admin")
    var arg21: List<String> = mutableListOf("hi", "hi", "admin", "project")
    var x2: List<String> = totalMatch(arg20, arg21)
    var v2: List<String> = mutableListOf("hi", "admin")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<String> = mutableListOf("4")
    var arg31: List<String> = mutableListOf("1", "2", "3", "4", "5")
    var x3: List<String> = totalMatch(arg30, arg31)
    var v3: List<String> = mutableListOf("4")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<String> = mutableListOf("hi", "admin")
    var arg41: List<String> = mutableListOf("hI", "Hi")
    var x4: List<String> = totalMatch(arg40, arg41)
    var v4: List<String> = mutableListOf("hI", "Hi")
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<String> = mutableListOf("hi", "admin")
    var arg51: List<String> = mutableListOf("hI", "hi", "hi")
    var x5: List<String> = totalMatch(arg50, arg51)
    var v5: List<String> = mutableListOf("hI", "hi", "hi")
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60: List<String> = mutableListOf("hi", "admin")
    var arg61: List<String> = mutableListOf("hI", "hi", "hii")
    var x6: List<String> = totalMatch(arg60, arg61)
    var v6: List<String> = mutableListOf("hi", "admin")
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70: List<String> = mutableListOf()
    var arg71: List<String> = mutableListOf("this")
    var x7: List<String> = totalMatch(arg70, arg71)
    var v7: List<String> = mutableListOf()
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80: List<String> = mutableListOf("this")
    var arg81: List<String> = mutableListOf()
    var x8: List<String> = totalMatch(arg80, arg81)
    var v8: List<String> = mutableListOf()
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

