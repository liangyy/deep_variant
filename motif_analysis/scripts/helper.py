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

def draw_from_gc_score_dist(pos_hist, neg_hist, pos_idx, neg_idx, pos, neg, num):
    index = [ i for i in range(1, 21) ]
    x_pos_idx = []
    x_neg_idx = []
    i = 0
    while i < num:
        gc_rand = np.random.multinomial(1, gc_dist)
        gc_idx = (gc_rand * index).sum()
        if neg_hist[gc_idx -1, :].sum() == 0 or pos_hist[gc_idx -1, :].sum() == 0:
            continue
        selected_pos_idx = _draw_from_score(gc_idx, pos_idx, pos)
        selected_neg_idx = _draw_from_score(gc_idx, neg_idx, neg)
        x_pos_idx.append(selected_pos_idx)
        x_neg_idx.append(selected_neg_idx)
        i += 1
    return x_pos_idx, x_neg_idx

def _draw_from_score(gc_idx, pos_idx, pos, mode):
    selected_set = np.where(pos_idx[0] == gc_idx)[0]
    selected = pos.loc[selected_set].reset_index()
    probs = selected['y.predict'] * selected['y'] + (1 - selected['y.predict']) * (1 - selected['y'])
    sample_rand = np.random.multinomial(1, probs / probs.sum())
    selected_sample = selected.loc[np.where(sample_rand == 1)[0]]
    return selected_sample['index'].as_matrix()[0]
