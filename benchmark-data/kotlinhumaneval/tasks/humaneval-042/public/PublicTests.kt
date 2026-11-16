fun main() {
    var arg00: Int = 8
    var arg01: Int = 3
    var x0: String = changeBase(arg00, arg01)
    var v0: String = "22"
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
