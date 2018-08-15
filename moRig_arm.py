import pymel.core as pm
import sys
import mo_Utils.mo_riggUtils as riggUtils
import mo_Utils.mo_curveLib as curveLib
import moRig_biped as biped
import moRig_settings as settings
import moRig_utils as utils

reload(biped)
reload(riggUtils)
reload(curveLib)

import logging
logger = logging.getLogger('root')
logging.basicConfig(format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
logger.setLevel(logging.DEBUG)

getframe_expr = 'sys._getframe({}).f_code.co_name'
def log_debug(msg='caller'):
	logger.debug('%s: %s' % (eval(getframe_expr.format(2)), msg))
def log_info(msg='caller'):
	logger.info('%s: %s' % (eval(getframe_expr.format(2)), msg))




'''
addScriptPath('D:\Google Drive\PythonScripting\my_autoRigger')
import mo_biped as biped
import mo_arm as arm
reload(arm)

'''

def test():
	debug_msg('testcall')

def define_jnts(jnts={}, parts=['spine', 'head', 'arm', 'leg'], part=['ctrl'], sides=['R', 'L']):
	jnts['root'] = 'root_ctrlJnt'
	jnts['spine01'] = {'ctrlJnt': pm.PyNode('C_spine01_ctrlJnt')}
	jnts['spine02'] = {'ctrlJnt': pm.PyNode('C_spine02_ctrlJnt')}
	jnts['spine03'] = {'ctrlJnt': pm.PyNode('C_spine03_ctrlJnt')}
	jnts['spine04'] = {'ctrlJnt': pm.PyNode('C_spine04_ctrlJnt')}
	jnts['pelvis01'] = {'ctrlJnt': pm.PyNode('C_pelvis01_ctrlJnt')}
	jnts['chest01'] = {'ctrlJnt': pm.PyNode('C_chest01_ctrlJnt')}
	jnts['neck01'] = {'ctrlJnt': pm.PyNode('C_neck01_ctrlJnt')}
	jnts['head01'] = {'ctrlJnt': pm.PyNode('C_head01_ctrlJnt')}
	# jnts['jaw'] = {'ctrlJnt': pm.PyNode('C_jaw01_ctrlJnt')}
	# arm
	for side in ['L', 'R']:
		jnts['%s_clavicle01' % side] = {'ctrlJnt': pm.PyNode('%s_clav01_ctrlJnt' % side),
										'fkJnt': pm.PyNode('%s_clav01_fkJnt' % side)}
		jnts['%s_arm01' % side] = {'ctrlJnt': pm.PyNode('%s_arm01_ctrlJnt' % side),
								   'fkJnt': pm.PyNode('%s_arm01_fkJnt' % side),
								   'ikJnt': pm.PyNode('%s_arm01_ikJnt' % side)}
		jnts['%s_arm02' % side] = {'ctrlJnt': pm.PyNode('%s_arm02_ctrlJnt' % side),
								   'fkJnt': pm.PyNode('%s_arm02_fkJnt' % side),
								   'ikJnt': pm.PyNode('%s_arm02_ikJnt' % side)}
		jnts['%s_hand01' % side] = {'ctrlJnt': pm.PyNode('%s_hand01_ctrlJnt' % side)}
		jnts['%s_eye01' % side] = {'ctrlJnt': pm.PyNode('%s_eye01_ctrlJnt' % side)}

		return jnts


def build_ctrlJnts_arm(jnts={}, side='L'):
	'''
	create ctrl joints for arm
	'''
	log_debug ( 'side is %s' % side )
	pm.createNode('transform', name='%s_arm_jntGrp' % side)
	riggUtils.grpIn('Skeleton_grp', '%s_arm_jntGrp' % side)

	# arm
	arm = pm.duplicate('%s_arm01_skinJnt' % side, n='%s_arm01_ctrlJnt' % side)[0]
	jnts['%s_arm01' % side] = {'ctrlJnt': arm}
	pm.select(arm)
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")
	pm.parent(arm, '%s_arm_jntGrp' % side)
	riggUtils.grpCtrl(arm)

	# deal with children
	for childJnt in pm.listRelatives(arm, children=1, type='joint', ad=1):

		if childJnt == ('%s_hand01_ctrlJnt' % side):
			pm.rename(childJnt, '%s_arm03_ctrlJntEnd' % side)  # create end joint from hand
			# delete fingers
			pm.delete(pm.listRelatives('%s_arm03_ctrlJntEnd' % side, children=1, ad=1))
			break

	# clavicle
	clav = pm.duplicate('%s_clav01_skinJnt' % side, n='%s_clav01_ctrlJnt' % side)[0]
	jnts['%s_clavicle' % side] = {'ctrlJnt': clav}

	riggUtils.grpIn('%s_arm_jntGrp' % side, clav)
	riggUtils.grpCtrl(clav)

	# deal with children
	for childJnt in pm.listRelatives(clav, children=1, type='joint', ad=1):
		log_debug( 'childJnt clav %s' % childJnt )
		if childJnt.nodeName() == ('%s_arm01_skinJnt' % side):
			pm.delete(childJnt.listRelatives(children=1))
			pm.rename(childJnt, '%s_clav01_ctrlJntEnd' % side)  # create end joint from hand
		else:
			pm.delete(childJnt)

	pm.select(clav)
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")

	# hand
	hand = pm.duplicate('%s_hand01_skinJnt' % side, n='%s_hand01_ctrlJnt' % side)[0]
	jnts['%s_hand01' % side] = {'ctrlJnt': hand}
	pm.select(hand)
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")

	riggUtils.grpIn('%s_arm_jntGrp' % side, hand)
	riggUtils.grpCtrl(hand)

	endjnt = hand.listRelatives(children=1)[0]

	# pm.delete(endjnt.listRelatives(children=1, ad=1))
	fingers = endjnt.listRelatives(children=1)
	finger_grp = pm.group(fingers, n='%s_fingersCtrlJnt_grp' % side)
	riggUtils.grpIn('%s_arm_jntGrp' % side, finger_grp)

	# constrain hand AUTO to arm03End
	pm.pointConstraint('%s_arm03_ctrlJntEnd' % side, pm.getAttr('%s_hand01_ctrlJnt.AUTO' % side))


	# finger

	# constrain fingerGrp AUTO to hand01
	pm.parentConstraint(hand, finger_grp, mo=1)





def build_jnts_arm(jnts={}, mode=['ik', 'fk']):
	'''
	Build arm jnts FK and IK by duplicating ctrlJnts
	Args:
	    jnts:
	    mode:

	Returns:

	'''
	for RL in ['R', 'L']:

		if '%s_arm01' % RL in jnts:
			if 'fk' in mode:
				if pm.objExists('%s_arm01_fkJnt' % RL): pm.delete('%s_arm01_fkJnt' % RL) # delete existing
				fkJnt = pm.duplicate(jnts['%s_arm01' % RL]['ctrlJnt'], n='%s_arm01_fkJnt' % RL)
				log_debug( 'creating fkJnt %s' % fkJnt )
				pm.select(fkJnt)
				pm.mel.searchReplaceNames("_ctrlJnt", "_fkJnt", "hierarchy")
			if 'ik' in mode:
				if pm.objExists('%s_arm01_ikJnt' % RL): pm.delete('%s_arm01_ikJnt' % RL)  # delete existing
				ikJnt = pm.duplicate(jnts['%s_arm01' % RL]['ctrlJnt'], n='%s_arm01_ikJnt' % RL)
				log_debug( 'creating ikJnt %s' % ikJnt )
				pm.select(ikJnt)
				pm.mel.searchReplaceNames("_ctrlJnt", "_ikJnt", "hierarchy")

			# jnts.update(define_fkJnts())
			# jnts.update(define_ikJnts())


def create_ctrl_ik_arm(jnts, side='L', parent='DIRECTION'):
	'''
	Args:
	    jnts: joint dictionary
	    side: 'R' or 'L'
	Returns:   joint dictionary
	'''

	color = biped.define_color(side)
	id = '%s_hand01' % side
	# check if exists
	if pm.objExists('%s_ikCtrl' % id):
		pm.select('%s_ikCtrl' % id)
		return '%s_ikCtrl Exists' % id

	# -- ik ctrl -- #
	jnts[id]['ikCtrl'] = curveLib.createShapeCtrl(type='cube', name='%s_ikCtrl' % id, scale=1, color=color)
	# group and align
	zero = riggUtils.grpCtrl(jnts[id]['ikCtrl'])
	riggUtils.snap(jnts[id]['ctrlJnt'], zero, typeCnx='point')
	riggUtils.grpIn('%s_arm_ctrlGrp' % side, zero)  # parent arm_ctrlGrp

	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['ikCtrl']], listAttr=['sx', 'sy', 'sz'], l=0, k=0, cb=0)

	# gimbal
	gimbalCtrl = pm.duplicate(jnts[id]['ikCtrl'], n='%s_ikGimbalCtrl' % id)[0]
	log_debug( 'GimbalCtrl is %s'%gimbalCtrl )

	pm.parent(gimbalCtrl, jnts[id]['ikCtrl'] )
	pm.xform('%s.cv[0:]'%gimbalCtrl.getShape(), s=(.8, .8, .8), r=1)
	pm.addAttr(jnts[id]['ikCtrl'],  ln='gimbal_vis', at='bool', k=1)
	jnts[id]['ikCtrl'].gimbal_vis >> gimbalCtrl.visibility
	# store attr of gimbal on main ctrl
	pm.addAttr(jnts[id]['ikCtrl'], ln='gimbal', dt='string')
	jnts[id]['ikCtrl'].attr('gimbal').set('%s' % gimbalCtrl, k=0, l=0, type='string')


	# -- pole vector -- #
	jnts[id]['pvecCtrl'] = curveLib.createShapeCtrl(type='sphere', name='%s_pvecCtrl' % id, scale=1, color=color)
	# group and align
	zero = riggUtils.grpCtrl(jnts[id]['pvecCtrl'])
	polePos = riggUtils.poleVectorPosition(startJnt=jnts['%s_arm01' % side]['ikJnt'],
										   midJnt=jnts['%s_arm02' % side]['ikJnt'],
										   endJnt=jnts['%s_hand01' % side]['ctrlJnt'], length=12, createLoc=0,
										   createViz=0)
	pm.xform(zero, ws=1, t=(polePos.x, polePos.y, polePos.z))
	riggUtils.grpIn('%s_arm_ctrlGrp' % side, zero)  # parent arm_ctrlGrp
	riggUtils.grpIn(parent, '%s_arm_ctrlGrp' % side)  # parent to DIRECTION


	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['pvecCtrl']], listAttr=['sx', 'sy', 'sz', 'rx', 'ry', 'rz'], l=0, k=0, cb=0)

	# snap

	return jnts


