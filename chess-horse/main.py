def run(target_x: int, target_y: int) -> int:
    if target_x < 0 or target_y < 0:
        return -1
        
    turns = min(target_x // 3, target_y // 3)
    
    current_x = turns * 3
    current_y = turns * 3
    
    movements = turns * 2
    
    rem_x = target_x - current_x
    rem_y = target_y - current_y
    
    if rem_x == 0 and rem_y == 0:
        return movements
        
    if rem_x == 2 and rem_y == 1:
        return movements + 1
        
    if rem_x == 1 and rem_y == 2:
        return movements + 1
        
    return -1


if __name__ == '__main__':
    import vendor

    vendor.launch(run)