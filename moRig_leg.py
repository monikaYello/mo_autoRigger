import pymel.core as pm
import mo_Utils.mo_riggUtils as riggUtils
import mo_Utils.mo_curveLib as curveLib
import moRig_biped as biped
reload(riggUtils)

from mo_Utils.mo_logging import log_debug
from mo_Utils.mo_logging import log_info

def build_ctrlJnts_leg(jnts={}, side='L', hook='C_pelvis01_ctrlJnt'):
    '''
    create ctrl joints for leg
    '''
    log_debug( 'side is %s' % side )
    pm.delete(pm.ls('%s_leg_jntGrp' % side))
    pm.createNode('transform', name='%s_leg_jntGrp' % side)
    riggUtils.grpIn('Skeleton_grp', '%s_leg_jntGrp' % side)

    # leg
    leg = pm.duplicate('%s_leg01_skinJnt' % side, n='%s_leg01_ctrlJnt' % side)[0]
    jnts['%s_leg01' % side] = {'ctrlJnt': leg}
    pm.select(leg)
    pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")
    pm.parent(leg, '%s_leg_jntGrp' % side)
    riggUtils.grpCtrl(leg)

    log_debug('constraining to hook %s'%leg.ZERO.get())

    if hook != '':
        pm.parentConstraint(hook, leg.AUTO.get(), mo=1)

    # deal with children
    for childJnt in pm.listRelatives(leg, children=1, type='joint', ad=1):
        log_debug( 'childJnt leg %s' % childJnt )
        if childJnt == ('%s_foot01_ctrlJnt' % side):
            pm.rename(childJnt, '%s_leg03_ctrlJntEnd' % side)  # create end joint from foot
            # delete fingers
            pm.delete(pm.listRelatives('%s_leg03_ctrlJntEnd' % side, children=1, ad=1))
            break

    # foot
    foot = pm.duplicate('%s_foot01_skinJnt' % side, n='%s_foot01_ctrlJnt' % side)[0]
    jnts['%s_foot' % side] = {'ctrlJnt': foot}

    pm.select(foot)
    pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")

    riggUtils.grpIn('%s_leg_jntGrp' % side, foot)
    riggUtils.grpCtrl(foot)

    # constrain foot AUTO to leg03End
    pm.pointConstraint('%s_leg03_ctrlJntEnd' % side, pm.getAttr('%s_foot01_ctrlJnt.AUTO' % side))



def build_jnts_leg(jnts={}, mode=['ik', 'fk']):
    '''
    Build leg jnts FK and IK by duplicating ctrlJnts
    Args:
        jnts:
        mode:

    Returns:

    '''
    for RL in ['R', 'L']:
        if '%s_leg01' % RL in jnts:
            if 'fk' in mode:
                if pm.objExists('%s_leg01_fkJnt' % RL): pm.delete('%s_leg01_fkJnt' % RL)  # delete existing

                fkJnt = pm.duplicate(jnts['%s_leg01' % RL]['ctrlJnt'], n='%s_leg01_fkJnt' % RL)
                log_debug( 'creating fkLeg %s' % fkJnt )
                pm.select(fkJnt)
                pm.mel.searchReplaceNames("_ctrlJnt", "_fkJnt", "hierarchy")

            if 'ik' in mode:
                if pm.objExists('%s_leg01_ikJnt' % RL): pm.delete('%s_leg01_ikJnt' % RL)  # delete existing
                ikJnt = pm.duplicate(jnts['%s_leg01' % RL]['ctrlJnt'], n='%s_leg01_ikJnt' % RL)
                log_debug( 'creating ikLeg %s' % ikJnt )
                pm.select(ikJnt)
                pm.mel.searchReplaceNames("_ctrlJnt", "_ikJnt", "hierarchy")

        if '%s_foot01' % RL in jnts:
            if 'fk' in mode:
                biped.deleteExisting('%s_foot01_fkJnt' % RL)  # delete existing
                fkJnt = pm.duplicate(jnts['%s_foot01' % RL]['ctrlJnt'], n='%s_foot01_fkJnt' % RL)
                pm.select(fkJnt)
                pm.mel.searchReplaceNames("_ctrlJnt", "_fkJnt", "hierarchy")
            if 'ik' in mode:
                biped.deleteExisting('%s_foot01_ikJnt' % RL)  # delete existing
                ikJnt = pm.duplicate(jnts['%s_foot01' % RL]['ctrlJnt'], n='%s_foot01_ikJnt' % RL)
                pm.select(ikJnt)
                pm.mel.searchReplaceNames("_ctrlJnt", "_ikJnt", "hierarchy")
    log_info("Done build_jnts_leg()")



