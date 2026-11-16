fun main() {
    var arg10 : String = "Earth"
    var arg11 : String = "Mercury"
    var x1 : List<String> = bf(arg10, arg11);
    var v1 : List<String> = mutableListOf("Venus");
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "Mercury"
    var arg21 : String = "Uranus"
    var x2 : List<String> = bf(arg20, arg21);
    var v2 : List<String> = mutableListOf("Venus", "Earth", "Mars", "Jupiter", "Saturn");
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "Neptune"
    var arg31 : String = "Venus"
    var x3 : List<String> = bf(arg30, arg31);
    var v3 : List<String> = mutableListOf("Earth", "Mars", "Jupiter", "Saturn", "Uranus");
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "Earth"
    var arg41 : String = "Earth"
    var x4 : List<String> = bf(arg40, arg41);
    var v4 : List<String> = mutableListOf();
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "Mars"
    var arg51 : String = "Earth"
    var x5 : List<String> = bf(arg50, arg51);
    var v5 : List<String> = mutableListOf();
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "Jupiter"
    var arg61 : String = "Makemake"
    var x6 : List<String> = bf(arg60, arg61);
    var v6 : List<String> = mutableListOf();
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

