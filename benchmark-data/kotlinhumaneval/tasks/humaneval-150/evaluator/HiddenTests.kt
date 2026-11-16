fun main() {
    var arg10 : String = "Boku123"
    var arg11 : List<String> = mutableListOf("nani", "NazeDa", "YEs.WeCaNe", "32145tggg")
    var x1 : String = strongestExtension(arg10, arg11);
    var v1 : String = "Boku123.YEs.WeCaNe";
    if (x1 != v1) {
        throw Exception("Exception -- test case 1 did not pass. x1 = " + x1)
    }

    var arg20 : String = "__YESIMHERE"
    var arg21 : List<String> = mutableListOf("t", "eMptY", "nothing", "zeR00", "NuLl__", "123NoooneB321")
    var x2 : String = strongestExtension(arg20, arg21);
    var v2 : String = "__YESIMHERE.NuLl__";
    if (x2 != v2) {
        throw Exception("Exception -- test case 2 did not pass. x2 = " + x2)
    }

    var arg30 : String = "K"
    var arg31 : List<String> = mutableListOf("Ta", "TAR", "t234An", "cosSo")
    var x3 : String = strongestExtension(arg30, arg31);
    var v3 : String = "K.TAR";
    if (x3 != v3) {
        throw Exception("Exception -- test case 3 did not pass. x3 = " + x3)
    }

    var arg40 : String = "__HAHA"
    var arg41 : List<String> = mutableListOf("Tab", "123", "781345", "-_-")
    var x4 : String = strongestExtension(arg40, arg41);
    var v4 : String = "__HAHA.123";
    if (x4 != v4) {
        throw Exception("Exception -- test case 4 did not pass. x4 = " + x4)
    }

    var arg50 : String = "YameRore"
    var arg51 : List<String> = mutableListOf("HhAas", "okIWILL123", "WorkOut", "Fails", "-_-")
    var x5 : String = strongestExtension(arg50, arg51);
    var v5 : String = "YameRore.okIWILL123";
    if (x5 != v5) {
        throw Exception("Exception -- test case 5 did not pass. x5 = " + x5)
    }

    var arg60 : String = "finNNalLLly"
    var arg61 : List<String> = mutableListOf("Die", "NowW", "Wow", "WoW")
    var x6 : String = strongestExtension(arg60, arg61);
    var v6 : String = "finNNalLLly.WoW";
    if (x6 != v6) {
        throw Exception("Exception -- test case 6 did not pass. x6 = " + x6)
    }

    var arg70 : String = "_"
    var arg71 : List<String> = mutableListOf("Bb", "91245")
    var x7 : String = strongestExtension(arg70, arg71);
    var v7 : String = "_.Bb";
    if (x7 != v7) {
        throw Exception("Exception -- test case 7 did not pass. x7 = " + x7)
    }

    var arg80 : String = "Sp"
    var arg81 : List<String> = mutableListOf("671235", "Bb")
    var x8 : String = strongestExtension(arg80, arg81);
    var v8 : String = "Sp.671235";
    if (x8 != v8) {
        throw Exception("Exception -- test case 8 did not pass. x8 = " + x8)
    }


}

