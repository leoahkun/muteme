def area(p1, p2):
    # print(p2[0],p1[0],p2[1],p1[1])
    area = (p2[0]-p1[0]) * (p2[1]-p1[1])
    return area

def intersection_area(a_p1, a_p2, b_p1, b_p2):
    x = 0
    y = 1
 
    # Area of 1st Rectangle
    area1 = area(a_p1, a_p2)
    area1 = area(b_p1, b_p2)
     
    dw = (min(a_p2[x], b_p2[x]) -
              max(a_p1[x], b_p1[x]))
 
    dh = (min(a_p2[y], b_p2[y]) -
              max(a_p1[y], b_p1[y]))
    areaI = 0
    if dw > 0 and dh > 0:
        areaI = dw * dh
 
    return areaI

def intersection_percentage(a_p1, a_p2, b_p1, b_p2):
    ia = intersection_area(a_p1,a_p2,b_p1,b_p2)
    return ia/area(a_p1,a_p2)

def box_occupied(box_p1, box_p2, p1, p2, threshold=0.3):    
    ip = intersection_percentage(box_p1, box_p2, p1, p2)    
    if ip > threshold:
        return True
    return False