from sys import stdin


REPLACE_ID = 1
REVERSE_ID = 2
SWAP_ID = 3
SUM_ID = 4


def main():
    n, q = _read_ints()
    a = tuple(_read_ints())
    requests = tuple(_read_ints() for _ in range(q))
    for result in compute_requests_results(a, requests):
        print(result)


def _read_ints():
    return map(int, stdin.readline().split(" "))


def compute_requests_results(initial_array, requests):
    tree = _Tree(initial_array)
    for request_id, *request_args in requests:
        if request_id == REPLACE_ID:
            index, new_value = request_args
            tree[index-1] = new_value
        elif request_id == REVERSE_ID:
            k, = request_args
            tree.reverse(k)
        elif request_id == SWAP_ID:
            k, = request_args
            tree.swap(k)
        else:
            assert request_id == SUM_ID
            l, r = request_args
            yield tree.find_sum(l-1, r-1)


class _Tree:
    
    def __init__(self, array):
        array = list(array)
        self._levels = [array]
        self._levels_sizes = [len(array)]
        self._nodes_sizes = [1]
        while self._levels_sizes[-1] > 1:
            last_size = self._levels_sizes[-1]
            last_level = self._levels[-1]
            last_node_size = self._nodes_sizes[-1]
            
            new_size = last_size // 2
            new_level = [last_level[2*i] + last_level[2*i+1] for i in range(new_size)]
            new_node_size = last_node_size * 2
            
            self._levels_sizes.append(new_size)
            self._levels.append(new_level)
            self._nodes_sizes.append(new_node_size)
        
        self._levels = tuple(self._levels)
        self._is_swapped = [False for level in self._levels]
    
    def __getitem__(self, index):
        i_curr_level = len(self._levels) - 1
        curr_node_index = 0
        while i_curr_level > 0:
            curr_node_index = self._get_subnode_index(curr_node_index, i_curr_level, index)
            i_curr_level -= 1
        
        return self._levels[i_curr_level][curr_node_index]
    
    def __setitem__(self, index, value):
        old_value = self[index]
        delta = value - old_value
        
        i_curr_level = len(self._levels) - 1
        curr_node_index = 0
        while i_curr_level > 0:
            self._levels[i_curr_level][curr_node_index] += delta
            curr_node_index = self._get_subnode_index(curr_node_index, i_curr_level, index)
            i_curr_level -= 1
        
        self._levels[i_curr_level][curr_node_index] += delta
    
    def _get_subnode_index(self, curr_node_index, i_curr_level, final_index):
        old_node_size = self._nodes_sizes[i_curr_level]
        i_new_level = i_curr_level - 1
        new_node_size = self._nodes_sizes[i_new_level]
        is_right = final_index % old_node_size >= new_node_size
        if self._is_swapped[i_curr_level]:
            is_right = not is_right
        new_node_index = curr_node_index * 2 + (1 if is_right else 0)
        return new_node_index
    
    def find_sum(self, l, r):
        return self._find_sum_before(r+1) - self._find_sum_before(l)
    
    def _find_sum_before(self, index):
        if index == len(self._levels[0]):
            return self._levels[-1][0]
        
        result_sum = 0
        
        i_curr_level = len(self._levels) - 1
        curr_node_index = 0
        while i_curr_level > 0:
            curr_node_size = self._nodes_sizes[i_curr_level]
            i_new_level = i_curr_level - 1
            new_node_size = self._nodes_sizes[i_new_level]
            is_right = 1 if index % curr_node_size >= new_node_size else 0
            is_swapped = self._is_swapped[i_curr_level]
            new_node_index = curr_node_index * 2 + (is_right if not is_swapped else 1 - is_right)
            denied_node_index = curr_node_index * 2 + (is_right if is_swapped else 1 - is_right)
            if is_right:
                result_sum += self._levels[i_new_level][denied_node_index]
            
            i_curr_level = i_new_level
            curr_node_index = new_node_index
        
        return result_sum
    
    def swap(self, k):
        self._is_swapped[k+1] = not self._is_swapped[k+1]

    def reverse(self, k):
        for i in range(k):
            self.swap(i)


if __name__ == '__main__':
    main()
