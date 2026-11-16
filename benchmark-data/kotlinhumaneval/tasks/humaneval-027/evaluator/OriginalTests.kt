fun main() {
    var arg00: String = ""
    var x0: String = flipCase(arg00)
    var v0: String = ""
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10: String = "Hello!"
    var x1: String = flipCase(arg10)
    var v1: String = "hELLO!"
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20: String = "These violent delights have violent ends"
    var x2: String = flipCase(arg20)
    var v2: String = "tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS"
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

