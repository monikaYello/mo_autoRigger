import pymel.core as pm
from mo_Utils.mo_logging import log_debug
from mo_Utils.mo_logging import log_info
import moRig_settings as settings


# copies from mo_riggUtils

def snap(driver, driven, typeCnx='parent', extraDrivers=(), skip=[]):
    '''
    snaps objects and skips locked attributes to prevent errors...
    also this doesnt uses constraints to snap..
    so The target objet could have keys if it is needed

    libUtil.snap('cube', 'target' , typeCnx='parent')

    Args:
         driver:
         driven:
         typeCnx:
             ['parent', 'parentCon', 1, 'p', 'P']
             ['point', 'translate', 3, 't', 'T']
             ['orient', 'rotate', 2, 'r', 'R']
             ['scale', 'Scale', 4, 's', 'S']
         extraDrivers:
         skip:

    Returns:
    '''

    drivers = [driver]
    drivers.extend(extraDrivers)

    for i, driver in enumerate(drivers):
        if not isinstance(driver, pm.PyNode):
            drivers[i] = pm.PyNode(driver)
    if not isinstance(driven, pm.PyNode):
        driven = pm.PyNode(driven)
    # skip memory
    skipMemory = []
    for s in skip:
        skipMemory.append(driven.attr(s).get())

    dummy = pm.duplicate(driven, n=driven + 'dummy', parentOnly=1)[0]
    for attr in ('t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz'):
        dummy.attr(attr).unlock()

    con = pm.parentConstraint(mo=0, *(drivers + [dummy]))
    con.interpType.set(2)
    pm.delete(con)
    # pm.delete(pm.parentConstraint(mo=0, *(drivers + [dummy]) ))
    pm.delete(pm.scaleConstraint(mo=0, *(drivers + [dummy])))
    # pm.delete( pm.parentConstraint(drivers, dummy, mo=0,))

    t = pm.getAttr(dummy + '.translate')
    r = pm.getAttr(dummy + '.rotate')
    s = pm.getAttr(dummy + '.scale')
    pm.delete(dummy)

    # PARENT
    if typeCnx in ['parent', 'parentCon', 1, 'p', 'P']:
        i = 0
        for at in ['tx', 'ty', 'tz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(t[i])
            i = i + 1
        i = 0
        for at in ['rx', 'ry', 'rz']:
            try:
                driven.attr(at).set(r[i])
            except:
                pass
            i = i + 1
    # ROTATE ONLY
    elif typeCnx in ['orient', 'rotate', 2, 'r', 'R']:
        i = 0
        for at in ['rx', 'ry', 'rz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(r[i])
            i = i + 1
    # TRANSLATE ONLY
    elif typeCnx in ['point', 'translate', 3, 't', 'T']:
        i = 0
        for at in ['tx', 'ty', 'tz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(t[i])
            i = i + 1
    # SCALE ONLY
    elif typeCnx in ['scale', 'Scale', 4, 's', 'S']:
        i = 0
        for at in ['sx', 'sy', 'sz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(s[i])
            i = i + 1
    # ALL
    elif typeCnx in ['all', 'All', 5, 'a', 'A']:
        i = 0
        for at in ['tx', 'ty', 'tz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(t[i])
            i = i + 1
        i = 0
        for at in ['rx', 'ry', 'rz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(r[i])
            i = i + 1
        i = 0
        for at in ['sx', 'sy', 'sz']:
            if driven.attr(at).isLocked() == 0:
                driven.attr(at).set(s[i])
            i = i + 1
    # skip memory
    i = 0
    for s in skip:
        driven.attr(s).set(skipMemory[i])
        i = i + 1
    pm.select(driven)


def cleanUpAttr(sel=None, listAttr=['sx', 'sy', 'sz', 'v'], l=1, k=1, cb=0):
    '''
    Args:
        sel:
        listAttr: ['sx', 'sy', 'sz', 'v']
        l: 1 lock attr , l=0 unlock attr
        k: 1  show attr ,k= 0 hide attr
        cb: 1 nonkeyable ,cb =0 make atte keyable
    Returns:
    riggUtil.cleanUpAttr(sel=[obj],listAttr=[
                         'sx', 'sy', 'sz', 'v'],l=0,k=0,cb=0)
    '''
    if sel == None:
        sel = pm.ls(sl=1)
    sel = pm.ls(sel)
    for obj in sel:
        # make pynode
        obj = pm.PyNode(obj)
        for attr in listAttr:
            if pm.objExists(obj + '.' + attr):
                obj.attr(attr).set(l=l, k=k, cb=cb)


def setWireAttributes(curve, aData):
    varKey = ""
    varStringVal = ""
    aStr = []
    # updates values on wires in form of {variableKey, varVal, variableKey2, varVal2}
    # use "&" to concatenate arrays
    i = 0
    for i in range(0, len(aData), 2):
        varKey = aData[i]
        varStringVal = aData[i + 1]
        if varKey == "wireScale":
            if varStringVal != "":
                if not pm.mel.attributeExists("wireScale", curve):
                    pm.addAttr(curve, ln="wireScale", hidden=True,
                               at='double', keyable=False, min=0)

                pm.setAttr((curve + ".wireScale"), (float(varStringVal)))

            elif pm.mel.attributeExists("wireScale", curve):
                pm.deleteAttr(curve + ".wireScale")

        elif varKey == "type":
            if varStringVal != "":
                if not pm.mel.attributeExists("type", curve):
                    pm.addAttr(curve, ln="type", dt="string",
                               hidden=True, keyable=False)

                pm.setAttr((curve + ".type"),
                           varStringVal, type="string")

            elif pm.mel.attributeExists("type", curve):
                pm.deleteAttr(curve + ".type")

        elif varKey == "wireFacingAxis":
            if varStringVal != "":
                if not pm.mel.attributeExists("wireFacingAxis", curve):
                    pm.addAttr(curve, ln="wireFacingAxis",
                               hidden=True, at='short', keyable=False)

                pm.setAttr((curve + ".wireFacingAxis"), (int(varStringVal)))

            elif pm.mel.attributeExists("wireFacingAxis", curve):
                pm.deleteAttr(curve + ".wireFacingAxis")


def copyWireAttributes(curve, mCtrl):
    maOffset = []
    # copies mirror wire attributes from curve to mCtrl
    aWireAtts = []
    if pm.mel.attributeExists("type", curve):
        aWireAtts.append("type")
        aWireAtts.append(str(pm.getAttr(curve + ".type")))

    if pm.mel.attributeExists("wireScale", curve):
        aWireAtts.append("wireScale")
        aWireAtts.append(str(str(pm.getAttr(curve + ".wireScale"))))

    if pm.mel.attributeExists("wireFacingAxis", curve):
        aWireAtts.append("wireFacingAxis")
        aWireAtts.append(str(str(pm.getAttr(curve + ".wireFacingAxis"))))

    abRTSetWireAttributes(mCtrl, aWireAtts)


# now add atts

def getMaxDim(obj):
    aBBox = pm.xform(obj, q=1, boundingBox=1, ws=1)
    # returns the max dimension of $obj boundingBox
    aDim = [abs(aBBox[3] - aBBox[0]), abs(aBBox[4] - aBBox[1]),
            abs(aBBox[5] - aBBox[2])]
    flt = 0.0
    max = float(0)
    for flt in aDim:
        if flt > max:
            max = float(flt)

    return max


def rigRootFolder():
    charName = settings.getGlobal["name"]
    # makes the root folder for all the riggery or returns it's path if it already exists
    folderName = charName + "_world"
    if not pm.objExists(folderName):
        pm.group(em=1, name=folderName)

    return folderName


def createNode(nodeType, baseName, prefix, limbName):
    suffix = ""
    cmd = ""
    node = ""
    # creates a node and records it to the character's charVars for easy rig removal
    # $nodeType is the type of node to create ("blendColors", "curveInfo", "plusMinusAverage", "multiplyDivide", "reverse", "condition", "clamp"
    # $baseName is baseName of node to be created, $prefix is "l","r", or "", and $cat is category att of charVars in which to record this node.
    # leave $limbName empty ("") to avoid it being recorded to charVars
    if nodeType == "blendColors":
        suffix = "blnd"

    elif nodeType == "curveInfo":
        suffix = "crvInfo"

    elif nodeType == "plusMinusAverage":
        suffix = "plsMns"

    elif nodeType == "multiplyDivide":
        suffix = "mltDiv"

    elif nodeType == "reverse":
        suffix = "rvrs"

    elif nodeType == "condition":
        suffix = "cond"

    elif nodeType == "clamp":
        suffix = "clmp"

    elif nodeType == "blendWeighted":
        suffix = "bldWght"

    elif nodeType == "blendTwoAttr":
        suffix = "bldTwoAtt"

    cmd = "createNode " + nodeType + \
          " -n (abRTRigNamer(\"" + baseName + "\", \"" + \
          prefix + "\", \"" + suffix + "\"));"
    node = str(pm.mel.eval(cmd))
    if limbName != "":
        saveToCharVars([node], limbName)

    return node


def saveToCharVars(aNodes, limbName):
    charVarNode = str(getCharVarNode())
    # Used for rig removal.
    # saves the joints to charVars in the attribute $limbName+"Jnts".
    # saves atts (nodeName.att) to charVars in the attribute $limbName+"Atts".
    # saves transforms to charVars in att $limbName+"Trans"
    # saves other nodes to charVars in att $limbName+"Nodes"
    if charVarNode == "":
        return
    # sort jnts into one array and atts and transforms into another

    aJnts = []
    aAtts = []
    aTrans = []
    aOthers = []
    node = ""
    aStr = []
    cVarAtt = ""
    cAttVal = ""
    arrayStr = ""
    for node in aNodes:
        if node == "":
            continue
        # determine whether this is an attribute

        aStr = node.split(".")
        if len(aStr) == 2:
            aStr[0] = stripPath(aStr[0])
            # it's an att
            if pm.mel.attributeExists(aStr[1], aStr[0]):
                aAtts.append(stripPath(node))
                continue

        if pm.nodeType(node) == "transform" and pm.objExists(node):
            aTrans.append(stripPath(node))
            # transforms
            continue

        if pm.nodeType(node) == "joint" and pm.objExists(node):
            aJnts.append(stripPath(node))
            # joints
            continue

        if pm.objExists(node):
            aOthers.append(stripPath(node))
            # capture others in $aOthers
            continue

    if len(aAtts) > 0:
        cVarAtt = limbName + "Atts"
        arrayStr = ",".join(aAtts)
        if not pm.mel.attributeExists(cVarAtt, charVarNode):
            pm.addAttr(charVarNode, ln=cVarAtt, dt="string")

        cAttVal = str(pm.getAttr(charVarNode + "." + cVarAtt))
        if len(cAttVal) > 0:
            arrayStr = cAttVal + "," + arrayStr

        pm.setAttr((charVarNode + "." + cVarAtt),
                   arrayStr, type="string")

    if len(aTrans) > 0:
        cVarAtt = limbName + "Trans"
        arrayStr = ",".join(aTrans)
        if not pm.mel.attributeExists(cVarAtt, charVarNode):
            pm.addAttr(charVarNode, ln=cVarAtt, dt="string")

        cAttVal = str(pm.getAttr(charVarNode + "." + cVarAtt))
        if len(cAttVal) > 0:
            arrayStr = cAttVal + "," + arrayStr

        pm.setAttr((charVarNode + "." + cVarAtt),
                   arrayStr, type="string")

    if len(aJnts) > 0:
        cVarAtt = limbName + "Jnts"
        arrayStr = ",".join(aJnts)
        if not pm.mel.attributeExists(cVarAtt, charVarNode):
            pm.addAttr(charVarNode, ln=cVarAtt, dt="string")

        cAttVal = str(pm.getAttr(charVarNode + "." + cVarAtt))
        if len(cAttVal) > 0:
            arrayStr = cAttVal + "," + arrayStr

        pm.setAttr((charVarNode + "." + cVarAtt),
                   arrayStr, type="string")

    if len(aOthers) > 0:
        cVarAtt = limbName + "Nodes"
        arrayStr = ",".join(aOthers)
        if not pm.mel.attributeExists(cVarAtt, charVarNode):
            pm.addAttr(charVarNode, ln=cVarAtt, dt="string")

        cAttVal = str(pm.getAttr(charVarNode + "." + cVarAtt))
        if len(cAttVal) > 0:
            arrayStr = cAttVal + "," + arrayStr

        pm.setAttr((charVarNode + "." + cVarAtt),
                   arrayStr, type="string")


def getCharVarNode():
    charName = settings.globalPrefs["name"]
    # returns or creates charVar node for a given character rootCon.  CharVar node contains info on the nodes created and associated with each part of the rigging process to allow easy removal of the rig.
    # charVar is a "geometryVarGroup" node with separate atts for spine, head/neck/eyes and lf and rt legs arms and hands;
    # Also holds version of script rig was created with
    # charVar is a child of the character_rig_grp
    # determines active character by nameField in UI.  If that's not consistent with name of rig group, then charVar won't be created correctly
    if charName == "":
        pm.warning(
            "Character Name is undefined.  Unable to save data to charVar node.")
        return ""

    rigGrp = charName + "_rig_grp"
    if not pm.objExists(rigGrp) or pm.nodeType(rigGrp) != "transform":
        pm.warning("The rig group \"" + rigGrp +
                   "\" doesn't exist.  Unable to proceed.")
        return ""

    aRel = pm.listRelatives(rigGrp, type='geometryVarGroup', ad=1)
    if len(aRel) == 1:
        return aRel[0]

    else:
        charVarNode = str(pm.createNode('geometryVarGroup',
                                        p=rigGrp, n=(charName + "_charVars")))
        # create the charVars node
        pm.addAttr(charVarNode, ln="versionNum", at='double')
        pm.setAttr((charVarNode + ".versionNum"),
                   (float(pm.mel.abRTGetGlobal("versionNum"))))
        return charVarNode


def saveRigGrpToCharVars(rigGrp, limbName):
    charVarNode = getCharVarNode()
    # saves the rigGrp to charVars in the attribute $limbName+"RigGrp".  Used for rig removal
    rigGrp = str(pm.mel.shortNameOf(rigGrp))
    if charVarNode != "":
        attName = limbName + "RigGrp"
        if not pm.mel.attributeExists(attName, charVarNode):
            pm.addAttr(charVarNode, ln=attName, dt="string")

        pm.setAttr((charVarNode + "." + attName),
                   rigGrp, type="string")


def stripPath(obj):
    # returns basename of a transform without path
    obj = str(obj)
    ret = obj[1:] if obj[0] == '|' else obj
    aName = ret.split("|")
    if len(aName) > 1:
        ret = aName[- 1]

    return ret


def setRootJntAtt(attName, attVal, rootJnt="C_root_jnt"):
    charName = settings.globalPrefs["skeletonName"]
    # sets value of attName on charName's rootJoint to attVal
    # returns success or failure

    if not pm.objExists(rootJnt):
        return False

    if not pm.mel.attributeExists(attName, rootJnt):
        pm.addAttr(rootJnt, ln=attName, dt="string",
                   hidden=True, keyable=False)

    pm.setAttr((rootJnt + "." + attName),
               attVal, type="string")
    return True


def getRootJntAtt(attName, rootJnt="C_root_jnt"):
    ret = ""
    # returns value of attName from rootJoint of charName (or nothing if doesn't exist)

    if not pm.objExists(rootJnt):
        return ""

    if pm.mel.attributeExists(attName, rootJnt): ret = str(
        pm.getAttr(rootJnt + "." + attName))

    return ret


def connectToMasterScale(grp):
    rootCtrl = "PLACER"
    # connects rig and space switching groups (or any transform) to masterScale
    if rootCtrl == "" or pm.nodeType(grp) != "transform":
        return
    # add masterScale if it doesn't exist

    if not (pm.mel.attributeExists("masterScale", rootCtrl)):
        pm.addAttr(rootCtrl, min=.001, ln="masterScale",
                   max=10, keyable=True, at='double', dv=1)

    if not (pm.isConnected((rootCtrl + ".masterScale"), (grp + ".sx"))):
        pm.connectAttr((rootCtrl + ".masterScale"), (grp + ".sx"))

    if not (pm.isConnected((rootCtrl + ".masterScale"), (grp + ".sy"))):
        pm.connectAttr((rootCtrl + ".masterScale"), (grp + ".sy"))

    if not (pm.isConnected((rootCtrl + ".masterScale"), (grp + ".sz"))):
        pm.connectAttr((rootCtrl + ".masterScale"), (grp + ".sz"))


def setScale():
    rootJnt = 'C_root_jnt'
    # sets global scale var based on size of entire skeleton -- $jnt can be any joint in skeleton below the rootJnt
    if rootJnt == "":
        return
    # if a masterScaleJnt has been specified and it's the same as the rootJnt, then the global scale var is accurate

    aJnts = pm.listRelatives(rootJnt, fullPath=1, type='joint', ad=1)
    minY = 0.0
    maxY = 0.0
    tLoc = str(pm.spaceLocator("abRTFindScaleLoc"))

    # find highest and lowest joints (in Y) to determine height of skeleton
    for tJnt in aJnts:
        snap(tJnt, tLoc)
        aTrans = pm.xform(tLoc, q=1, ws=1, t=1)
        if aTrans[1] > maxY:
            maxY = aTrans[1]
        elif aTrans[1] < minY:
            minY = aTrans[1]

    pm.delete(tLoc)
    height = maxY - minY
    avgHeight = settings.globalPrefs["avgHeight"]
    scale = height / avgHeight
    scaleStr = str(scale)
    settings["globalScale"] = scaleStr

    # fill the masterScaleJnt field to flag that scale has been determined for this jnt
    # pm.mel.abRTSetUITxtFld("masterScaleJnt", rootJnt)

    ###############################


# Splits the selected joint into the specified number of segments
###############################
def splitJnt(numSegments, joints=None, name='C_split##_skinJnt'):
    '''

    Args:
        numSegments: number of segments
        joints: the two joints in an array ['start_jnt', 'end_jnt']
        name: the name, ## will be replaced with 01, 02 ...

    Returns: the list of new joints ['C_split01_jnt', ...]

    '''
    if numSegments < 2:
        pm.error("The number of segments has to be greater than 1.. ")

    # for all selected joints
    joint = None
    splitJnts = []

    if joints == None:
        joints = pm.ls(sl=1, type='joint')

    for joint in joints:

        prevJoint = joint

        child = pm.listRelatives(joint, children=1, type='joint')
        if child == []:
            print("Joint: " + str(joint) + " has no children joints.\n")
            continue

        else:
            print("Joint: " + str(joint) + " has children joints.\n")
            child = child[0]
            # axis
            radius = pm.getAttr("%s.radius" % joint)
            axis = getJointAxis(child)

            # make sure the rotation order on $joint is correct.
            rotOrderIndex = int(pm.getAttr("%s.rotateOrder" % joint))

            # calculate spacing
            attr = ("t" + axis)
            childT = pm.getAttr("%s.%s" % (child, attr))
            print 'childT is %s' % childT
            space = childT / numSegments

            # create a series of locators along the joint based on the number of segments.
            locators = []
            for x in range(0, (numSegments - 1)):
                # align locator to joint

                locator = pm.spaceLocator()
                locators.append(locator)

                pm.parent(locator, joint)

                pm.setAttr("%s.t" % locator, (0, 0, 0))
                # offset
                pm.setAttr("%s.%s" % (locator, attr), (space * (x + 1)))
                # insert a joint
                newJoint = pm.PyNode(pm.insertJoint(prevJoint))

        splitJnts.append(newJoint)

        # get the position of the locator
        position = pm.xform(locator, q=1, rp=1, ws=1)

        # move the joint there
        pm.move(position, ws=1, pcp=1)

        pm.setAttr("%s.radius" % newJoint, radius)
        pm.setAttr("%s.rotateOrder" % newJoint, rotOrderIndex)

        prevJoint = newJoint
        pm.delete(locator)
    pm.select(joint)
    # mo_stringUtils.renameHierarchy()

    return splitJnts


# Splits the selected joint into the specified number of segments
###############################
def addTwistJnts(numSegments, joints=None, name='C_split##_skinJnt'):
    '''

    Args:
        numSegments: number of segments
        joints: the two joints in an array ['start_jnt', 'end_jnt']
        name: the name, ## will be replaced with 01, 02 ...

    Returns: the list of new joints ['C_split01_jnt', ...]

    '''
    if numSegments < 1:
        pm.error("The number of segments has to be greater than 0.. ")

    # for all selected joints
    joint = None
    twistJnts = []

    if joints == None:
        joints = pm.ls(sl=1, type='joint')

    for joint in joints:

        prevJoint = joint

        child = pm.listRelatives(joint, children=1, type='joint')
        if child == []:
            print("Joint: " + str(joint) + " has no children joints.\n")
            continue

        else:
            print("Joint: " + str(joint) + " has children joints.\n")
            child = child[0]
            # axis
            radius = pm.getAttr("%s.radius" % joint)
            axis = getJointAxis(child)

            # make sure the rotation order on $joint is correct.
            rotOrderIndex = int(pm.getAttr("%s.rotateOrder" % joint))

            # calculate spacing
            attr = ("t" + axis)
            childT = pm.getAttr("%s.%s" % (child, attr))
            print 'childT is %s' % childT
            space = childT / numSegments

            # create a series of locators along the joint based on the number of segments.
            locators = []

            for x in range(0, (numSegments - 1)):
                # align locator to joint

                locator = pm.spaceLocator()
                locators.append(locator)

                pm.parent(locator, joint)

                pm.setAttr("%s.t" % locator, (0, 0, 0))
                # offset
                pm.setAttr("%s.%s" % (locator, attr), (space * (x + 1)))
                # insert a joint
                newJoint = pm.joint(n=name.replace("##", '%02d' % x))
                snap(locator, newJoint)

                pm.parent(newJoint, joint)
                # pm.makeIdentity(newJoint,)

        twistJnts.append(newJoint)

        # get the position of the locator
        position = pm.xform(locator, q=1, rp=1, ws=1)

        # move the joint there
        pm.move(position, ws=1, pcp=1)

        pm.setAttr("%s.radius" % newJoint, radius)
        pm.setAttr("%s.rotateOrder" % newJoint, rotOrderIndex)

        prevJoint = newJoint
        pm.delete(locator)
    pm.select(joint)
    # mo_stringUtils.renameHierarchy()

    return twistJnts


def getJointAxis(child):
    axis = ""
    t = [0.0] * (0)
    t = pm.getAttr("%s.t" % child.name())
    # get the translation values of the $child joint
    # now check and see which one is greater than 0.  We should have a tolerance value just in case
    tol = 0.0001
    for x in range(0, 2 + 1):
        if (t[x] > tol) or (t[x] < (-1 * tol)):
            if x == 0:
                axis = "x"
            elif x == 1:
                axis = "y"
            elif x == 2:
                axis = "z"
    if axis == "":
        pm.error(
            "The child joint is too close to the parent joint. Cannot determine the proper axis to segment.")

    return axis


def createCurveControl(controlObj, controlAttribute, destinationAttribute):
    '''
    Script:     js_createCurveControl.mel
    Author:     Jason Schleifer

    Descr:      This script will create a single curve which can be used to control
                the given attribute on the selected objects.

                For example, if you want to drive the ty attribute on 10 objects with
                a "height" curve on another object, you would select the 10 objects,
                and then enter:

                js_createControlCurve controlObj height ty

                Note: make sure the given object and attribute exists
    '''

    if not pm.objExists(controlObj):
        pm.pm.mel.error(controlObj + " does not exist.  Exiting..\n")

    if not pm.attributeQuery(controlAttribute,
                             node=controlObj, exists=1):
        pm.addAttr(controlObj,
                   ln=controlAttribute, at='double')
        pm.setAttr((controlObj + "." + controlAttribute),
                   k=1)

    # find the selected objects
    objs = pm.ls(sl=1)
    if len(objs) == 0:
        pm.pm.mel.error("Nothing Selected.\n")

    numControls = len(objs)
    # now that we have the objects, we can create the animation curve which will control the attribute
    objAttr = (controlObj + "." + controlAttribute)
    pm.setKeyframe(controlObj,
                   v=0, at=controlAttribute, t=1)
    pm.setKeyframe(controlObj,
                   v=0, at=controlAttribute, t=numControls)
    pm.keyTangent(controlObj,
                  wt=1, at=controlAttribute)
    pm.keyTangent(controlObj,
                  at=controlAttribute, weightLock=False)
    pm.keyTangent(objAttr,
                  a=1, e=1, t=1, outAngle=50)
    pm.keyTangent(objAttr,
                  a=1, e=1, t=numControls, inAngle=-50)
    # next, we'll create frameCache nodes for each object, and attach them to the object's attribute
    for x in range(0, numControls):
        fc = pm.createNode('frameCache')
        # create the frameCache node
        fc = pm.rename(fc,
                       (str(objs[x]) + "_frameCache"))
        # connect the attribute
        pm.connectAttr(objAttr,
                       (str(fc) + ".stream"))
        # set the frame
        pm.setAttr((str(fc) + ".vt"), (x + 1))
        # connect the output
        # check and see if the destination attribute exists.  if not, create it
        if not pm.attributeQuery(destinationAttribute,
                                 node=objs[x], exists=1):
            pm.addAttr(objs[x],
                       ln=destinationAttribute, at='double')
            pm.setAttr((str(objs[x]) + "." + destinationAttribute),
                       k=1)

        pm.connectAttr((str(fc) + ".v"), (str(objs[x]) + "." + destinationAttribute),
                       f=1)

    pm.select(objAttr)


def makeCurveFromJoints(jointList, name='C_spine_crv', rebuild=True, divisions=3):
    tLoc = pm.spaceLocator(name="skeletonizeTemp_loc")
    curveStr = "curve -d 3"

    for i in range(0, len(jointList)):
        snap(jointList[i], tLoc)
        aTrans = pm.xform(tLoc, q=1, ws=1, t=1)
        curveStr += " -p " + str(aTrans[0]) + " " + str(aTrans[1]) + " " + str(aTrans[2])

    curveStr += " -n " + name
    spineCurve = str(pm.mel.eval(curveStr))
    # parent curve

    pm.delete(tLoc)
    pm.select(clear=1)

    if rebuild:
        aStr = pm.rebuildCurve(spineCurve,
                               rt=0, ch=1, end=1, d=3, kr=0, s=divisions, kcp=0, tol=0.01, kt=0, rpo=1, kep=0)

        # create spine joints
        # pm.delete(spineCurve)
        spineCurve = pm.rename(aStr[0], name)

    return spineCurve


def createJointsAlongCurve(crv, amount=4, name='C_spine##_fkJnt'):
    joints = []
    crv_info = '%s_pointinfo' % crv
    pm.delete(pm.ls(crv_info))
    crv_info = pm.shadingNode('pointOnCurveInfo', name=crv_info, asUtility=True)
    pm.setAttr('%s.turnOnPercentage' % crv_info, 1)

    pm.connectAttr('%s.worldSpace[0]' % crv, '%s.inputCurve' % crv_info, f=1)

    for i in range(0, amount):
        log_debug(1.00 / amount * float(i))
        pm.setAttr('%s.parameter' % crv_info, (1.00 / amount * float(i)))
        log_debug(pm.getAttr('%s.parameter' % crv_info)) 
        position_on_curve = pm.getAttr('%s.position' % crv_info)

        # create joint at position
        j = pm.joint(n=name.replace('##', '%02d' % (i+1), p=position_on_curve))
        joints.append(j)
    
    pm.setAttr('%s.parameter' % crv_info, 1)
    position_on_curve = pm.getAttr('%s.position' % crv_info)
    j = pm.joint(n=name.replace('##', '%02d' % amount), p=position_on_curve)
    joints.append(j)

    pm.delete(pm.ls(crv_info))

    return joints

def zeroJointOrient(jnt):
    pm.setAttr('%s.jointOrientX'%jnt, 0)
    pm.setAttr('%s.jointOrientY'%jnt, 0)
    pm.setAttr('%s.jointOrientZ'%jnt, 0)