def create_ctrl_fk_leg(jnts, side='L', parent='DIRECTION', scale=1):
    '''
    Args:
        jnts: joint dictionary
        side: 'R' or 'L'
    Returns:   joint dictionary
    '''
    if side == 'L':
        color = 'blue'
    else:
        color = 'red'

    id = '%s_leg01' % side
    jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=scale, color=color)
    # pm.xform('%sShape.cv[0:]' % jnts[id]['fkCtrl'], s=(1.75, 1, 1), t=(1.5, 0, 0), r=1)
    # group and align
    zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
    riggUtils.snap(jnts[id]['fkJnt'], zero)
    riggUtils.grpIn('%s_leg_ctrlGrp' % side, zero)  # parent leg_ctrlGrp
    riggUtils.grpIn(parent, '%s_leg_ctrlGrp' % side)
    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

    id = '%s_leg02' % side
    jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=scale, color=color)
    # group and align
    zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
    riggUtils.snap(jnts[id]['fkJnt'], zero)
    pm.parent(zero, jnts['%s_leg01' % side]['fkCtrl'])  # parent leg01
    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

    # leg03 is technically foot in human setup, so we will hide ctrl
    # leg03_ctrl drive leg03_endJnt and therefore foot01_ctrl and will be used for stretch setup
    # to hook up length to zero tx
    id = '%s_leg03' % side
    jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=scale, color=color)
    # group and align
    zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
    riggUtils.snap(jnts[id]['fkJnt'], zero)
    pm.parent(zero, jnts['%s_leg02' % side]['fkCtrl'])  # parent leg02
    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)
    zero.hide()

    id = '%s_foot01' % side
    jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=(scale*.75), color=color)
    # group and align
    zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
    riggUtils.snap(jnts[id]['ctrlJnt'], zero)
    riggUtils.grpIn('%s_leg_ctrlGrp' % side, zero)  # parent leg ctrlGrp, AUTO will be constraint to leg03_endJnt
    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

    id = '%s_foot02' % side
    jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=(scale*.75), color=color)
    # group and align
    zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
    riggUtils.snap(jnts[id]['ctrlJnt'], zero)
    riggUtils.grpIn('%s_leg_ctrlGrp' % side, zero)  # parent leg ctrlGrp, AUTO will be constraint to leg03_endJnt
    riggUtils.grpIn(parent, '%s_leg_ctrlGrp' % side) # parent to DIRECTION
    pm.parent(zero, jnts['%s_foot01' % side]['fkCtrl'])  # parent foot2
    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

    log_info("Done create_ctrl_fk_leg()")


