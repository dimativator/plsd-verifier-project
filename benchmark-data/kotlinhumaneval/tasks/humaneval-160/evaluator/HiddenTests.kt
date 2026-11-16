fun main() {
    var arg10 : Int = 10
    var arg11 : Int = 2
    var x1 : List<Int> = generateIntegers(arg10, arg11);
    var v1 : List<Int> = mutableListOf(2, 4, 6, 8);
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : Int = 132
    var arg21 : Int = 2
    var x2 : List<Int> = generateIntegers(arg20, arg21);
    var v2 : List<Int> = mutableListOf(2, 4, 6, 8);
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : Int = 17
    var arg31 : Int = 89
    var x3 : List<Int> = generateIntegers(arg30, arg31);
    var v3 : List<Int> = mutableListOf();
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

