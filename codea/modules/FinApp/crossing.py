# determines if one feature is crossing another

def crossing(feature1, feature2):
    # create feature for feature ema crossing feature
    poscross = [0] # positive cross
    negcross = [0] # negative cross
    higher = [0] # ema higher than feature

    for i in range (1, len(feature1)):
        # check if ema is crossing feature
        if feature1[i-1] < feature2[i-1] and feature1[i] > feature2[i]:
            poscross.append(1)
            negcross.append(0)
        elif feature1[i-1] > feature2[i-1] and feature1[i] < feature2[i]:
            poscross.append(0)
            negcross.append(1)
        else:
            poscross.append(0)
            negcross.append(0)

        # check if ema is higher or lower than feature
        if feature1[i] > feature2[i]:
            higher.append(1)
        else:
            higher.append(0)
    return poscross, negcross, higher
