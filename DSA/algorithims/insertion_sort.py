def func(nums, target):
    left, right = 0, len(nums)-1
    while left<=right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return left

if __name__=="__main__":
    print(func([1,3,5,6], target = 7))