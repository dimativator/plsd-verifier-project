fun main() {
    var arg00: List<Double> = mutableListOf(4.0, 3.0, 1.7, 2.0, 3.5)
    var x0: List<String> = numericalLetterGrade(arg00)
    var v0: List<String> = mutableListOf("A+", "B", "C-", "C", "A-")
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
