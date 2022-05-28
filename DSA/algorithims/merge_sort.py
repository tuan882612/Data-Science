def out(nums):
    if len(nums)>1:
        right, left = nums[:len(nums)//2], nums[len(nums)//2:]
        out(left)  
        out(right)
              
        i, j, k = 0, 0, 0
        while i<len(left) and j<len(right):
            if left[i] > right[j]:
                nums[k] = right[j]
                j+=1
            else:
                nums[k] = left[i]
                i+=1
            k+=1
        
        while i<len(left):
            nums[k] = left[i]
            i+=1
            k+=1
        
        while j<len(right):
            nums[k] = right[j]
            j+=1
            k+=1
          
arr = [
    [],
    [],
    [10, 12],
    [],
    [3, 3, 13],
    [3],
    [10],
    [0, 7]
]
out(arr)
print(arr)