def create_ctrl_ik_leg(jnts, side='L', parent='DIRECTION', scale=1):
    '''
    Args:
        jnts: joint dictionary
        side: 'R' or 'L'
    Returns:   joint dictionary
    '''

    color = biped.define_color(side)
    id = '%s_foot01' % side
    # check if exists
    if pm.objExists('%s_ikCtrl' % id):
        pm.select('%s_ikCtrl' % id)
        return '%s_ikCtrl Exists' % id

    # -- ik ctrl -- #
    jnts[id]['ikCtrl'] = curveLib.createShapeCtrl(type='cube', name='%s_ikCtrl' % id, scale=scale, color=color)
    # group and align
    zero = riggUtils.grpCtrl(jnts[id]['ikCtrl'])
    riggUtils.snap(jnts[id]['ctrlJnt'], zero, typeCnx='point')
    riggUtils.grpIn('%s_leg_ctrlGrp' % side, zero)  # parent leg_ctrlGrp

    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['ikCtrl']], listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)
    log_debug('limit')

    # gimbal
    gimbalCtrl = pm.duplicate(jnts[id]['ikCtrl'], n='%s_ikGimbalCtrl' % id)[0]

    pm.parent(gimbalCtrl, jnts[id]['ikCtrl'])
    pm.xform('%s.cv[0:]' % gimbalCtrl.getShape(), s=(.8, .8, .8), r=1)
    pm.addAttr(jnts[id]['ikCtrl'], ln='gimbal_vis', at='bool', k=1)
    jnts[id]['ikCtrl'].gimbal_vis >> gimbalCtrl.visibility
    # store attr of gimbal on main ctrl
    pm.addAttr(jnts[id]['ikCtrl'], ln='gimbal', dt='string')
    jnts[id]['ikCtrl'].attr('gimbal').set('%s' % gimbalCtrl, k=0, l=0, type='string')
    log_debug('gimal done')

    # -- pole vector -- #
    jnts[id]['pvecCtrl'] = curveLib.createShapeCtrl(type='sphere', name='%s_pvecCtrl' % id, scale=scale, color=color)
    # group and align
    zero = riggUtils.grpCtrl(jnts[id]['pvecCtrl'])
    log_debug('finding pole position')
    polePos = riggUtils.poleVectorPosition(startJnt=jnts['%s_leg01' % side]['ikJnt'],
                                           midJnt=jnts['%s_leg02' % side]['ikJnt'],
                                           endJnt=jnts['%s_foot01' % side]['ctrlJnt'], length=12, createLoc=0,
                                           createViz=0)
    log_debug('polepos is %s'%polePos)
    pm.xform(zero, ws=1, t=(polePos.x, polePos.y, polePos.z))
    riggUtils.grpIn('%s_leg_ctrlGrp' % side, zero)  # parent leg_ctrlGrp
    riggUtils.grpIn(parent, '%s_leg_ctrlGrp' % side)  # parent to DIRECTION

    # limit
    riggUtils.cleanUpAttr(sel=[jnts[id]['pvecCtrl']], listAttr=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'], l=0, k=0, cb=0)

    log_info("Done create_ctrl_ik_leg()")

    return jnts


def setup_fk_leg(jnts, RL='L'):

    # clean existing
    legJnts = [j for j in jnts.keys() if 'leg' in j or 'foot' in j]
    try:
        for legJnt in legJnts:
            riggUtils.deleteChildrenConstraints(jnts[legJnt]['fkJnt'])
    except:
        pass

    pm.parentConstraint(jnts['%s_leg01' % RL]['fkCtrl'], jnts['%s_leg01' % RL]['fkJnt'], mo=1,
                        n='%s_leg01_fkJnt_parentCon' % RL)
    pm.parentConstraint(jnts['%s_leg02' % RL]['fkCtrl'], jnts['%s_leg02' % RL]['fkJnt'], mo=1,
                        n='%s_leg02_fkJnt_parentCon' % RL)
    pm.parentConstraint(jnts['%s_leg03' % RL]['fkCtrl'], jnts['%s_leg03' % RL]['fkJnt'], mo=1,
                        n='%s_leg03_fkJnt_parentCon' % RL)

    # orient constraint will be shared by ik and fk ctrl, switch via reverse
    pm.parentConstraint(jnts['%s_foot01' % RL]['fkCtrl'], jnts['%s_foot01' % RL]['fkJnt'], mo=1,
                        n='%s_foot01_ctrlJnt_orientCon' % RL)
    pm.parentConstraint(jnts['%s_foot02' % RL]['fkCtrl'], jnts['%s_foot02' % RL]['fkJnt'], mo=1,
                        n='%s_foot02_ctrlJnt_orientCon' % RL)

    # constrain foot ctrl auto to leg end jnt
    end_jnt = jnts['%s_leg02' % RL]['fkJnt'].getChildren(type='joint')
    pm.parentConstraint(end_jnt, jnts['%s_foot01' % RL]['fkCtrl'].attr('AUTO').get(), mo=1)

    log_info("Done setup_fk_leg()")
    # TODO make leg follow chest. parentconstrain fkCtrl auto to clavJntEnd
    # TODO clavicle ctrlJnt connect. ik/fk switch
    #


def setup_ik_leg(jnts, RL='L'):


    ikj_leg = jnts['%s_leg01' % RL]['ikJnt']
    ikj_legend = pm.listRelatives(ikj_leg, children=1, ad=1, type='joint')[0]  # last child

    ikj_ankle = jnts['%s_foot01' % RL]['ikJnt']
    ikj_ball = jnts['%s_foot02' % RL]['ikJnt']
    ikj_toe = jnts['%s_foot03' % RL]['ikJnt']

    ikh_leg =   pm.ikHandle(sj=ikj_leg, ee=ikj_legend, sol='ikRPsolver', n='%s_leg_ikh' % RL)
    ikh_ball =  pm.ikHandle(sj=ikj_ankle, ee=ikj_ball, sol="ikSCsolver", n='%s_ball_ikh' % RL)
    ikh_toe =   pm.ikHandle(sj=ikj_ball, ee=ikj_toe, sol="ikSCsolver", n='%s_toe_ikh' % RL)

    # pole vector
    pm.poleVectorConstraint(jnts['%s_foot01' % RL]['pvecCtrl'], ikh_leg[0])

    # parent handle to ikCtrl or ikGimbalCtrl
    ik_ctrl = jnts['%s_foot01' % RL]['ikCtrl'] if not jnts['%s_foot01' % RL]['ikCtrl'].hasAttr('gimbal') \
        else pm.PyNode(jnts['%s_foot01' % RL]['ikCtrl'].attr('gimbal').get())
    pm.parent(ik[0], ik_ctrl)

    # this group is buffer that is aligned to foot01_ctrlJnt to orientConstrain without offset
    ik_grp = pm.createNode('transform', n='%s_foot01_ikGrp' % RL, p=ik_ctrl)
    riggUtils.snap(jnts['%s_foot01' % RL]['ctrlJnt'], ik_grp)

    con_node = pm.createNode('transform', n='%s_foot01_targetCon' % RL, p=ik_grp)
    # orient constraint will be shared by ik and fk ctrl, switch via reverse

    pm.orientConstraint(con_node, jnts['%s_foot01' % RL]['ctrlJnt'], mo=1, n='%s_foot01_ctrlJnt_orientCon' % RL)
    # for switch  L_foot01_fkCtrlMatch
    con_node = pm.createNode('transform', n='%s_foot01_fkCtrlMatch' % RL, p=ik_grp)

    # foot attributes
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='twist', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='roll', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='heelRoll', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='bend', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='side', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='toeRoll', at='double', k=1, min=0, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='toeSpin', at='double', k=1, min=-300, max=300.0)
    pm.addAttr(jnts['L_foot01']['ikCtrl'], ln='toeWiggle', at='double', k=1, min=-300, max=300.0)

    footGroups = ("grp_footPivot", "grp_heel", "grp_toe", "grp_ball", "grp_flap")
    for item in footGroups:
        cmds.group(n=item, empty=True, world=True)

    log_info('Done: setup_ik_leg')
    return ik


