import pymel.core as pm
import mo_Utils.mo_riggUtils as riggUtils
import moRig_utils as utils
import moRig_settings as settings
import mo_Utils.mo_curveLib as curveLib
from mo_Utils.mo_logging import log_debug
from mo_Utils.mo_logging import log_info
reload(utils)
reload(riggUtils)


def build_skinJnts_spine(startknob, endknob, amount):
    pm.select(clear=1)

    start_jnt, end_jnt = pm.joint(n='C_spine01_skinJnt'), pm.joint(n='C_spine%02d_skinJnt' % amount)

    pm.xform(start_jnt, t=pm.xform(startknob, q=1, t=1, ws=1), ws=1)
    pm.xform(end_jnt, t=pm.xform(endknob, q=1, t=1, ws=1), ws=1)

    riggUtils.splitJnt(amount, joints=[start_jnt, end_jnt])


def resampleSpline(amount=4):
    multiplyer = 1.00 / amount
    for i in range(amount):
        knob = pm.sphere(n='spine_knob%02d' % (i + 1), r=0.2)
        grp = pm.group(knob, name='spine_grp%02d' % (i + 1))
        const = pm.parentConstraint(['Root_knob', 'Chest_knob'], grp, mo=0)

        pm.setAttr('%s.Root_knobW0' % const, (1 - (multiplyer * i)))
        pm.setAttr('%s.Chest_knobW1' % const, (multiplyer * i))


