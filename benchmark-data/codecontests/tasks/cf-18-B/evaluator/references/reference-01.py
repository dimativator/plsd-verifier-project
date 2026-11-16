class Platforms:
    @classmethod
    def read_input(cls):
        nums = list(map(int, input('').split()))
        return nums[0], nums[1], nums[2], nums[3]

    @classmethod
    def run(cls):
        n, d, m, l = cls.read_input()
        end_plat = (n - 1) * m + l
        for cur_jump in range(d, (m + 1) * d, d):
            if (cur_jump % m) > l or cur_jump > end_plat:
                print(cur_jump)
                return
        print(end_plat - (end_plat % d) + d)

if __name__ == "__main__":
    Platforms.run()