def setup_ikfkSwitch_leg(jnts, RL='L'):
    # - # create blend ctrl if not exists
    if pm.objExists('%s_leg_fkIkSwitch' % RL) == False:
        log_debug('No ctrl for blend found. Building')
        color = biped.define_color(RL)
        log_debug('create switch')
        switch = create_ctrl_ikfkSwitch(name='%s_leg_fkIkSwitch' % RL, color=color, parent='%s_leg_ctrlGrp' % RL)
        log_debug('constrain')
        pm.parentConstraint(jnts['%s_foot01' % RL]['ctrlJnt'], switch.attr('ZERO').get(), mo=0)
    else:
        log_debug('switch ctrl already exists. skippin')
        switch = pm.PyNode('%s_leg_fkIkSwitch' % RL)
    #jnts['%s_foot01' % RL]['switchCtrl'] = switch

    # - # create blendnodes for rot/trans/scale for leg01 and leg02
    for i in [1, 2, 3]:  # leg01 and leg02
        # blend node
        log_debug( jnts['%s_leg%02d' % (RL, i)] )
        jnt_name = jnts['%s_leg%02d' % (RL, i)]['ctrlJnt'].name()

        # delete existing
        for attr in ['transBlend', 'rotBlend', 'scaleBlend']:
            pm.delete(pm.ls('%s_%s' % (jnt_name, attr)))

        blend_trans = pm.createNode('blendColors', n='%s_transBlend' % jnt_name)
        blend_rot = pm.createNode('blendColors', n='%s_rotBlend' % jnt_name)
        blend_scale = pm.createNode('blendColors', n='%s_scaleBlend' % jnt_name)

        jnts['%s_leg%02d' % (RL, i)]['fkJnt'].t >> blend_trans.color2
        jnts['%s_leg%02d' % (RL, i)]['ikJnt'].t >> blend_trans.color1
        blend_trans.output >> jnts['%s_leg%02d' % (RL, i)]['ctrlJnt'].t

        jnts['%s_leg%02d' % (RL, i)]['fkJnt'].r >> blend_rot.color2
        jnts['%s_leg%02d' % (RL, i)]['ikJnt'].r >> blend_rot.color1
        blend_rot.output >> jnts['%s_leg%02d' % (RL, i)]['ctrlJnt'].r

        jnts['%s_leg%02d' % (RL, i)]['fkJnt'].s >> blend_scale.color2
        jnts['%s_leg%02d' % (RL, i)]['ikJnt'].s >> blend_scale.color1
        blend_scale.output >> jnts['%s_leg%02d' % (RL, i)]['ctrlJnt'].s

        switch = pm.PyNode('%s_leg_fkIkSwitch' % RL)

        log_debug('connecting')
        switch.fkIk >> blend_trans.blender
        switch.fkIk >> blend_rot.blender
        switch.fkIk >> blend_scale.blender

    # -- foot--#
    # foot01_ctrlJnt - weight blend existing orient constrain
    const = pm.PyNode('%s_foot01_ctrlJnt_orientCon' % RL)
    weightList = const.getWeightAliasList()

    rev = pm.createNode('reverse', n='%s_legIkFk_rev' % RL)
    switch.fkIk >> weightList[1]
    switch.fkIk >> rev.inputX
    rev.outputX >> weightList[0]

    # hook up visibility of ctrls
    rev.outputX >> pm.PyNode(jnts['%s_leg01' % RL]['fkCtrl'].attr('ZERO').get()).visibility
    rev.outputX >> jnts['%s_leg01' % RL]['fkJnt'].visibility
    rev.outputX >> pm.PyNode(jnts['%s_foot01' % RL]['fkCtrl'].attr('ZERO').get()).visibility

    switch.fkIk >> pm.PyNode(jnts['%s_foot01' % RL]['ikCtrl'].attr('ZERO').get()).visibility
    switch.fkIk >> jnts['%s_leg01' % RL]['ikJnt'].visibility

    log_info('Done: setup_ik_leg')
    return jnts


