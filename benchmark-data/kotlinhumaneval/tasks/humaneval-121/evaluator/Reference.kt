fun validDate(date : String) : Boolean {
    val regex = Regex("""\d{2}-\d{2}-\d{4}""")
    if (!regex.matches(date)) return false

    val (month, day, year) = date.split("-").map { it.toInt() }

    if (month !in 1..12) return false

    val daysInMonth = when (month) {
        4, 6, 9, 11 -> 30
        2 -> 29 // Not accounting for leap years
        else -> 31
    }

    if (day !in 1..daysInMonth) return false

    return true
}

