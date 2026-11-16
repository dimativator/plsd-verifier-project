fun splitWords(txt : String) : Any {
    if (txt.contains(" ")) {
        return txt.split("\\s+".toRegex())
    }
    if (txt.contains(",")) {
        return txt.split(",")
    }
    val count = txt.count { it in 'a'..'z' && (it - 'a') % 2 == 1 }
    return count
}

