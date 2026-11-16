fun main() {
    var arg00 : String = "Hello world"
    var x0 : String? = stringToMd5(arg00);
    var v0 : String? = "3e25960a79dbc69b674cd4ec67a72c62";
    if (x0 != v0) {
        throw Exception("Exception -- test case 0 did not pass. x0 = " + x0)
    }

    var arg10 : String = ""
    var x1 : String? = stringToMd5(arg10);
    var v1 : String? = null;
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "A B C"
    var x2 : String? = stringToMd5(arg20);
    var v2 : String? = "0ef78513b0cb8cef12743f5aeb35f888";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "password"
    var x3 : String? = stringToMd5(arg30);
    var v3 : String? = "5f4dcc3b5aa765d61d8327deb882cf99";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }


}