def create_ctrl_ikfkSwitch(name='L_leg_fkIkSwitch', color='blue', parent=None, scale=1):
    """
    Args:
        name:
        color:
        parent:
    Returns:

    """
    fkikSwitch = curveLib.createShapeCtrl(type='crossPaddle', name=name, scale=scale, color=color)
    # addd 'rotOrder'

    lmin = -90
    lmax = 90

    # fkik stretchy
    attrs = ['fkIk', 'stretchy']
    pm.addAttr(fkikSwitch, ln='fkIk', at='double', k=1, min=0, max=1)
    pm.addAttr(fkikSwitch, ln='stretchy', at='long', k=1, min=0, max=1)

    # group and limit
    zero = riggUtils.grpCtrl(fkikSwitch)
    riggUtils.cleanUpAttr(sel=fkikSwitch, listAttr=['sx', 'sy', 'sz', 'rx', 'ry', 'rz', 'tx', 'ty', 'tz'], l=0, k=0,
                          cb=0)
    if parent is not None:
        riggUtils.snap(parent, zero)
        pm.parent(zero, parent)

    return fkikSwitch


def setup_fk_stretch_leg(jnts, RL='L'):
    # add lenght attribute to ctrl and hook it up to fkJnt_ZERO length
    for i in [1, 2]:  # arm01 and arm02
        # adda

        node_to_trans = pm.PyNode(jnts['%s_leg%02d' % (RL, i + 1)]['fkCtrl'].AUTO.get())
        try:
            pm.addAttr(jnts['%s_leg%02d' % (RL, i)]['fkCtrl'], ln='length', at='double', k=1, min=0, max=10.0)
        except:
            pass

        jnts['%s_leg%02d' % (RL, i)]['fkCtrl'].length >> node_to_trans.tx


