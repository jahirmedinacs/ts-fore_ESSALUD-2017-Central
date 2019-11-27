# DEBUG

import random
import numpy as np

def random_noise(data, error_rate):
    output = []
    worth = [ i % (2 * random.random()) for i in range(int(np.floor(100/error_rate)))]

    [fail, change] = [0, 0]

    for index  in range(len(data)):
        if not random.choice(worth):
            output.append(np.int32( data[index] * random.random() ))
                
            change += 1
        else:
            fail += 1
            output.append(data[index])
            
    
    print("Not Changed" ,fail / len(data), "Changed", change / len(data) )
    
    return output