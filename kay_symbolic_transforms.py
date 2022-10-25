import sympy as sp
sp.init_printing(use_unicode=True)
import math

 
# ------------------------- roundExpr -------------------------------------
# 
# If you need to round a sympy expression down to fewer decimal places
# 
# Based on https://stackoverflow.com/questions/48491577/printing-the-output-rounded-to-3-decimals-in-sympy
def roundExpr(expr, num_decimal_places=3):
    return expr.xreplace({n : round(n, num_decimal_places) for n in expr.atoms(sp.Number)})


# ------------------------- isCloseToEqual -----------------------------------
#
# Lets you know if two matrices or vectors are close to equal by rounding and
# placewise checking
#
def isCloseToEqual(thingOne, thingTwo, num_decimal_places=3):
    # Make sure they are the same shape:
    if sp.shape(thingOne)!= sp.shape(thingTwo):
        return False
    else:
        dims = sp.shape(thingOne)
    
    # Now let's round both of them
    roundedOne = roundExpr(thingOne, num_decimal_places)
    roundedTwo = roundExpr(thingTwo, num_decimal_places)
    
    # And finally test elementwise equality and hope for the best
    if roundedOne.equals(roundedTwo):
        return True
    else:
        return False
    
    
       
    
    


#----------------------- makeSpTransform --------------------------------
# Create a 4x4 homogeneous transform (represented as a 4x4 numpy matrix) 
# 
# Input arguments: 4 tuples of length 3
# Use these arguments as column vectors and filling in the 0,0,0,1 for the 
# last row
#
# Note: I used tuples here so that the interface would be the same 
# as the makeTransform one
# 
def makeSpTransform(xDirection, yDirection, zDirection, originLocation):
    assert isinstance(originLocation, tuple), "Arguments to makeSPTransform must be tuples"
    assert isinstance(xDirection, tuple), "Arguments to makeSPTransform must be tuples"
    assert isinstance(yDirection, tuple), "Arguments to makeSPTransform must be tuples"
    assert isinstance(zDirection, tuple), "Arguments to makeSPTransform must be tuples"
    assert len(xDirection) == 3, "Args to makeSPTransform must be tuples of len==3"
    assert len(yDirection) == 3, "Args to makeSPTransform must be tuples of len==3"
    assert len(zDirection) == 3, "Args to makeSPTransform must be tuples of len==3"
    assert len(originLocation) == 3, "Args to makeSPTransform must be tuples of len==3"
    
    # Convert everything to list
    xDir = list(xDirection)
    xDir.append(0)
    yDir = list(yDirection)
    yDir.append(0)
    zDir = list(zDirection)
    zDir.append(0)
    originLoc = list(originLocation)
    originLoc.append(1)
    
    mx = sp.Matrix([xDir, yDir, zDir, originLoc])
    mx = mx.T
    return mx

    
#----------------------- makeSpIdentityTransform --------------------------------
# A quick way to make a 4x4 identity matrix
#
def makeSpIdentityTransform():
    return sp.eye(4)


# -------------------- makeSpPoint ------------------------------------------
# Take the x, y, z values (as ints or floats) and return a vertical 4x1 sympy vector
# (with 1 as the bottom value, of course)
#
def makeSpPoint(a,b,c):
    checkLegitType(a, "makeSpPoint")
    checkLegitType(b, "makeSpPoint")
    checkLegitType(c, "makeSpPoint")
    
    point = sp.Matrix([a,b,c,1])
    return point


# --------------------- spTrans ---------------------------------------
#
# This method takes as input three ints or floats u, v, and w which represent
# the x,y,z values and returns the corresponding 4x4 homogenious transformation matrix.
def spTrans(u,v,w):
    checkLegitType(u, "spTrans")
    checkLegitType(v, "spTrans")
    checkLegitType(w, "spTrans")

    t = sp.eye(4)
    t.col_del(3)
    t = t.col_insert(3, sp.Matrix([u,v,w,1]))
    return t


# -------------------------- Rotations -----------------------------------------
# A pile of rotation matrices, for your convenience offered in radians and degrees 
# All of them, of course, return a 4x4 rotation matrix

def convertDegToRad(val):
    checkLegitType(val, "convertDegToRad")    
    return val * math.pi / 180.0 
    

def radiansSpRotX(rad):
    checkLegitType(rad, "radiansSpRotX")    
    x = (1,0,0)
    y = (0, sp.cos(rad), sp.sin(rad))
    z = (0, -1*sp.sin(rad), sp.cos(rad))
    t = (0,0,0)
    return makeSpTransform(x,y,z,t)

    
def degreesSpRotX(deg):
    checkLegitType(deg, "degreesSpRotX")    
    rad = convertDegToRad(deg)
    return radiansSpRotX(rad)


def radiansSpRotY(rad):
    checkLegitType(rad, "radiansSpRotY")    
    x = (sp.cos(rad), 0, -1*sp.sin(rad))
    y = (0,1,0)
    z = (sp.sin(rad), 0, sp.cos(rad))
    t = (0,0,0)
    return makeSpTransform(x,y,z,t)
       

def degreesSpRotY(deg):
    checkLegitType(deg, "degreesSpRotY")    
    rad = convertDegToRad(deg)
    return radiansSpRotY(rad)
    
def radiansSpRotZ(rad):
    checkLegitType(rad, "radiansSpRotZ")
    x = (sp.cos(rad), sp.sin(rad),0)
    y = (-1*sp.sin(rad), sp.cos(rad), 0)
    z = (0,0,1)
    t = (0,0,0)
    return makeSpTransform(x,y,z,t)
       
def degreesSpRotZ(deg):
    checkLegitType(deg, "degreesSPRotZ")   
    rad = convertDegToRad(deg)
    return radiansSpRotZ(rad)


#----------------------------------- checkLegitType -------------------------------------------
# 
# Confirm that the parameter is a legitimate type for sympy
# 
# Note: If type is None, then it checks for:
#       int
#       float
#       sp.core.symbol.Symbol
#       sp.core.mul.Mul
#
# I may be missing something ... so I've put the DO_SP_ASSERTION_CHECKS in here to turn off easily 
# If necessary
#
def checkLegitType(item, functionName="this function", itemType=None):
    DO_SP_ASSERTION_CHECKS = True   # just to make it easy to turn off if need be ...
       
    if DO_SP_ASSERTION_CHECKS: 
        if itemType==None:
            itemType = (int,float, sp.core.symbol.Symbol, sp.core.mul.Mul, sp.core.add.Add)
            
        assert isinstance(itemType, tuple), "checkLegitType got passed a bad itemType"
        
        message = "Problem with arguments to " + functionName + " types should be one of:\n"
        for i in itemType:
            message = message + str(i) + "\n"
        
        message = message + "\n\nNote: Check the types of your arguments using the python\ntype() "
        message = message + "\nmethod and if you don't see it as one of the ones listed above and you think it should be good\n"
        message = message + "then you can edit the checkLegitType method inside \n"
        message = message + "of kay_sympolic_transforms and set DO_SP_ASSERTION_CHECKS to False \n"
        message = message + "to turn off this warning\n*****(and contact Dr. Kay)!!******* "
        
        assert isinstance(item, itemType), message
        
  



