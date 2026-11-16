fun intToMiniRoman(number : Int) : String {
    val romanNumerals = listOf(
        1000 to "m",
        900 to "cm",
        500 to "d",
        400 to "cd",
        100 to "c",
        90 to "xc",
        50 to "l",
        40 to "xl",
        10 to "x",
        9 to "ix",
        5 to "v",
        4 to "iv",
        1 to "i"
    )
    var num = number
    val romanStringBuilder = StringBuilder()

    for ((value, numeral) in romanNumerals) {
        while (num >= value) {
            num -= value
            romanStringBuilder.append(numeral)
        }
    }

    return romanStringBuilder.toString()
}

