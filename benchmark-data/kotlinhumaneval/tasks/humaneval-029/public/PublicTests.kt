fun main() {
    var arg00: List<String> = mutableListOf()
    var arg01: String = "john"
    var x0: List<String> = filterByPrefix(arg00, arg01)
    var v0: List<String> = mutableListOf()
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }
}
