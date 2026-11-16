fun fileNameCheck(fileName : String) : String {
    val parts = fileName.split('.')

    if (parts.size != 2 || parts[0].isEmpty() || !parts[0][0].isLetter()) {
        return "No"
    }
    if (parts[0].count { it.isDigit() } > 3) {
        return "No"
    }
    val validExtensions = setOf("txt", "exe", "dll")
    if (parts[1] !in validExtensions) {
        return "No"
    }

    return "Yes"
}

