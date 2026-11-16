fun minsubarraysum(nums : List<Long>) : Long {
    var answer = nums[0]
	nums.indices.forEach { i ->
        nums.indices.forEach { j ->
            if (i <= j) {
                answer = Math.min(nums.subList(i, j + 1).sum(), answer)
            }
        }
    }
    return answer
}