def setup_ik_stretch_leg(jnts, RL='L'):
    ### TODO: consider global scale, stretch attribute on/off on ik Ctlr
    ### TODO: split up upper and lower leg stretch amound (as seen in AM steward)

    # distance measure. 2 locators, parent foot and up_leg
    dd = pm.distanceDimension(sp=jnts['L_leg01']['ikJnt'].t.get(), ep=jnts['L_foot01']['ctrlJnt'].t.get(), )
    pm.rename(dd.getParent(), '%s_leg_ik_dist' % RL)

    start_loc = pm.spaceLocator(n='%s_leg_ik_startDist' % RL)
    end_loc = pm.spaceLocator(n='%s_leg_ik_endDist' % RL)
    pm.pointConstraint(jnts['L_leg01']['ikJnt'], start_loc)
    pm.pointConstraint('%s_leg_ikHandle' % RL, end_loc)
    # connect loc to distanceNode
    start_loc.t >> dd.startPoint
    end_loc.t >> dd.endPoint

    riggUtils.grpIn('L_legikJnt_distGrp', [start_loc, end_loc])
    log_debug('dist create done')

    # sum_leg_tx to compare. ADD UP UP LOW DISTANCfE

    leg02_tx_orig = pm.createNode('plusMinusAverage', n='%s_leg02StrOrig_plsMns')
    leg02_tx_orig.input1D[0].set(jnts['L_leg02']['ikJnt'].tx.get())
    leg03_tx_orig = pm.createNode('plusMinusAverage', n='%s_leg03StrOrig_plsMns')
    leg03_tx_orig.input1D[1].set(jnts['L_leg03']['ikJnt'].tx.get())

    leg_tx_orig = pm.createNode('plusMinusAverage', n='%s_legStrOrig_plsMns')
    leg02_tx_orig.output1D >> leg_tx_orig.input1D[0]
    leg03_tx_orig.output1D >> leg_tx_orig.input1D[1]
    log_debug('summing up tx to compare done')

    # divide dist node by summed

    stretch_factor_mult = pm.createNode('multiplyDivide', n='%s_legStrFactor_mult')
    leg_tx_orig.output1D >> stretch_factor_mult.input2X
    dd.distance >> stretch_factor_mult.input1X
    stretch_factor_mult.operation.set(2)
    log_debug('figure out distance multiplyer done')

    # clamp output 1 to max stretch (don't want to go below 1, squash..)
    clamp_stretch = pm.createNode('clamp', n='%s_legStr_clamp' % RL)
    clamp_stretch.minR.set(1)
    clamp_stretch.maxR.set(3)
    # TODO: max stretch sett a attribute for it animator can adjust
    stretch_factor_mult.outputX >> clamp_stretch.inputR
    log_debug('clamp done')

    # multiply tx fo leg02 and 03 with stretch
    stretch_mult = pm.createNode('multiplyDivide', n='%s_legStr_mult')
    clamp_stretch.outputR >> stretch_mult.input2X
    clamp_stretch.outputR >> stretch_mult.input2Y
    leg02_tx_orig.output1D >> stretch_mult.input1X
    leg03_tx_orig.output1D >> stretch_mult.input1Y
    log_debug('mult tx to leg 02/03 stretch done')

    # now connect that to actual ikJnt TX
    stretch_mult.outputX >> jnts['L_leg02']['ikJnt'].tx
    stretch_mult.outputY >> jnts['L_leg03']['ikJnt'].tx
    log_debug('connecting done')

# jnts = {}
# jnts['root'] = 'root_jnt'
# jnts['torso1'] = pm.PyNode('C_torso1_jnt')
# jnts['torso2'] = pm.PyNode('C_torso2_jnt')
# jnts['torso3'] = pm.PyNode('C_torso3_jnt')
# jnts['torso4'] = pm.PyNode('C_torso4_jnt')
# 
# side = 'L'
# jnts['upleg']  = pm.PyNode('%s_upleg_jnt'%side)
# jnts['lowleg']  = pm.PyNode('%s_lowleg_jnt'%side)
# jnts['foot']  = pm.PyNode('%s_foot_jnt'%side)
# 
# # ik footles
# 
# # locs
# heel_loc = pm.spaceLocator(n='%s_heel_loc'%side)
# ball_loc = pm.spaceLocator(n='%s_ball_loc'%side)
# toe_loc = pm.spaceLocator(n='%s_toe_loc'%side)
# inside_loc = pm.spaceLocator(n='%s_inside_loc'%side)
# outside_loc = pm.spaceLocator(n='%s_outside_loc'%side)
#
