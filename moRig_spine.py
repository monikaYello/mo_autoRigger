import pymel.core as pm
import mo_Utils.mo_riggUtils as mo_riggUtils
reload(mo_riggUtils)

def build_skinJnts_spine():
    startknob = pm.PyNode('Root_knob')
    endknob = pm.PyNode('Chest_knob')
    pm.select(clear=1)
    start_jnt, end_jnt = pm.joint(n='C_spine0_ctrlJnt'), pm.joint(n='C_spineEnd_ctrlJnt')
    pm.xform(start_jnt, t=pm.xform(startknob, q=1, t=1, ws=1), ws=1)
    pm.xform(end_jnt, t=pm.xform(endknob, q=1, t=1, ws=1), ws=1)
    mo_riggUtils.splitJnt(4, joints=[start_jnt, end_jnt])


def resampleSpline():
    amount = 4
    multiplyer = 1.00/amount
    for i in range(amount):
        knob = pm.sphere(n='spine_knob%02d'%(i+1), r=0.2)
        grp = pm.group(knob, name='spine_grp%02d'%(i+1))
        const = pm.parentConstraint(['Root_knob', 'Chest_knob'], grp, mo=0)
        print (multiplyer * i )
        pm.setAttr('%s.Root_knobW0'%const, (1-(multiplyer*i)))
        pm.setAttr('%s.Chest_knobW1'%const, (multiplyer*i))

def setup_spine(jnts):
    # constrain pelvis
    pm.parentConstraint(jnts['pelvis01']['ctrl'], jnts['pelvis01']['ctrlJnt'].attr('AUTO').get(), mo=1)
    # constrain chest
    pm.parentConstraint(jnts['chest01']['ctrl'], jnts['chest01']['ctrlJnt'].attr('AUTO').get(), mo=1)

    spine_list = [j for j in jnts.keys() if j[0:5] == 'spine']
    spine_list.sort()
    spline_ik = pm.ikHandle(n='C_spine_splineIK', sj=jnts[spine_list[0]]['ctrlJnt'], ee=jnts[spine_list[-1]]['ctrlJnt'],
                            sol='ikSplineSolver')

    spline_hndl = spline_ik[0]
    spline_eff = spline_ik[1].rename('C_spine_splineEfctr')
    spline_crv = spline_ik[2].rename('C_spine_splineCrv')

    pm.group(spline_hndl, n='C_spine_nonScaleGrp')
    mo_riggUtils.grpIn('C_spine_nonScaleGrp', 'RIG_NONSCALE')

    # skin cure to joints
    # to bind nurbsSphere1 and pPlane1 to the skeleton containing joint2
    #
    pm.bindSkin(spline_crv, [jnts['pelvis01']['ctrlJnt'], jnts['chest01']['ctrlJnt']])

    # make stretchy
    createStretchSpline(spline_crv, volume=1, worldScale=0, worldScaleObj=None, worldScaleAttr=None)


def createStretchSpline(curveObj, volume, worldScale, worldScaleObj, worldScaleAttr):
    """
    Script:     js_createStretchSpline.mel
    Author:     Jason Schleifer


    Descr:      Given the selected curve, it will tell the joints to stretch.  It's easiest to use with the
                js_createStretchSplineUI.mel script

    Inputs:     $curveObj           =>  The nurbs curve that will be stretched
                $maintainVolume     =>  Whether or not to maintain volume on the joints
                                        if this is on, then it will be made with
                                        an expression, if not then we'll use nodes.

                $worldScale         =>  Whether or not to take worldScale into account

                $worldScaleObj      =>  The object that will be used for world scale

                $worldScaleAttr     =>  The attribute to be used for world scale

    Req:        js_getStretchAxis.mel
                js_createCurveControl.mel
    """

    node = pm.arclen(curveObj, ch=1)
    # based on the given curve, tell the joints to stretch
    # create a curveInfo node
    # get the ikhandle
    con = [""] * (0)
    shape = [""] * (0)
    shape = pm.listRelatives(curveObj, s=1, f=1)
    con = pm.listConnections((shape[0] + ".worldSpace[0]"),
                             type='ikHandle')
    ikHandle = con[0]
    # find out what joints are in the list
    joints = [""] * (0)
    joints = pm.ikHandle(ikHandle, q=1, jl=1)
    # we need to figure out which direction the curve should be scaling.
    # do to that, we'll look at the translate values of the second joint.  Whichever translate has the
    # highest value, that'll be the first one and the other two axis will be the shrinking one
    stretchAxis = [""] * (3)
    stretchAxis = pm.mel.js_getStretchAxis(joints[1])
    # create a normalizedScale attr on the curveInfo node
    pm.addAttr(node, ln="normalizedScale", at="double")
    length = pm.getAttr(str(node) + ".arcLength")
    #  create a NormalizedScale node to connect to everything.
    multDivide = pm.createNode('multiplyDivide')
    multDivide = pm.rename(multDivide,
                           (curveObj + "_normalizedScale"))
    # set the multiplyDivide node to division
    pm.setAttr((str(multDivide) + ".operation"),
               2)
    pm.connectAttr((str(node) + ".arcLength"), (str(multDivide) + ".input1X"))
    pm.setAttr((str(multDivide) + ".input2X"),
               length)
    pm.connectAttr((str(multDivide) + ".outputX"), (str(node) + ".normalizedScale"))
    # if worldscale is off, and volume deformation is off, we can just connect directly to the joints
    if (worldScale == 0) and (volume == 0):
        for joint in joints:
            print "connecting to " + str(joint) + "." + stretchAxis[0] + "\n"
            pm.connectAttr((str(node) + ".normalizedScale"), (str(joint) + "." + stretchAxis[0]),
                           f=1)



    elif (worldScale == 1) and (volume == 0):
        md2 = pm.createNode('multiplyDivide', n=(curveObj + "_worldScale"))
        # if $worldScale is on, but volume is off we can just add another multiply divide node
        # and connect to that
        # create a multiplyDivide node
        pm.setAttr((str(md2) + ".operation"),
                   2)
        pm.connectAttr((str(node) + ".normalizedScale"), (str(md2) + ".input1X"))
        pm.connectAttr((worldScaleObj + "." + worldScaleAttr), (str(md2) + ".input2X"))
        for joint in joints:
            pm.connectAttr((str(md2) + ".outputX"), (str(joint) + "." + stretchAxis[0]),
                           f=1)



    else:
        pm.select(joints)
        # also create an anim curve which we can use to connnect to the joints to help
        # determine the scaling power in X and Z.  This will be attached to the curve itself
        pm.mel.js_createCurveControl(curveObj, "scalePower", "pow")
        # start creating an expression
        expr = ""
        # for each joint, connect the scaleX to the normalizedScale
        if worldScale:
            expr += ("$scale = " + str(node) + ".normalizedScale/" + worldScaleObj + "." + worldScaleAttr + ";\n")


        else:
            expr += ("$scale = " + str(node) + ".normalizedScale;\n")

        expr += ("$sqrt = 1/sqrt($scale);\n")
        size = len(joints)
        for x in range(0, size):
            item = joints[x]
            # set a powPosition based on the number of joints which will be scaling, from 0 to 1
            expr = (expr + str(item) + "." + stretchAxis[0] + " = $scale;\n")
            expr = (expr + str(item) + "." + stretchAxis[1] + " = pow($sqrt," + str(item) + ".pow);\n")
            expr = (expr + str(item) + "." + stretchAxis[2] + " = pow($sqrt," + str(item) + ".pow);\n")

        pm.expression(s=expr, n=(curveObj + "_expr"))

    pm.select(curveObj)


