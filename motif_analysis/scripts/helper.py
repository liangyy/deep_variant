def get_rough_threshold(y, num, mode):
    '''
    This function is specialized for finding top/lowest [num] values inside y
    in heuristic way. If the [divider] has been close to [num] enough, we will
    return [divider]
    '''
    diff_precentage = 0.1
    divider = 0.5
    jump_scale = 0.5
    if mode == 'min':
        y = - y
        divider = - divider
    while abs(divider) < 1 and abs(divider) > 0:
        rightnum = (y >= divider).sum()
        if _close_enough(rightnum, num, diff_precentage) is True:
            break
        else:
            jump_scale /= 2
            if rightnum > num:
                divider += jump_scale
            else:
                divider -= jump_scale
    if mode == 'min':
        divider = - divider
    return divider

def _close_enough(now, target, diff):
    left_bound = target * (1 - diff)
    right_bound = target * (1 + diff)
    if now >= left_bound and now <= right_bound:
        return True
    else:
        return False
