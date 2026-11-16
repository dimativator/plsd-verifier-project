fun stringToMd5(text : String) : String? {

    if (text.isEmpty()) return null

    // Get MD5 MessageDigest instance
    val md = java.security.MessageDigest.getInstance("MD5")

    // Digest the input string bytes, then convert the digest bytes to a hex string
    val hashBytes = md.digest(text.toByteArray())
    return hashBytes.joinToString(separator = "") { byte -> "%02x".format(byte) }
}

