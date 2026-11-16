fun strongestExtension(className : String, extensions : List<String>) : String {
    var strongestExtension = ""
    var maxStrength = Int.MIN_VALUE

    extensions.forEach { extension ->
        val strength = extension.count { it.isUpperCase() } - extension.count { it.isLowerCase() }
        if (strength > maxStrength) {
            strongestExtension = extension
            maxStrength = strength
        }
    }

    return "$className.$strongestExtension"
}

