fun main() {
    var arg10 : List<Number> = mutableListOf(5, 4)
    var x1 : Int = doubleTheDifference(arg10);
    var v1 : Int = 25;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<Number> = mutableListOf(0.1, 0.2, 0.3)
    var x2 : Int = doubleTheDifference(arg20);
    var v2 : Int = 0;
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<Number> = mutableListOf(-10, -20, -30)
    var x3 : Int = doubleTheDifference(arg30);
    var v3 : Int = 0;
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<Number> = mutableListOf(-1, -2, 8)
    var x4 : Int = doubleTheDifference(arg40);
    var v4 : Int = 0;
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<Number> = mutableListOf(0.2, 3, 5)
    var x5 : Int = doubleTheDifference(arg50);
    var v5 : Int = 34;
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<Number> = mutableListOf(-99, -97, -95, -93, -91, -89, -87, -85, -83, -81, -79, -77, -75, -73, -71, -69, -67, -65, -63, -61, -59, -57, -55, -53, -51, -49, -47, -45, -43, -41, -39, -37, -35, -33, -31, -29, -27, -25, -23, -21, -19, -17, -15, -13, -11, -9, -7, -5, -3, -1, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99)
    var x6 : Int = doubleTheDifference(arg60);
    var v6 : Int = 166650;
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }


}