def create_ctrl_spine(jnts, spine_count=4, scale=1):
    '''
    Create COG, pelvis, spine and chest ctrls

    Args:
        jnts:
        spine_count:
        size: ctrl scale

    Returns:

    '''
    ### TODO cest offset control, to rotate from chest if needed (human_luma:C_chest_offsetCtrl)
    log_info('Creating Spine Ctrls')
    side = 'C'
    scale = scale * 2 # scale multiplyier

    # - COG - #

    # create ctrl
    cog = curveLib.wireController(type='circle', name='C_COG_ctrl', size=scale*1.25, color='yellow', facingAxis='y+')
    riggUtils.cleanUpAttr(sel=[cog], listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
    # grp - snap - parent - gimbal
    riggUtils.grpCtrl(cog)
    riggUtils.snap(jnts['pelvis01']['ctrlJnt'], cog.ZERO.get(), 'point')
    pm.parent(cog.ZERO.get(), 'DIRECTION')
    riggUtils.addGimbal(cog)
    # add to dictionary
    jnts['cog'] = {'ctrl': pm.PyNode('C_COG_ctrl')}

    spine_ctrl_grp = pm.createNode('transform', n='C_spineCtrl_grp', p=cog.gimbal.get())
    riggUtils.snap(cog.gimbal.get(), spine_ctrl_grp)
    
    
    # - Pelvis - #

    log_debug('creating pelvis ctrls')
    jnts['pelvis01']['ctrl'] = curveLib.wireController(type='circle', name='C_pelvis_ctrl', size=scale,
                                                       color='red', facingAxis='y+', aOffset=[0, -0.5, 0])
    riggUtils.cleanUpAttr(sel=jnts['pelvis01']['ctrl'], listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
    # rotation order
    jnts['pelvis01']['ctrlJnt'].rotateOrder.set(2)
    jnts['pelvis01']['ctrl'].rotateOrder.set(2)
    # grp - snap - parent - gimbal
    riggUtils.grpCtrl(jnts['pelvis01']['ctrl'])
    riggUtils.snap(jnts['pelvis01']['ctrlJnt'], jnts['pelvis01']['ctrl'].ZERO.get(), 'point')
    pm.parent(jnts['pelvis01']['ctrl'].ZERO.get(), spine_ctrl_grp)
    riggUtils.addGimbal(jnts['pelvis01']['ctrl'])

    # - Spine - #

    # ik spine
    
    log_debug('creating ik spine ctrls %s' % spine_count)
    spine_ik_jnts = pm.ls('C_spine*_ikJnt*')

    if len(spine_ik_jnts) < 3:
        log_info("No spine*_fkJnts found. Skipping")   
    else:
        parent_to=spine_ctrl_grp 
    
        # for ik ctrl, we skip 01 and 03, we will parent those to pelvis and chest, we only want a 'C_spine_midCtrl'
        ctrl = curveLib.wireController(type='cube', name='C_spineMid_ikCtrl', size=scale *0.25,
                                                        color='blue', facingAxis='y+',  aOffset=[0, 0, -3])
        riggUtils.cleanUpAttr(ctrl, listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
        riggUtils.grpCtrl(ctrl)
        riggUtils.snap(spine_ik_jnts[1], ctrl.ZERO.get(), 'point')
        pm.parent(ctrl.ZERO.get(), parent_to)
        
        # add to dic    
        jnts['spine02']['ikCtrl'] = ctrl

        #parent jnt
        pm.parent(spine_ik_jnts[1], ctrl)
    
    
    # fk spine

    log_debug('creating fk spine ctrls %s' % spine_count)
    spine_fk_jnts = pm.ls('C_spine*_ctrlJnt')

    if len(spine_fk_jnts) == 0:
        log_info("No spine*_fkJnts found. Skipping")
    
    parent_to=spine_ctrl_grp

    for i in range(0, len(spine_fk_jnts)):
        jnt_nr = '%02d' % ( i + 1)
        ctrl = curveLib.wireController(type='circle', name='C_spine%s_fkCtrl'%jnt_nr, size=scale,
                                                      color='blue', facingAxis='y+')
        riggUtils.cleanUpAttr(ctrl, listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
        riggUtils.grpCtrl(ctrl)
        riggUtils.snap(spine_fk_jnts[i], ctrl.ZERO.get(), 'point')
        pm.parent(ctrl.ZERO.get(), parent_to)
        
        # parent next jnt to this ctrl
        parent_to = ctrl

        # add to dic
        jnts['spine%s'%jnt_nr]['fkCtrl'] = ctrl

    # - Chest - #

    log_debug('creating chest ctrls')
    jnts['chest01']['ctrl'] = curveLib.wireController(type='circle', name='C_spineChest_ctrl', size=scale,
                                                      color='red', facingAxis='y+')
    riggUtils.cleanUpAttr(sel=jnts['chest01']['ctrl'], listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
    # rotation order
    jnts['chest01']['ctrlJnt'].rotateOrder.set(2)
    jnts['chest01']['ctrl'].rotateOrder.set(2)

    # grp - snap - parent - gimbal
    riggUtils.grpCtrl(jnts['chest01']['ctrl'])
    riggUtils.snap(jnts['chest01']['ctrlJnt'], jnts['chest01']['ctrl'].ZERO.get(), 'point')
    pm.parent(jnts['chest01']['ctrl'].ZERO.get(), spine_ctrl_grp)
    riggUtils.addGimbal(jnts['chest01']['ctrl'])

    log_debug('spine_ik is %s'%spine_ik_jnts)
    
    # lets parent 01_ikJnt to pelvis ctrl and 03_ikJnt to chest (ik 2 has its own ctrl)
    if len(spine_ik_jnts) > 2:
        pm.parent(spine_ik_jnts[0],  jnts['pelvis01']['ctrl'])
        pm.parent(spine_ik_jnts[2],  jnts['chest01']['ctrl'])

        # align spineMid halfway between pelvis and chest
        pm.parentConstraint([jnts['pelvis01']['ctrl'], jnts['chest01']['ctrl']], jnts['spine02']['ikCtrl'].AUTO.get(), mo=1)
    
    log_debug('done create_ctrl_spine')



''

def create_fk_spine(amount=4):
    pm.delete(pm.ls('C_spine_splineCrv'))
    spineJnts = pm.ls('C_spine*_ctrlJnt')

    spline_crv = utils.makeCurveFromJoints(spineJnts, name='C_spine_splineCrv', rebuild=True, divisions=2)
    jointRadius = float(settings.globalPrefs['jointRadius'])
    fkJnts = utils.createJointsAlongCurve(spline_crv, amount=amount+1, name='C_spine##_fkJnt', jointRadius=jointRadius)

    pm.delete(spline_crv)

    return fkJnts

def create_ik_spine():
    log_debug('creating ik spine')
    jointRadius = float(settings.globalPrefs['jointRadius'])

    # get spine jnts
    spineJnts = pm.ls('C_spine*_ctrlJnt')

    # create curve with 3 cvs along spine jnts
    spline_crv = utils.makeCurveFromJoints(spineJnts, name= 'C_spine_splineCrv', rebuild=True, divisions=2)

    ikJnts = utils.createJointsAlongCurve(spline_crv, amount=3, name='C_spine##_ikJnt', jointRadius=jointRadius)
    
    pm.skinCluster(ikJnts, spline_crv, tsb=True, maximumInfluences=3, normalizeWeights=1, obeyMaxInfluences=True)
    
    pm.delete(spline_crv)

    return ikJnts
    # ikJnts = riggUtils.createCvClusters(curves=spline_crv, ctrl='joint', suffix='ikJnt', skin=False)
    # for ikJnt in ikJnts:
    #     pm.setAttr(ikJnt, radius=jointRadius)


def setup_spine(jnts, fkCtrls=3):
    spineCrv = 'C_spine_splineCrv'
    pm.delete(pm.ls(spineCrv))
    spineFkCtrls = pm.ls('C_spine*_fkCtrl', type='transform')
    spineIkJnts = pm.ls('C_spine*_ikJnt*', type='joint')
    spineCtrlJnts =pm.ls('C_spine*_ctrlJnt*', type='joint')
    
    #clean up from old runs
    utils.deleteChildrenConstraints(jnts['pelvis01']['ctrlJnt'].attr('AUTO').get())
    utils.deleteChildrenConstraints(jnts['chest01']['ctrlJnt'].attr('AUTO').get())
    

    # constrain pelvis
    pm.parentConstraint(jnts['pelvis01']['ctrl'], jnts['pelvis01']['ctrlJnt'].attr('AUTO').get(), mo=1)
    # constrain chest
    pm.parentConstraint(jnts['chest01']['ctrl'], jnts['chest01']['ctrlJnt'].attr('AUTO').get(), mo=1)

    spine_list = [j for j in jnts.keys() if j[0:5] == 'spine']
    spine_list.sort()
    spineJnts = pm.ls('C_spine*_skinJnt')

    # ik stretchy spline

    spline_crv = utils.makeCurveFromJoints(spineJnts, name=spineCrv, rebuild=True, divisions=2)
    
    spline_ik = pm.ikHandle(n='C_spine_splineIK', sj=jnts[spine_list[0]]['ctrlJnt'], ee=jnts[spine_list[-1]]['ctrlJnt'],
                            sol='ikSplineSolver', curve=spline_crv, ccv=False)
    print 'spine_ik is %s' % spline_ik
    spline_hndl = spline_ik[0]
    spline_eff = spline_ik[1].rename('C_spine_splineEfctr')
    # spline_crv = spline_ik[2].rename('C_spine_splineCrv')

    riggUtils.grpIn('C_spineNonScale_grp',[spline_hndl, spline_crv])
    riggUtils.grpIn('RIG_NONSCALE','C_spineNonScale_grp')

    # skin curve to ik joints
    pm.select(clear=1)
    pm.select(spineIkJnts)
    pm.skinCluster(spineIkJnts, spline_crv, maximumInfluences=4, normalizeWeights=1, obeyMaxInfluences=True)


    log_debug( 'creating stretchy spline' )
    # add attributes
    pm.addAttr(jnts['chest01']['ctrl'], ln='stretchy', at='float', dv=1, k=1)
    pm.addAttr(jnts['chest01']['ctrl'], ln='follow', at='float', dv=1, k=1)
    
    # make stretchy
    createStretchSpline(spline_crv, volume=1, worldScale=1, worldScaleObj='RIG_SCALE', worldScaleAttr='scaleX', disable=1, disableObj=jnts['chest01']['ctrl'], disableAttr='stretchy' )

    # fk - expect fkJnts having fkCtrls in right spot
    
    for spineFkCtrl in spineFkCtrls:
        log_debug('fk constraint %s'%spineFkCtrl)
        spineFkJnt = spineFkCtrl.replace('fkCtrl', 'fkJnt')
        pm.parentConstraint(spineFkCtrl, spineFkJnt, mo=1)

    # connect ik to fk
    pm.parentConstraint(spineFkCtrls[-1], 'C_spineChest_AUTO', mo=1)

    # connect spine to chest
    ### TODO Pin to attribute blend set on chest of Lumahuman
    pm.pointConstraint(spineCtrlJnts[-1], jnts['chest01']['ctrlJnt'])

    # connect rigg scale to curve
    pm.addAttr(spineCrv, ln='globalScale', at='float', dv=1, k=1)
    pm.connectAttr('RIG_SCALE.scaleX', '%s.globalScale'%spineCrv)

def createStretchSpline(curveObj, volume, worldScale, worldScaleObj, worldScaleAttr, disable=0, disableObj='', disableAttr=''):
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

                $disable            =>  Option to control and disable stretch with control

                $disableObj      =>  The object that will be used for disable

                $disableAttr     =>  The attribute to be used for disable 

    Req:        getStretchAxis
                createCurveControl
    """

    node = pm.arclen(curveObj, n= '%s_curveInfo'%curveObj, ch=1)
    # based on the given curve, tell the joints to stretch
    # create a curveInfo node
    # get the ikhandle
    shape = pm.listRelatives(curveObj, s=1, f=1)
    con = pm.listConnections((shape[0] + ".worldSpace[0]"),  type='ikHandle')
    ikHandle = con[0]
    # find out what joints are in the list
    joints = pm.ikHandle(ikHandle, q=1, jl=1)
    # we need to figure out which direction the curve should be scaling.
    # do to that, we'll look at the translate values of the second joint.  Whichever translate has the
    # highest value, that'll be the first one and the other two axis will be the shrinking one
    stretchAxis = getStretchAxis(joints[1])
    # create a normalizedScale attr on the curveInfo node
    pm.addAttr(node, ln="normalizedScale", at="double")
    length = pm.getAttr(str(node) + ".arcLength")

    # create blend node for on/off
    blendStretch = pm.shadingNode('blendColors', asUtility=1, name='%s_stretchBlend'%curveObj)
    pm.setAttr(str(blendStretch) + '.color1R', length)
    pm.connectAttr((str(node) + ".arcLength"), str(blendStretch) + '.color2R')

    #  create a NormalizedScale node to connect to everything.
    multDivide = pm.createNode('multiplyDivide')
    multDivide = pm.rename(multDivide,
                           (curveObj + "_normalizedScale"))
    # set the multiplyDivide node to division
    pm.setAttr((str(multDivide) + ".operation"), 2)
    pm.connectAttr("%s.outputR"%blendStretch,  "%s.input1X"%multDivide)
    pm.setAttr((str(multDivide) + ".input2X"),
               length)
    pm.connectAttr((str(multDivide) + ".outputX"), (str(node) + ".normalizedScale"))
    
    if disable:
        pm.connectAttr('%s.%s'%(disableObj, disableAttr), '%s.blender'%blendStretch )
    else:
        pm.setAttr('%s.blender'%blendStretch, 1 )

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
        utils.createCurveControl(curveObj, "scalePower", "pow")
        # start creating an expression
        expr = ""
        # for each joint, connect the scaleX to the normalizedScale
        # if worldScale and disable:
        #     expr += ("$scale = " + str(node) + ".normalizedScale *" + worldScaleObj + "." + worldScaleAttr + " * " + disableObj + "." + disableAttr + ";\n")
        if worldScale:
            expr += ("$scale = " + str(node) + ".normalizedScale *" + worldScaleObj + "." + worldScaleAttr + ";\n")
        # elif disable:
        #     expr += ("$scale = " + str(node) + ".normalizedScale *" + disableObj + "." + disableAttr + ";\n")
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
    return joints


def getStretchAxis(joint):
    stretchAxis = [""] * (3)
    t = [0.0] * (3)
    t = pm.getAttr(joint + ".t")
    if (abs(t[0]) > abs(t[1])) and (abs(t[0]) > abs(t[2])):
        stretchAxis = ["sx", "sy", "sz"]


    elif (abs(t[1]) > abs(t[0])) and (abs(t[1]) > abs(t[2])):
        stretchAxis = ["sy", "sx", "sz"]


    elif (abs(t[2]) > abs(t[0])) and (abs(t[2]) > abs(t[1])):
        stretchAxis = ["sz", "sx", "sy"]

    return stretchAxis
