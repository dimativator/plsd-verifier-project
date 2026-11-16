fun parseMusic(musicString: String): List<Any> {
    if (musicString.length == 0) {
        return emptyList()
    }
    return musicString.split(" ").map { note ->
        when (note) {
            "o" -> 4
            "o|" -> 2
            ".|" -> 1
            else -> throw Exception("Invalid input")
        }
    }
}