def create_ctrl_fk_arm(jnts, side='L', parent='DIRECTION'):
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

	id = '%s_arm01' % side
	jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=1, color=color)
	# pm.xform('%sShape.cv[0:]' % jnts[id]['fkCtrl'], s=(1.75, 1, 1), t=(1.5, 0, 0), r=1)
	# group and align
	zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
	riggUtils.snap(jnts[id]['fkJnt'], zero)
	riggUtils.grpIn('%s_arm_ctrlGrp' % side, zero)  # parent arm_ctrlGrp
	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

	id = '%s_arm02' % side
	jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=1, color=color)
	# group and align
	zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
	riggUtils.snap(jnts[id]['fkJnt'], zero)
	pm.parent(zero, jnts['%s_arm01' % side]['fkCtrl'])  # parent arm01
	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

	# arm03 is technically hand in human setup, so we will hide ctrl
	# arm03_ctrl drive arm03_endJnt and therefore hand01_ctrl and will be used for stretch setup
	# to hook up length to zero tx
	id = '%s_arm03' % side
	jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=1, color=color)
	# group and align
	zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
	riggUtils.snap(jnts[id]['fkJnt'], zero)
	pm.parent(zero, jnts['%s_arm02' % side]['fkCtrl'])  # parent arm01
	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)
	zero.hide()

	id = '%s_hand01' % side
	jnts[id]['fkCtrl'] = curveLib.createShapeCtrl(type='circle', name='%s_fkCtrl' % id, scale=.75, color=color)
	# group and align
	zero = riggUtils.grpCtrl(ctrl=jnts[id]['fkCtrl'], sdk=1)
	riggUtils.snap(jnts[id]['ctrlJnt'], zero)
	riggUtils.grpIn('%s_arm_ctrlGrp' % side, zero)  # parent arm ctrlGrp, AUTO will be constraint to arm03_endJnt
	riggUtils.grpIn(parent, '%s_arm_ctrlGrp' % side)  # parent to DIRECTION
	# limit
	riggUtils.cleanUpAttr(sel=[jnts[id]['fkCtrl']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

def create_ctrl_shoulder(jnts, RL='L'):
	'''

	Args:
	    jnts: joint dictionary
	    side: 'R' or 'L'
	Returns:   joint dictionary
	'''
	if RL == 'L':
		color = 'blue'
	else:
		color = 'red'
	# TODO clavicle is not part of jnts{} dictionary
	jnts['%s_clav01'%RL]['fkCtrl'] = curveLib.createShapeCtrl(type='squareAxis45', name='%s_clav_fkCtrl'%RL, scale=1, color=color)
	# pm.xform('%sShape.cv[0:]' % jnts[id]['fkCtrl'], s=(1.75, 1, 1), t=(1.5, 0, 0), r=1)
	# group and align
	zero = riggUtils.grpCtrl(ctrl=jnts['%s_clav01'%RL]['fkCtrl'], sdk=1)
	riggUtils.snap(['%s_clav01'%RL]['fkJnt'], zero)
	riggUtils.grpIn('%s_arm_ctrlGrp' % RL, zero)  # parent arm_ctrlGrp
	# limit
	riggUtils.cleanUpAttr(sel=[['%s_clav01'%RL]['fkJnt']], listAttr=['sx', 'sy', 'sz', 'tx', 'ty', 'tz'], l=0, k=0, cb=0)

def setup_fk_arm(jnts, RL='L'):
	log_debug('Enter')

	# clean existing
	# riggUtils.deleteChildrenConstraints(
	# 	[jnts['%s_arm01' % RL]['fkJnt'], jnts['%s_arm02' % RL]['fkJnt'], jnts['%s_hand01' % RL]['ctrlJnt']])
	#
	pm.parentConstraint(jnts['%s_arm01' % RL]['fkCtrl'], jnts['%s_arm01' % RL]['fkJnt'], mo=1, n='%s_arm01_fkJnt_parentCon'%RL)
	pm.parentConstraint(jnts['%s_arm02' % RL]['fkCtrl'], jnts['%s_arm02' % RL]['fkJnt'], mo=1, n='%s_arm02_fkJnt_parentCon'%RL)
	pm.parentConstraint(jnts['%s_arm03' % RL]['fkCtrl'], jnts['%s_arm03' % RL]['fkJnt'], mo=1, n='%s_arm03_fkJnt_parentCon' % RL)
	# orient constraint will be shared by ik and fk ctrl, switch via reverse
	pm.orientConstraint(jnts['%s_hand01' % RL]['fkCtrl'], jnts['%s_hand01' % RL]['ctrlJnt'], mo=1, n='%s_hand01_ctrlJnt_orientCon'%RL)

	# constrain hand ctrl auto to arm end jnt
	end_jnt = jnts['%s_arm02' % RL]['fkJnt'].getChildren(type='joint')
	pm.parentConstraint(end_jnt, jnts['%s_hand01' % RL]['fkCtrl'].attr('AUTO').get(), mo=1)

	# TODO make arm follow chest. parentconstrain fkCtrl auto to clavJntEnd
	# TODO clavicle ctrlJnt connect. ik/fk switch
	#


def setup_ik_arm(jnts, RL='L'):
	log_debug('Enter')

	startjoint = jnts['%s_arm01' % RL]['ikJnt']
	endJoint = pm.listRelatives(startjoint, children=1, ad=1, type='joint')[0]  # last child

	ik = pm.ikHandle(sj=startjoint, ee=endJoint, sol='ikRPsolver', n='%s_arm_ikHandle'%RL)

	# pole vector
	pm.poleVectorConstraint(jnts['%s_hand01' % RL]['pvecCtrl'], ik[0])

	# parent handle to ikCtrl or ikGimbalCtrl
	ik_ctrl = jnts['%s_hand01' % RL]['ikCtrl'] if not jnts['%s_hand01' % RL]['ikCtrl'].hasAttr('gimbal') \
		else pm.PyNode(jnts['%s_hand01' % RL]['ikCtrl'].attr('gimbal').get())
	pm.parent(ik[0], ik_ctrl)

	# this group is buffer that is aligned to hand01_ctrlJnt to orientConstrain without offset
	ik_grp = pm.createNode('transform',n='%s_hand01_ikGrp'%RL, p=ik_ctrl)
	riggUtils.snap(jnts['%s_hand01' % RL]['ctrlJnt'], ik_grp)

	con_node = pm.createNode('transform',n='%s_hand01_targetCon'%RL, p=ik_grp)
	# orient constraint will be shared by ik and fk ctrl, switch via reverse
	pm.orientConstraint(con_node, jnts['%s_hand01' % RL]['ctrlJnt'], mo=1, n='%s_hand01_ctrlJnt_orientCon'%RL)

	# for switch  L_hand01_fkCtrlMatch
	con_node = pm.createNode('transform',n='%s_hand01_fkCtrlMatch'%RL, p=ik_grp)
	log_info('Done')
	return ik


def setup_ikfkSwitch_arm(jnts, RL='L'):
	log_debug('Enter')

	# - # create blend ctrl if not exists
	if pm.objExists('%s_arm_fkIkSwitch' % RL) == False:
		log_debug('No ctrl for blend found. Building')
		color = biped.define_color(RL)
		log_debug('create switch' )
		switch = create_ctrl_ikfkSwitch(name='%s_arm_fkIkSwitch' % RL, color=color, parent='%s_arm_ctrlGrp' % RL)
		log_debug('constrain' )
		pm.parentConstraint(jnts['%s_hand01' % RL]['ctrlJnt'], switch.attr('ZERO').get(), mo=0)
	else:
		log_debug('switch ctrl already exists. skippin')
		switch = pm.PyNode('%s_arm_fkIkSwitch' % RL)
	#jnts['%s_hand01' % RL]['switchCtrl'] = switch

	# - # create blendnodes for rot/trans/scale for arm01 and arm02
	for i in [1, 2, 3]:  # arm01 and arm02
		# blend node
		jnt_name = jnts['%s_arm%02d' % (RL, i)]['ctrlJnt'].name()

		# delete existing
		for attr in ['transBlend', 'rotBlend', 'scaleBlend']:
			pm.delete(pm.ls('%s_%s' % (jnt_name, attr)))

		blend_trans = pm.createNode('blendColors', n='%s_transBlend' % jnt_name)
		blend_rot = pm.createNode('blendColors', n='%s_rotBlend' % jnt_name)
		blend_scale = pm.createNode('blendColors', n='%s_scaleBlend' % jnt_name)

		jnts['%s_arm%02d' % (RL, i)]['fkJnt'].t >> blend_trans.color2
		jnts['%s_arm%02d' % (RL, i)]['ikJnt'].t >> blend_trans.color1
		blend_trans.output >> jnts['%s_arm%02d' % (RL, i)]['ctrlJnt'].t

		jnts['%s_arm%02d' % (RL, i)]['fkJnt'].r >> blend_rot.color2
		jnts['%s_arm%02d' % (RL, i)]['ikJnt'].r >> blend_rot.color1
		blend_rot.output >> jnts['%s_arm%02d' % (RL, i)]['ctrlJnt'].r

		jnts['%s_arm%02d' % (RL, i)]['fkJnt'].s >> blend_scale.color2
		jnts['%s_arm%02d' % (RL, i)]['ikJnt'].s >> blend_scale.color1
		blend_scale.output >> jnts['%s_arm%02d' % (RL, i)]['ctrlJnt'].s

		switch = pm.PyNode('%s_arm_fkIkSwitch' % RL)

		log_debug('connecting')

		switch.fkIk >> blend_trans.blender
		switch.fkIk >> blend_rot.blender
		switch.fkIk >> blend_scale.blender

	# -- hand--#
	# hand01_ctrlJnt - weight blend existing orient constrain
	const = pm.PyNode('%s_hand01_ctrlJnt_orientCon'%RL)
	weightList = const.getWeightAliasList()

	rev= pm.createNode('reverse', n ='%s_armIkFk_rev'%RL)
	switch.fkIk >> weightList[1]
	switch.fkIk >> rev.inputX
	rev.outputX >> weightList[0]

	# hook up visibility of ctrls
	rev.outputX >> pm.PyNode(jnts['%s_arm01' %RL]['fkCtrl'].attr('ZERO').get()).visibility
	rev.outputX >> jnts['%s_arm01' %RL]['fkJnt'].visibility
	rev.outputX >> pm.PyNode(jnts['%s_hand01' % RL]['fkCtrl'].attr('ZERO').get()).visibility

	switch.fkIk >> pm.PyNode(jnts['%s_hand01'%RL]['ikCtrl'].attr('ZERO').get()).visibility
	switch.fkIk >> jnts['%s_arm01' %RL]['ikJnt'].visibility



def create_ctrl_ikfkSwitch(name='L_arm_fkIkSwitch', color='blue', parent=None):

	"""
	Args:
	    name:
	    color:
	    parent:
	Returns:

	"""
	fkikSwitch = curveLib.createShapeCtrl(type='crossPaddle', name=name, scale=1, color=color)
	# addd 'rotOrder'

	lmin = -90
	lmax = 90

	# fkik stretchy
	attrs = ['fkIk', 'stretchy']
	pm.addAttr(fkikSwitch, ln='fkIk', at='double', k=1, min=0, max=1)
	pm.addAttr(fkikSwitch, ln='stretchy', at='long', k=1, min=0, max=1)

	pm.addAttr(fkikSwitch, ln='fingerCtrl', at='enum', en='---------------')
	pm.setAttr('%s.fingerCtrl' % fkikSwitch, cb=1, k=0, l=1)

	pm.addAttr(fkikSwitch, ln='fingerCtrlVis', at='bool')
	pm.setAttr('%s.fingerCtrl' % fkikSwitch, cb=1, k=0, l=0)

	# finger all
	pm.addAttr(fkikSwitch, ln='fingerAllCtrl', at='enum', en='---------------')
	pm.setAttr('%s.fingerAllCtrl' % fkikSwitch, cb=1, k=0, l=1)

	attrs = ['cup', 'spread', 'curlAll', 'fngThumbCurl', 'fngIndexCurl', 'fngMidCurl', 'fngRingCurl', 'fngPinkyCurl']
	for attr in attrs:
		pm.addAttr(ln=attr, at='double', k=1, min=lmin, max=lmax)

	# seperate fingers
	for finger in ['Thumb', 'Index', 'Mid', 'Ring', 'Pinky']:
		pm.addAttr(fkikSwitch, ln='fng%sCtrl' % finger, at='enum', en='---------------')
		pm.setAttr('%s.fng%sCtrl' % (fkikSwitch, finger), cb=1, k=0, l=1)

		pm.addAttr(ln='fng%sBaseCurl' % finger, at='double', k=1, min=lmin, max=lmax)
		pm.addAttr(ln='fng%sBaseSpread' % finger, at='double', k=1, min=lmin, max=lmax)
		pm.addAttr(ln='fng%s01Curl' % finger, at='double', k=1, min=lmin, max=lmax)
		pm.addAttr(ln='fng%s02Curl' % finger, at='double', k=1, min=lmin, max=lmax)
		pm.addAttr(ln='fng%s03Curl' % finger, at='double', k=1, min=lmin, max=lmax)

	# fkikSwitchGrp = pm.group(n='%sCON' % name)
	# riggUtils.movePivot(fkikSwitch, fkikSwitchGrp)
	zero = riggUtils.grpCtrl(fkikSwitch)

	# limit
	riggUtils.cleanUpAttr(sel=fkikSwitch, listAttr=['sx', 'sy', 'sz', 'rx', 'ry', 'rz', 'tx', 'ty', 'tz'], l=0, k=0,
						  cb=0)

	if parent is not None:
		riggUtils.snap(parent, zero)
		pm.parent(zero, parent)

	return fkikSwitch



def setup_fk_stretch_arm(jnts, RL='L'):

	# add lenght attribute to ctrl and hook it up to fkJnt_ZERO length
	for i in [1, 2]:  # arm01 and arm02
		# adda

		node_to_trans = pm.PyNode(jnts['%s_arm%02d' % (RL, i+1)]['fkCtrl'].AUTO.get())
		try:
			pm.addAttr(jnts['%s_arm%02d' % (RL, i)]['fkCtrl'], ln='length', at='double', k=1, min=0, max=10.0)
		except:
			pass

		jnts['%s_arm%02d' % (RL, i)]['fkCtrl'].length >> node_to_trans.tx



def setup_ik_stretch_arm(jnts, RL='L'):

	### TODO: consider global scale, stretch attribute on/off on ik Ctlr
	### TODO: split up upper and lower arm stretch amound (as seen in AM steward)

	# distance measure. 2 locators, parent hand and up_arm
	dd = pm.distanceDimension(sp=jnts['%s_arm01'%RL]['ikJnt'].t.get(), ep=jnts['%s_hand01'%RL]['ctrlJnt'].t.get(),)
	pm.rename(dd.getParent(), '%s_arm_ik_dist'%RL)

	start_loc = pm.spaceLocator(n='%s_arm_ik_startDist'%RL)
	end_loc = pm.spaceLocator(n='%s_arm_ik_endDist'%RL)
	pm.pointConstraint(jnts['%s_arm01'%RL]['ikJnt'], start_loc)
	pm.pointConstraint('%s_arm_ikHandle'%RL, end_loc)
	# connect loc to distanceNode
	start_loc.t >> dd.startPoint
	end_loc.t >> dd.endPoint

	riggUtils.grpIn('%s_armikJnt_distGrp'%RL, [start_loc, end_loc])
	log_debug('dist create done')

	# sum_arm_tx to compare. ADD UP UP LOW DISTANCfE

	arm02_tx_orig = pm.createNode('plusMinusAverage', n='%s_arm02StrOrig_plsMns'%RL)
	arm02_tx_orig.input1D[0].set(jnts['%s_arm02'%RL]['ikJnt'].tx.get())
	arm03_tx_orig = pm.createNode('plusMinusAverage', n='%s_arm03StrOrig_plsMns'%RL)
	arm03_tx_orig.input1D[1].set(jnts['%s_arm03'%RL]['ikJnt'].tx.get())

	arm_tx_orig = pm.createNode('plusMinusAverage', n='%s_armStrOrig_plsMns'%RL)
	arm02_tx_orig.output1D >> arm_tx_orig.input1D[0]
	arm03_tx_orig.output1D >> arm_tx_orig.input1D[1]
	log_debug('summing up tx to compare done')

	# divide dist node by summed

	stretch_factor_mult = pm.createNode('multiplyDivide', n='%s_armStrFactor_mult'%RL)
	arm_tx_orig.output1D >> stretch_factor_mult.input2X
	dd.distance >> stretch_factor_mult.input1X
	stretch_factor_mult.operation.set(2)
	log_debug('figure out distance multiplyer done')

	# clamp output 1 to max stretch (don't want to go below 1, squash..)
	clamp_stretch =pm.createNode('clamp', n='%s_armStr_clamp'%RL)
	clamp_stretch.minR.set(1)
	clamp_stretch.maxR.set(3)
	# TODO: max stretch sett a attribute for it animator can adjust
	stretch_factor_mult.outputX >> clamp_stretch.inputR
	log_debug('clamp done')

	# multiply tx fo arm02 and 03 with stretch
	stretch_mult = pm.createNode('multiplyDivide', n='%s_armStr_mult'%RL)
	clamp_stretch.outputR >> stretch_mult.input2X
	clamp_stretch.outputR >> stretch_mult.input2Y
	arm02_tx_orig.output1D >> stretch_mult.input1X
	arm03_tx_orig.output1D >> stretch_mult.input1Y
	log_debug('mult tx to arm 02/03 stretch done')

	# blend 0-1 with user set CTRL attribute Stretch
	stretch_ctrl = pm.ls('%s_arm_fkIkSwitch'%RL)

	stretch_user_blend = pm.createNode('blendColors', n='%s_armStrUser_blend'%RL)
	arm02_tx_orig.output1D >> stretch_user_blend.color2R
	arm03_tx_orig.output1D >> stretch_user_blend.color2G
	stretch_mult.outputX >> stretch_user_blend.color1R
	stretch_mult.outputY >> stretch_user_blend.color1G
	stretch_user_blend.blender.set(0)
	if len(stretch_ctrl) > 0:
		stretch_ctrl[0].stretchy >> stretch_user_blend.blender
	else:
		logging.info('No fkIkSwitch Ctrl with stretch control found to connect to')


	# now connect that to actual ikJnt TX
	stretch_user_blend.outputR >> jnts['L_arm02']['ikJnt'].tx
	stretch_user_blend.outputG >> jnts['L_arm03']['ikJnt'].tx
	log_debug('connecting done')

### TODO build_skinJnts_arm from template
def build_skinJnts_arm(side='L'):
	'''
	WIP create the joints based on locators. skinjoints
	Args:
	Returns:
    3 rotation orders
    upper: xyz, lower xzy, wrist zyx
	'''
	return 'Building body skinJnts from template'

	# set rotation orders. hand01: zyx
	pm.joint(n='%s_arm01_skinJnt' % side)
	pm.joint(n='%s_arm01_skinJnt' % side)
	pm.joint(n='%s_hand01_skinJnt' % side)
	pm.setAttr("%s_hand01.rotateOrder" % side, 5)


def setup_fk_spaceswitch_arm(jnts, RL='L'):
	''' Create Space Switch for arm01_fkCtrl
	Arm01 - Chest - COG - DIRECTION
	'''

	fkCtrl = jnts['%s_arm01' % RL]['fkCtrl']
	follow_const_grp = pm.createNode('transform', n='%s_FollowCONST'%fkCtrl)
	if len(fkCtrl.listRelatives(parent=1)) == 0:
		return pm.error('No parent of fkCtrl %s found'%fkCtrl)
	fkCtrl_parent = fkCtrl.listRelatives(parent=1)[0]
	pm.parent(follow_const_grp, fkCtrl_parent)
	riggUtils.snap(fkCtrl_parent, follow_const_grp)
	pm.parent(fkCtrl, follow_const_grp)

	space = {}
	# - # Create a Locators for each Space and parent/snap it to its according parent

	# arm
	space['arm'] = pm.spaceLocator(n='%s_parentToArm01Loc' % fkCtrl)

	pm.parent(space['arm'], fkCtrl.attr('AUTO').get())
	riggUtils.snap(fkCtrl, space['arm'])


	# chest
	space['chest'] = pm.spaceLocator(n='%s_parentToChestLoc' % fkCtrl)
	pm.parent(space['chest'], jnts['chest01']['ctrl'])
	riggUtils.snap(fkCtrl, space['chest'])

	# cog
	space['cog'] = pm.spaceLocator(n='%s_parentToCogLoc' % fkCtrl)
	if jnts.has_key('cog'):
		pm.parent(space['cog'], jnts['cog']['ctrl'])
	else: pm.parent(space['cog'], 'C_COG_ctrl')
	riggUtils.snap(fkCtrl, space['cog'])

	# direction
	space['direction'] = pm.spaceLocator(n='%s_parentToDIRECTIONLoc' % fkCtrl)
	pm.parent(space['direction'], 'DIRECTION')
	riggUtils.snap(fkCtrl, space['direction'])

	# - # Add Switch Attribute to CTRL
	space_switch = pm.addAttr(fkCtrl, ln='space', at='enum', en='arm:chest:cog:direction:', k=1)

	# - # Set Driven Key
	const = pm.orientConstraint([space['arm'], space['chest'], space['cog'], space['direction']], follow_const_grp, mo=1)
	weightList = const.getWeightAliasList()



	for i in range(4):
		fkCtrl.attr('space').set(i)
		# turn to 1
		log_debug( 'set weightlist %s to 1 %s' %(weightList[i], weightList[i].get()) )


		# key all the weights
		for j in range(4):
			if i == j:
				weightList[j].set(1)
			else:
				weightList[j].set(0)
			pm.setAttr('%s.r'%follow_const_grp, (0,0,0))
			log_debug( 'setdriven key weightlist %s %s >> space %s'%(weightList[j], weightList[j].get(),'%s.space'%fkCtrl) )
			pm.setDrivenKeyframe(weightList[j], cd='%s.space'%fkCtrl)

	return weightList


def rigHand(handCtrl, thumbJnt, indexJnt, middleJnt, ringJnt, pinkyJnt, pinkyCup, ringCup):
	ret = -1
	# rigs a hand -- returns 1 on success, -1 on failure
	if handCtrl == "" or thumbJnt == "" or indexJnt == "":
		return ret

	settings.setScale()
	i = 0
	aThumb = []
	aIndex = []
	aMiddle = []
	aRing = []
	aPinky = []
	handGrp = ""
	prefix = handCtrl.split('_')[0]
	limbName = (prefix == "L") and "leftHand" or "rightHand"
	makeIk = int(settings.globalPrefs["createIkFingerCtrls"])
	rtReverseCurl = int(settings.globalPrefs["reverseFingerCurl"])
	charName = str(settings.globalPrefs["name"])
	pfx = (prefix == "L") and settings.globalPrefs["leftPrefix"] or settings.globalPrefs["rightPrefix"]
	# create hand rig group (if necessary) -- ik is responsible for the only hand related transforms
	handGrp = str('%s_finger_grp'%prefix)
	# hand group -- all hand rig transforms created from here out will be placed in this group
	if not pm.objExists(handGrp):
		handGrp = pm.group(em=1, name=handGrp)
		utils.snap('%s_hand01_skinJnt'%prefix, handGrp)
		pm.parent(handGrp, utils.rigRootFolder())
	else:
		pm.warning(
			"This part of the character has already been rigged.  You must remove the current rig before you can continue.")
		return ret

	utils.connectToMasterScale(handGrp)
	aAllHandJnts = []
	# used to save all hand Jnts to charVars
	aFingerVarNames = []
	aFingerBaseNames = []
	# save existing fingers in a a couple of arrays so we can add some individual finger atts before fingerRigHelper is called
	if thumbJnt != "":
		aThumb = pm.mel.abRTGetHierarchy(thumbJnt, "", True)
		aAllHandJnts = aAllHandJnts + aThumb
		aFingerVarNames.append("aThumb")
		aFingerBaseNames.append("thumb")

	if indexJnt != "":
		aIndex = pm.mel.abRTGetHierarchy(indexJnt, "", True)
		aAllHandJnts = aAllHandJnts + aIndex
		aFingerVarNames.append("aIndex")
		aFingerBaseNames.append("index")

	if middleJnt != "":
		aMiddle = pm.mel.abRTGetHierarchy(middleJnt, "", True)
		aAllHandJnts = aAllHandJnts + aMiddle
		aFingerVarNames.append("aMiddle")
		aFingerBaseNames.append("middle")

	if ringJnt != "":
		aRing = pm.mel.abRTGetHierarchy(ringJnt, "", True)
		aAllHandJnts = aAllHandJnts + aRing
		aFingerVarNames.append("aRing")
		aFingerBaseNames.append("ring")

	if pinkyJnt != "":
		aPinky = pm.mel.abRTGetHierarchy(pinkyJnt, "", True)
		aAllHandJnts = aAllHandJnts + aPinky
		aFingerVarNames.append("aPinky")
		aFingerBaseNames.append("pinky")

	aAllHandJnts = aAllHandJnts + [pinkyCup, ringCup]
	# finish and clean up $aAllHandJnts
	aAllHandJnts = [x for x in aAllHandJnts if x not in [""]]
	# save to charVars
	utils.saveRigGrpToCharVars(handGrp, limbName)
	utils.saveToCharVars(aAllHandJnts, limbName)
	# want to capture newly added $handCtrl atts, so first must capture list of current custom $handCtrl atts
	aOrigAtts = pm.listAttr(handCtrl, userDefined=1)
	aOtherNewAtts = []
	# used to capture new spread atts on spine control curve
	tAtt = ""
	longPrefix = (prefix == "L") and "left" or "right"
	cupRotStr = "r" + settings.globalPrefs["fingerCupAxis"]
	# rx, ry, or rz (from fingerCupAxis global)
	# header for finger controls
	if not pm.mel.attributeExists("FINGER_SETTINGS___", handCtrl):
		pm.addAttr(handCtrl, ln="FINGER_SETTINGS___", at='bool', keyable=False)

	pm.setAttr((handCtrl + ".FINGER_SETTINGS___"),
			   lock=True, cb=True)
	# add finger control vis atts
	if not pm.mel.attributeExists("fkFingerCtrlVis", handCtrl):
		pm.addAttr(handCtrl, ln="fkFingerCtrlVis", dv=1, at='bool', keyable=True)

	if not pm.mel.attributeExists("fingerMasterCtrlVis", handCtrl):
		pm.addAttr(handCtrl, ln="fingerMasterCtrlVis", dv=1, at='bool', keyable=True)
	# add thumb dampener att (modifies masterFist effect on thumb)

	if not pm.mel.attributeExists("thumbFistDamp", handCtrl):
		pm.addAttr(handCtrl, min=-100, ln="thumbFistDamp", max=100, keyable=True, at='double', dv=.3)
	# add finger curl atts (instead of master fist)

	if not pm.mel.attributeExists("midCurlAmt", handCtrl):
		pm.addAttr(handCtrl, min=-100, ln="midCurlAmt", max=100, keyable=True, at='double', dv=1)

	if not pm.mel.attributeExists("tipCurlAmt", handCtrl):
		pm.addAttr(handCtrl, min=-100, ln="tipCurlAmt", max=100, keyable=True, at='double', dv=1.4)
	# add finger spread and roll inherit atts

	if not pm.mel.attributeExists("midSpreadInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="midSpreadInherit", max=1, keyable=True, at='double', dv=0)

	if not pm.mel.attributeExists("tipSpreadInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="tipSpreadInherit", max=1, keyable=True, at='double', dv=0)

	if not pm.mel.attributeExists("midRollInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="midRollInherit", max=1, keyable=True, at='double', dv=0)

	if not pm.mel.attributeExists("tipRollInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="tipRollInherit", max=1, keyable=True, at='double', dv=0)

	if not pm.mel.attributeExists("baseStretchInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="baseStretchInherit", max=1, keyable=True, at='double', dv=1)

	if not pm.mel.attributeExists("midStretchInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="midStretchInherit", max=1, keyable=True, at='double', dv=1)

	if not pm.mel.attributeExists("tipStretchInherit", handCtrl):
		pm.addAttr(handCtrl, min=0, ln="tipStretchInherit", max=1, keyable=True, at='double', dv=1)
	# add IK and stretch attributes

	aFingerStretchAtts = []
	aHandStretchAtts = []
	aFingerIKSwitches = []
	aFingerStretchAttNames = []
	aHandStretchAttNames = []
	aFingerIKSwitchNames = []
	# create arrays of IK and stretch att names
	for i in range(0, len(aFingerBaseNames)):
		aFingerStretchAttNames[i] = aFingerBaseNames[i] + "Stretch"
		aHandStretchAttNames[i] = aFingerBaseNames[i] + "HandStretch"
		if makeIk:
			aFingerIKSwitchNames[i] = aFingerBaseNames[i] + "IK"

	if makeIk:
		if not pm.mel.attributeExists("________FINGER_IK_____", handCtrl):
			pm.addAttr(handCtrl, ln="________FINGER_IK_____", at='bool', keyable=False)
		# IK
		# IK switches

		pm.setAttr((handCtrl + ".________FINGER_IK_____"),
				   lock=True, cb=True)
		if not pm.mel.attributeExists("stretchyIkFingers", handCtrl):
			pm.addAttr(handCtrl, min=0, ln="stretchyIkFingers", max=1, keyable=True, at='double', dv=0)

		if not pm.mel.attributeExists("maxIkFingerStretch", handCtrl):
			pm.addAttr(handCtrl, min=1, ln="maxIkFingerStretch", max=10, keyable=True, at='double', dv=2)

		for i in range(0, len(aFingerIKSwitchNames)):
			if not pm.mel.attributeExists(aFingerIKSwitchNames[i], handCtrl):
				pm.addAttr(handCtrl, min=0, ln=aFingerIKSwitchNames[i], max=1, keyable=True, at='double', dv=0)

			aFingerIKSwitches[i] = (handCtrl + "." + aFingerIKSwitchNames[i])

	if not pm.mel.attributeExists("___FINGER_STRETCH_______", handCtrl):
		pm.addAttr(handCtrl, ln="___FINGER_STRETCH_______", at='bool', keyable=False)
	# Stretch

	pm.setAttr((handCtrl + ".___FINGER_STRETCH_______"),
			   lock=True, cb=True)
	if not pm.mel.attributeExists("masterFingerStretch", handCtrl):
		pm.addAttr(handCtrl, min=-1, ln="masterFingerStretch", max=5, keyable=True, at='double', dv=0)
	# finger stretch

	for i in range(0, len(aFingerStretchAttNames)):
		if not pm.mel.attributeExists(aFingerStretchAttNames[i], handCtrl):
			pm.addAttr(handCtrl, min=-1, ln=aFingerStretchAttNames[i], max=5, keyable=True, at='double', dv=0)

		aFingerStretchAtts[i] = (handCtrl + "." + aFingerStretchAttNames[i])

	if not pm.mel.attributeExists("masterHandStretch", handCtrl):
		pm.addAttr(handCtrl, min=-1, ln="masterHandStretch", max=5, keyable=True, at='double', dv=0)
	# hand stretch

	for i in range(0, len(aHandStretchAttNames)):
		if not pm.mel.attributeExists(aHandStretchAttNames[i], handCtrl):
			pm.addAttr(handCtrl, min=-1, ln=aHandStretchAttNames[i], max=5, keyable=True, at='double', dv=0)

		aHandStretchAtts[i] = (handCtrl + "." + aHandStretchAttNames[i])

	if not pm.mel.attributeExists("_MASTER_FINGER_ATTS___", handCtrl):
		pm.addAttr(handCtrl, ln="_MASTER_FINGER_ATTS___", at='bool', keyable=False)
	# add master hand atts

	pm.setAttr((handCtrl + "._MASTER_FINGER_ATTS___"),
			   lock=True, cb=True)
	if not pm.mel.attributeExists("masterFist", handCtrl):
		pm.addAttr(handCtrl, min=-100, ln="masterFist", max=100, keyable=True, at='double', dv=0)

	if not pm.mel.attributeExists("masterSpread", handCtrl):
		pm.addAttr(handCtrl, min=-100, ln="masterSpread", max=100, keyable=True, at='double', dv=0)
	# master cup

	if pm.objExists(pinkyCup):
		if not pm.mel.attributeExists("masterCup", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="masterCup", max=100, keyable=True, at='double', dv=0)
	# done
	mstrSpreadAtt = (handCtrl + ".masterSpread")
	mstrFingerStretchAtt = (handCtrl + ".masterFingerStretch")
	mstrHandStretchAtt = (handCtrl + ".masterHandStretch")
	baseStretchInherit = (handCtrl + ".baseStretchInherit")
	midStretchInherit = (handCtrl + ".midStretchInherit")
	tipStretchInherit = (handCtrl + ".tipStretchInherit")
	stretchyIkFingers = (handCtrl + ".stretchyIkFingers")
	maxIkFingerStretch = (handCtrl + ".maxIkFingerStretch")
	mstrFistAtt = (handCtrl + ".masterFist")
	thumbCurlDampAtt = (handCtrl + ".thumbFistDamp")
	midCurlAmtAtt = (handCtrl + ".midCurlAmt")
	tipCurlAmtAtt = (handCtrl + ".tipCurlAmt")
	midSpreadInheritAtt = (handCtrl + ".midSpreadInherit")
	tipSpreadInheritAtt = (handCtrl + ".tipSpreadInherit")
	midRollInheritAtt = (handCtrl + ".midRollInherit")
	tipRollInheritAtt = (handCtrl + ".tipRollInherit")
	if not pm.mel.attributeExists("_FINGER_CURL___", handCtrl):
		pm.addAttr(handCtrl, ln="_FINGER_CURL___", at='bool', keyable=False)

	pm.setAttr((handCtrl + "._FINGER_CURL___"),
			   lock=True, cb=True)
	# set up finger curl
	if len(aThumb) > 0:
		if not pm.mel.attributeExists("thumbCurl", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="thumbCurl", max=100, keyable=True, at='double', dv=0)

		thumbCurlAtt = (handCtrl + ".thumbCurl")

	if len(aIndex) > 0:
		if not pm.mel.attributeExists("indexCurl", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="indexCurl", max=100, keyable=True, at='double', dv=0)

		indexCurlAtt = (handCtrl + ".indexCurl")

	if len(aMiddle) > 0:
		if not pm.mel.attributeExists("middleCurl", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="middleCurl", max=100, keyable=True, at='double', dv=0)

		middleCurlAtt = (handCtrl + ".middleCurl")

	if len(aRing) > 0:
		if not pm.mel.attributeExists("ringCurl", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="ringCurl", max=100, keyable=True, at='double', dv=0)

		ringCurlAtt = (handCtrl + ".ringCurl")

	if len(aPinky) > 0:
		if not pm.mel.attributeExists("pinkyCurl", handCtrl):
			pm.addAttr(handCtrl, min=-100, ln="pinkyCurl", max=100, keyable=True, at='double', dv=0)

		pinkyCurlAtt = (handCtrl + ".pinkyCurl")

	if pm.objExists(pinkyCup) or pm.objExists(ringCup):
		if not pm.mel.attributeExists("_FINGER_CUP____", handCtrl):
			pm.addAttr(handCtrl, ln="_FINGER_CUP____", at='bool', keyable=False)
		# add individual cup attributes

		pm.setAttr((handCtrl + "._FINGER_CUP____"),
				   lock=True, cb=True)
		if pm.objExists(ringCup):
			if not pm.mel.attributeExists("ringCup", handCtrl):
				pm.addAttr(handCtrl, min=-100, ln="ringCup", max=100, keyable=True, at='double', dv=0)

		if pm.objExists(pinkyCup):
			if not pm.mel.attributeExists("pinkyCup", handCtrl):
				pm.addAttr(handCtrl, min=-100, ln="pinkyCup", max=100, keyable=True, at='double', dv=0)

	aSpreadAmts = [1.0, .5, 0.0, -.5, -1.0]
	# add masterSpread individual finger amounts to rigSettingsCtrl
	# array to hold spread amounts by finger index (starting with the thumb)
	rigSettingsCtrl = str(pm.mel.abRTGetFromUI("rigSettingsCtrl"))
	aSpreadAmtAtts = []
	# contains attributes ("transform.att") for fingers spread amounts (starting with the thumb)
	if rigSettingsCtrl != "":
		totNumFingers = 0
		# count fingers
		if thumbJnt != "":
			totNumFingers += 1

		if indexJnt != "":
			totNumFingers += 1

		if middleJnt != "":
			totNumFingers += 1

		if ringJnt != "":
			totNumFingers += 1

		if pinkyJnt != "":
			totNumFingers += 1

		spreadDelta = float(2 / float(totNumFingers - 1))
		cSpread = float(1)
		# add attributes
		# string $attLabel = ($prefix == "L") ? "________LF_SPREAD___" : "________RT_SPREAD___";
		attLabel = (prefix == "L") and "_LF_MASTER_SPREAD___" or "_RT_MASTER_SPREAD___"

		if not pm.mel.attributeExists(attLabel, rigSettingsCtrl):
			pm.addAttr(rigSettingsCtrl, ln=attLabel, dv=0, at='bool', keyable=True)
			pm.setAttr((rigSettingsCtrl + "." + attLabel),
					   lock=True)
			# record atts to charVars
			aOtherNewAtts.append((rigSettingsCtrl + "." + attLabel))

		if thumbJnt != "":
			aSpreadAmts[0] = cSpread
			cSpread -= spreadDelta
			tAtt = longPrefix + "ThumbAmt"
			if not pm.mel.attributeExists(tAtt, rigSettingsCtrl):
				pm.addAttr(rigSettingsCtrl, min=-100, ln=tAtt, max=100, keyable=True, at='double', dv=aSpreadAmts[0])

			aSpreadAmtAtts[0] = (rigSettingsCtrl + "." + tAtt)
			aOtherNewAtts.append(aSpreadAmtAtts[0])

		if indexJnt != "":
			aSpreadAmts[1] = cSpread
			cSpread -= spreadDelta
			tAtt = longPrefix + "IndexAmt"
			if not pm.mel.attributeExists(tAtt, rigSettingsCtrl):
				pm.addAttr(rigSettingsCtrl, min=-100, ln=tAtt, max=100, keyable=True, at='double', dv=aSpreadAmts[1])

			aSpreadAmtAtts[1] = (rigSettingsCtrl + "." + tAtt)
			aOtherNewAtts.append(aSpreadAmtAtts[1])

		if middleJnt != "":
			aSpreadAmts[2] = cSpread
			cSpread -= spreadDelta
			tAtt = longPrefix + "MiddleAmt"
			if not pm.mel.attributeExists(tAtt, rigSettingsCtrl):
				pm.addAttr(rigSettingsCtrl, min=-100, ln=tAtt, max=100, keyable=True, at='double', dv=aSpreadAmts[2])

			aSpreadAmtAtts[2] = (rigSettingsCtrl + "." + tAtt)
			aOtherNewAtts.append(aSpreadAmtAtts[2])

		if ringJnt != "":
			aSpreadAmts[3] = cSpread
			cSpread -= spreadDelta
			tAtt = longPrefix + "RingAmt"
			if not pm.mel.attributeExists(tAtt, rigSettingsCtrl):
				pm.addAttr(rigSettingsCtrl, min=-100, ln=tAtt, max=100, keyable=True, at='double', dv=aSpreadAmts[3])

			aSpreadAmtAtts[3] = (rigSettingsCtrl + "." + tAtt)
			aOtherNewAtts.append(aSpreadAmtAtts[3])

		if pinkyJnt != "":
			aSpreadAmts[4] = cSpread
			cSpread -= spreadDelta
			tAtt = longPrefix + "PinkyAmt"
			if not pm.mel.attributeExists(tAtt, rigSettingsCtrl):
				pm.addAttr(rigSettingsCtrl, min=-100, ln=tAtt, max=100, keyable=True, at='double', dv=aSpreadAmts[4])

			aSpreadAmtAtts[4] = (rigSettingsCtrl + "." + tAtt)
			aOtherNewAtts.append(aSpreadAmtAtts[4])

	thumbCSRAxes = settings.globalPrefs["thumbCurlSpreadRoll"]
	fingerCSRAxes = settings.globalPrefs["fingerCurlSpreadRoll"]

	# rig fingers
	aTempFinger = []
	tFingerAxes = ""
	tThumbDampAtt = ""
	tFingerLabel = ""
	curlAtt = ""
	aFingerStretchIKAtts = []
	for i in range(0, len(aFingerVarNames)):
		aTempFinger = []
		if aFingerVarNames[i] == "aThumb":
			aTempFinger = aThumb

			curlAtt = thumbCurlAtt


		elif aFingerVarNames[i] == "aIndex":
			aTempFinger = aIndex

			curlAtt = indexCurlAtt


		elif aFingerVarNames[i] == "aMiddle":
			aTempFinger = aMiddle

			curlAtt = middleCurlAtt


		elif aFingerVarNames[i] == "aRing":
			aTempFinger = aRing

			curlAtt = ringCurlAtt


		elif aFingerVarNames[i] == "aPinky":
			aTempFinger = aPinky

			curlAtt = pinkyCurlAtt

		if len(aTempFinger) > 0:
			tFingerAxes = (aFingerBaseNames[i] == "thumb")
			tFingerAxes and thumbCSRAxes or fingerCSRAxes
			tThumbDampAtt = (aFingerBaseNames[i] == "thumb")
			tThumbDampAtt and thumbCurlDampAtt or ""
			tFingerLabel = ("________" + (aFingerBaseNames[i].upper()) + "___")
			# stretchy and IK finger atts
			aFingerStretchIKAtts = []
			aFingerStretchIKAtts[0] = mstrFingerStretchAtt
			# master finger stretch obj.att
			aFingerStretchIKAtts[1] = mstrHandStretchAtt
			# master hand stretch obj.att
			aFingerStretchIKAtts[2] = aFingerStretchAtts[i]
			# individual finger stretch obj.att
			aFingerStretchIKAtts[3] = aHandStretchAtts[i]
			# individual hand stretch obj.att
			aFingerStretchIKAtts[4] = baseStretchInherit
			# finger base stretch inherit obj.att
			aFingerStretchIKAtts[5] = midStretchInherit
			# finger mid stretch inherit obj.att
			aFingerStretchIKAtts[6] = tipStretchInherit
			# finger tip stretch inherit obj.att
			if makeIk:
				aFingerStretchIKAtts[7] = aFingerIKSwitches[i]
				# FK/IK finger switch
				aFingerStretchIKAtts[8] = stretchyIkFingers
				# main stretch switch obj.att for all fingers
				aFingerStretchIKAtts[9] = maxIkFingerStretch
			# max number of lengths that fingers will stretch obj.att

			pm.mel.abRTFingerRigHelper(aTempFinger, tFingerLabel, aFingerBaseNames[i], handCtrl, tFingerAxes,
									   mstrSpreadAtt, mstrFistAtt, aSpreadAmtAtts[i], curlAtt, midCurlAmtAtt,
									   tipCurlAmtAtt, tThumbDampAtt, midSpreadInheritAtt, tipSpreadInheritAtt,
									   midRollInheritAtt, tipRollInheritAtt, aFingerStretchIKAtts, prefix, handGrp,
									   limbName)

	pm.select(clear=1)
	# now back to add and connect cup attributes, if any
	if pm.objExists(ringCup) or pm.objExists(pinkyCup):
		masterCupMltDiv = ""
		# master cup
		aXyz = ["x", "y", "z"]
		ringBaseFkCtrl = charName + "_" + pfx + "ringBase_fk_ctrl"
		pinkyBaseFkCtrl = charName + "_" + pfx + "pinkyBase_fk_ctrl"
		aCupJnts = [ringCup, pinkyCup]
		aFkCtrlToAddCupAttsLU = [ringBaseFkCtrl, pinkyBaseFkCtrl]
		aFkCtrlAttNameLU = ["ringCup", "pinkyCup"]
		pinkyRingCupPlsMns = str(utils.createNode("plusMinusAverage", "pinkyRingCup", prefix, limbName))
		ringCupMltDiv = str(utils.createNode("multiplyDivide", "pinkyRingCup", prefix, limbName))
		if not rtReverseCurl or rtReverseCurl and prefix == "L":
			pm.setAttr((ringCupMltDiv + ".input1X"),
					   1)
			pm.setAttr((ringCupMltDiv + ".input1Y"),
					   1)
			if pm.objExists(ringCup):
				masterCupMltDiv = str(utils.createNode("multiplyDivide", "masterCup", prefix, limbName))
				pm.setAttr((masterCupMltDiv + ".input1X"),
						   .5)
				pm.setAttr((masterCupMltDiv + ".input1Y"),
						   1)
		else:
			pm.setAttr((ringCupMltDiv + ".input1X"),
					   -1)
			pm.setAttr((ringCupMltDiv + ".input1Y"),
					   -1)

		# add all of the cup inputs first
		for i in range(0, len(aCupJnts)):
			if not pm.objExists(aCupJnts[i]):
				continue
			# add masterCup

			if pm.objExists(masterCupMltDiv):
				pm.connectAttr((handCtrl + ".masterCup"), (masterCupMltDiv + ".input2" + aXyz[i].upper()))
				pm.connectAttr((masterCupMltDiv + ".output" + aXyz[i].upper()),
							   (pinkyRingCupPlsMns + ".input2D[0].input2D" + aXyz[i]))


			else:
				pm.connectAttr((handCtrl + ".masterCup"), (pinkyRingCupPlsMns + ".input2D[0].input2D" + aXyz[i]))

			if pm.mel.attributeExists(aFkCtrlAttNameLU[i], handCtrl):
				pm.connectAttr((handCtrl + "." + aFkCtrlAttNameLU[i]),
							   (pinkyRingCupPlsMns + ".input2D[1].input2D" + aXyz[i]))
			# add specific cup att
			# add cup control to relevant FK base finger ctrl

			if pm.objExists(aFkCtrlToAddCupAttsLU[i]):
				if not pm.mel.attributeExists(aFkCtrlAttNameLU[i], aFkCtrlToAddCupAttsLU[i]):
					pm.addAttr(aFkCtrlToAddCupAttsLU[i], min=-100, ln=aFkCtrlAttNameLU[i], max=100, keyable=True,
							   at='double', dv=0)

				pm.connectAttr((aFkCtrlToAddCupAttsLU[i] + "." + aFkCtrlAttNameLU[i]),
							   (pinkyRingCupPlsMns + ".input2D[2].input2D" + aXyz[i]))

			pm.connectAttr((pinkyRingCupPlsMns + ".output2D.output2D" + aXyz[i]),
						   (ringCupMltDiv + ".input2" + aXyz[i].upper()))
			pm.connectAttr((ringCupMltDiv + ".input2" + aXyz[i].upper()), (aCupJnts[i] + "." + cupRotStr))

	aNewAtts = pm.listAttr(handCtrl, userDefined=1)
	# compare orig with current handCtrl atts to get an array of newly added atts
	aNewAtts = [x for x in aNewAtts if x not in aOrigAtts]
	# add handCtrl to atts ("handCtrl.att")
	for i in range(0, len(aNewAtts)):
		aNewAtts[i] = handCtrl + "." + aNewAtts[i]
	# add new other atts to new atts

	aNewAtts = aNewAtts + aOtherNewAtts
	# save new atts to charVars
	utils.saveToCharVars(aNewAtts, limbName)
	# save some stuff to skeleton
	utils.setRootJntAtt("createIkFingerCtrls", str(makeIk))
	utils.setRootJntAtt("reverseFingerCurl", str(rtReverseCurl))
	utils.setRootJntAtt("fingerCurlSpreadRoll", fingerCSRAxes)
	utils.setRootJntAtt("thumbCurlSpreadRoll", thumbCSRAxes)

	ret = 1
	return ret



