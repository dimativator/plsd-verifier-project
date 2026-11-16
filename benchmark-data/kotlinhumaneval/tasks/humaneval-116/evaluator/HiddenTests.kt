fun main() {
    var arg10 : List<String> = mutableListOf(")", ")")
    var x1 : String = matchParens(arg10);
    var v1 : String = "No";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : List<String> = mutableListOf("(()(())", "())())")
    var x2 : String = matchParens(arg20);
    var v2 : String = "No";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : List<String> = mutableListOf(")())", "(()()(")
    var x3 : String = matchParens(arg30);
    var v3 : String = "Yes";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : List<String> = mutableListOf("(())))", "(()())((")
    var x4 : String = matchParens(arg40);
    var v4 : String = "Yes";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : List<String> = mutableListOf("()", "())")
    var x5 : String = matchParens(arg50);
    var v5 : String = "No";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : List<String> = mutableListOf("(()(", "()))()")
    var x6 : String = matchParens(arg60);
    var v6 : String = "Yes";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : List<String> = mutableListOf("((((", "((())")
    var x7 : String = matchParens(arg70);
    var v7 : String = "No";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : List<String> = mutableListOf(")(()", "(()(")
    var x8 : String = matchParens(arg80);
    var v8 : String = "No";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }

    var arg90 : List<String> = mutableListOf(")(", ")(")
    var x9 : String = matchParens(arg90);
    var v9 : String = "No";
    if (x9 != v9) {
        throw Exception("Exception -- test case 9 did not pass. x9 = " + x9)
    }

    var arg100 : List<String> = mutableListOf("(", ")")
    var x10 : String = matchParens(arg100);
    var v10 : String = "Yes";
    if (x10 != v10) {
        throw Exception("Exception -- test case 10 did not pass. x10 = " + x10)
    }

    var arg110 : List<String> = mutableListOf(")", "(")
    var x11 : String = matchParens(arg110);
    var v11 : String = "Yes";
    if (x11 != v11) {
        throw Exception("Exception -- test case 11 did not pass. x11 = " + x11)
    }


}

