fun main() {
    var arg10: List<Double> = mutableListOf(1.2)
    var x1: List<String> = numericalLetterGrade(arg10)
    var v1: List<String> = mutableListOf("D+")
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: List<Double> = mutableListOf(0.5)
    var x2: List<String> = numericalLetterGrade(arg20)
    var v2: List<String> = mutableListOf("D-")
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30: List<Double> = mutableListOf(0.0)
    var x3: List<String> = numericalLetterGrade(arg30)
    var v3: List<String> = mutableListOf("E")
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40: List<Double> = mutableListOf(1.0, 0.3, 1.5, 2.8, 3.3)
    var x4: List<String> = numericalLetterGrade(arg40)
    var v4: List<String> = mutableListOf("D", "D-", "C-", "B", "B+")
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50: List<Double> = mutableListOf(0.0, 0.7)
    var x5: List<String> = numericalLetterGrade(arg50)
    var v5: List<String> = mutableListOf("E", "D-")
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }


}

