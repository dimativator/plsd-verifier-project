fun main() {
    var arg10 : List<String> = mutableListOf("3", "11111111")
    var x1 : List<String> = oddCount(arg10);
    var v1 : List<String> = mutableListOf("the number of odd elements 1n the str1ng 1 of the 1nput.", "the number of odd elements 8n the str8ng 8 of the 8nput.");
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<String> = mutableListOf("271", "137", "314")
    var x2 : List<String> = oddCount(arg20);
    var v2 : List<String> = mutableListOf("the number of odd elements 2n the str2ng 2 of the 2nput.", "the number of odd elements 3n the str3ng 3 of the 3nput.", "the number of odd elements 2n the str2ng 2 of the 2nput.");
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }


}

