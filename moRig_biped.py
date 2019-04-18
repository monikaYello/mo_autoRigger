import pymel.core as pm
# sys.path.append('D:\Google Drive\PythonScripting\my_autoRigger')
import mo_Utils.mo_curveLib as curveLib
import mo_Utils.mo_riggUtils as riggUtils

import logging

logging.basicConfig(level=logging.INFO)
lg = logging.getLogger(__name__)
from mo_Utils.mo_logging import *
reload(curveLib)
reload(riggUtils)
'''
import sys
sys.path.append('D:\Google Drive\PythonScripting\mo_autoRigger')
sys.path.append('D:\Google Drive\PythonScripting\scripts')

# Build template and skinJnts with UI
import moRig_UI as moRig_UI
reload(moRig_UI)
moRig_UI.skeletonMakerUI()


# Build tempate script
import moRig_skeletonTemplate as skelTemp
import moRig_settings as settings
settings.initGlobals()
skelTemp.makeProxySkeleton()

# Build skinJnts from template
skelTemp.skeletonizeProxy()

## or temporary work with autoRigger_lumaHuman.003

# Build ctrlJnts form skinJnts
import moRig_biped as biped
import moRig_spine as spine
import moRig_arm as arm
import moRig_leg as leg
reload(biped)
reload(arm)
reload(leg)

biped.build_ctrlJnts_body()
arm.build_ctrlJnts_arm()
leg.build_ctrlJnts_leg()

# dictionary
jntsDic={}
biped.define_ctrlJnts(jntsDic)

# ikfk jntsDic
arm.build_jnts_arm(jntsDic, mode=['ik', 'fk'])
leg.build_jnts_leg(jntsDic, mode=['ik', 'fk'])

biped.define_fkJnts(jntsDic)
biped.define_ikJnts(jntsDic)

# ctrls
scale = 1
biped.createWorld(scale=scale)
arm.create_ctrl_fk_arm(jntsDic, scale=scale)
arm.create_ctrl_ik_arm(jntsDic, scale=scale)


reload(leg)
leg.create_ctrl_fk_leg(jntsDic, scale=scale)
leg.create_ctrl_ik_leg(jntsDic, scale=scale)

biped.define_fkCtrls(jntsDic)

# ikfk with switch
arm.setup_fk_arm(jntsDic, RL='L')
arm.setup_ik_arm(jntsDic, RL='L')
arm.setup_ikfkSwitch_arm(jntsDic)

# spine
biped.create_ctrl_spine(jntsDic, spine_count=3, scale=scale*2)
spine.setup_spine(jntsDic)

# space switch
arm.setup_fk_spaceswitch_arm(jntsDic)
'''

def test():
	foo = "this is var to test"
	testnumber = 12
	print testnumber
	print foo
	return foo

def define_color(side):
	# define side
	if side == 'L':
		return 'blue'
	elif side == 'R':
		return 'red'
	else:
		return 'yellow'


def define_ctrlJnts(jntsDic={}):
	ctrljnts = {}
	try:
		ctrljnts['root'] = pm.PyNode('root_ctrlJnt')
	except:
		ctrljnts['root'] = ''
	# Center
	for limb in ['spine', 'chest', 'neck', 'head', 'pelvis']:
		existingJnts = pm.ls('C_%s*_ctrlJnt' % limb) + pm.ls('C_%s*_ctrlJntEnd' % limb)  # * at end with or without JntEnd
		for j in existingJnts:
			ctrljnts['%s%s' % (limb, j.split(limb)[-1].split('_ctrlJnt')[0])] = {'ctrlJnt': j}
	
	merge_nested_dic(jntsDic, ctrljnts)
	
	# R/L limbs
	for limb in ['clavicle', 'arm', 'hand', 'eye', 'leg', 'foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_ctrlJnt' % (side, limb)) + pm.ls(
				'%s_%s*_ctrlJntEnd' % (side, limb))  # * at end with or without JntEnd
			for j in existingJnts:
				ctrljnts['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_ctrlJnt')[0])] = {'ctrlJnt': j}
	print ctrljnts
	return merge_nested_dic(jntsDic, ctrljnts)




def define_fkJnts(jntsDic={}):
	'''
	Define fk jntsDic based on searching for '_fkJnt' in scene and merge them into existing Jnts Dictionary
	Args:
	    jntsDic: existing Jnts Dictionary containing skinJns, ctrlJnts etc.

	Returns: Jnts Dictionary with found  fkJnts added
	'''
	fkjnts = {}
	# Center
	side = 'C'
	for limb in ['spine', 'chest', 'neck', 'head', 'pelvis']:
		existingJnts  = pm.ls('%s_%s*_fkJnt' % (side,limb))
		for j in existingJnts:
			print 'j is %s'%j 
			fkjnts['%s%s' % (limb, j.split(limb)[-1].split('_fkJnt')[0])] = {'fkJnt': j}
	
	merge_nested_dic(jntsDic, fkjnts)
	
	# R/L limbs
	for limb in ['clavicle', 'arm', 'hand', 'leg', 'foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_fkJnt' % (side, limb)) + pm.ls(
				'%s_%s*_fkJntEnd' % (side, limb))  # * at end with or without JntEnd
			for j in existingJnts:
				
				fkjnts['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_fkJnt')[0])] = {'fkJnt': j}	
	if len(fkjnts) == 0:
		lg.info('No *_fkJnt found.')
	print 'fkJnts is %s'%fkjnts
	return merge_nested_dic(jntsDic, fkjnts)


def define_fkCtrls(jntsDic={}):
	'''
	Define fk Ctrl based on searching for '_fkCtrl' in scene and merge them into existing Jnts Dictionary
	Args:
	    jntsDic: existing Jnts Dictionary containing skinJns, ctrlJnts etc.

	Returns: Jnts Dictionary with found  fk Ctrls added
	'''
	fkCtrls = {}
	for limb in ['clavicle', 'arm', 'hand', 'leg', 'foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_fkCtrl' % (side, limb))
			for j in existingJnts:
				fkCtrls['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_fkCtrl')[0])] = {'fkCtrl': j}

	merge_nested_dic(jntsDic, fkCtrls)

	# Center
	fkCtrls = {}
	side = 'C'
	for limb in ['spine', 'chest', 'neck', 'head', 'pelvis']:
		existingJnts  = pm.ls('%s_%s*_fkCtrl' % (side, limb))
		for j in existingJnts:
			fkCtrls['%s%s' % (limb, j.split(limb)[-1].split('_fkCtrl')[0])] = {'fkCtrl': j}
	
	if len(fkCtrls) == 0:
		lg.info('No *_fkCtrl found.')
	
	return merge_nested_dic(jntsDic, fkCtrls)

def define_ikCtrls(jntsDic={}):
	'''
	Define fk Ctrl based on searching for '_ikCtrl' in scene and merge them into existing Jnts Dictionary
	Args:
	    jntsDic: existing Jnts Dictionary containing skinJns, ctrlJnts etc.

	Returns: Jnts Dictionary with found  fk Ctrls added
	'''
	ikCtrls = {}
	for limb in ['clavicle', 'hand','foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_ikCtrl' % (side, limb)) 
			print existingJnts
			for j in existingJnts:
				ikCtrls['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_ikCtrl')[0])] = {'ikCtrl': j}
				print 'R is %s' % ikCtrls
	
	merge_nested_dic(jntsDic, ikCtrls)

	for limb in ['clavicle', 'hand','foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_pvecCtrl' % (side, limb))
			for j in existingJnts:
				ikCtrls['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_pvecCtrl')[0])] = {'pvecCtrl': j}
				print 'R clav is %s' % ikCtrls
	
	merge_nested_dic(jntsDic, ikCtrls)
	
	# Center
	side = 'C'
	for limb in ['spine']:
		existingJnts  = pm.ls('%s_%s*_ikCtrl' % (side, limb))
		for j in existingJnts:
			ikCtrls['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_ikCtrl')[0])] = {'ikCtrl': j}
			print 'C is %s' % ikCtrls
	
	if len(ikCtrls) == 0:
		lg.info('No *_ikCtrls found.')
	
	return merge_nested_dic(jntsDic, ikCtrls)



def define_ikJnts(jntsDic={}):
	'''
	Define ik jntsDic based on searching for '_ikJnt' in scene and merge them into existing Jnts Dictionary
	Args:
	    jntsDic: existing Jnts Dictionary containing skinJns, ctrlJnts etc.

	Returns: Jnts Dictionary with found fkJnts added
	'''
	ikjnts = {}
	for limb in ['clavicle', 'arm', 'hand', 'leg', 'foot']:
		for side in ['R', 'L']:
			existingJnts = pm.ls('%s_%s*_ikJnt' % (side, limb)) + pm.ls(
				'%s_%s*_ikJntEnd' % (side, limb))  # * at end with or without JntEnd
			for j in existingJnts:
				ikjnts['%s_%s%s' % (side, limb, j.split(limb)[-1].split('_ikJnt')[0])] = {'ikJnt': j}

	if len(ikjnts) == 0:
		lg.info('No *_ikJnt found.')

	return merge_nested_dic(jntsDic, ikjnts)

def define_jnts(jntsDic={}):

	define_ctrlJnts(jntsDic=jntsDic)
	define_fkJnts(jntsDic=jntsDic)
	define_ikJnts(jntsDic=jntsDic)	
	
	return jntsDic

def define_ctrls(jntsDic={}):
	
	define_fkCtrls(jntsDic=jntsDic)
	define_ikCtrls(jntsDic=jntsDic)	
	
	return jntsDic


def merge_nested_dic(d1, d2):
	'''
	Merge two nested dictionaries. Dictionaries containing Dictionaries
	Returns: merged Dictionary
	'''
	for k in d2:
		if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
			merge_nested_dic(d1[k], d2[k])
		else:
			d1[k] = d2[k]


def createWorld(name='human', scale=1):
	'''
	Create World node for character with standardized Rigg Groups and export Sets
	Creates Placer, Mover, Direction Ctrls
	Args:
	    name: Name of world
	Returns:

	'''
	if pm.objExists('%s_world' % name):
		lg.info('createWorld: Deleting existing %s_world' % name)
		pm.delete('%s_world' % name)
	world = pm.createNode('transform', n='%s_world' % name)
	pm.createNode('transform', n='CONTROLS'), pm.createNode('transform', n='RIG'), pm.createNode('transform', n='GEO')
	pm.parent(['CONTROLS', 'RIG', 'GEO'], world)
	pm.createNode('transform', n='CONTSTRAINER')
	pm.parent('CONTSTRAINER', 'CONTROLS')
	pm.createNode('transform', n='render_Geo'), pm.createNode('transform', n='nonRender_Geo')
	pm.parent(['render_Geo', 'nonRender_Geo'], 'GEO')
	pm.createNode('transform', n='RIG_NONSCALE')
	pm.parent('RIG_NONSCALE', 'RIG')
	rigscale = pm.createNode('transform', n='RIG_SCALE')
	pm.parent('RIG_SCALE', 'RIG')

	print 'placer'
	placer = curveLib.createShapeCtrl(type='PLACER', name='PLACER', scale=scale)
	print 'mover'
	mover = curveLib.createShapeCtrl(type='MOVER', name='MOVER', scale=scale, color='blue')
	print 'direction'
	direction = curveLib.createShapeCtrl(type='DIRECTION', name='DIRECTION', scale=scale, color='red')
	
	# size attribute
	pm.addAttr(direction, ln='size', at='double', dv=1, k=1)
	direction.size >> direction.scaleX
	direction.size >> direction.scaleY
	direction.size >> direction.scaleZ
	direction.size >> rigscale.scaleX
	direction.size >> rigscale.scaleY
	direction.size >> rigscale.scaleZ

	pm.parent(direction, mover)
	pm.parent(mover, placer)
	pm.parent(placer, 'CONTSTRAINER')

	# DISPLAY
	curveLib.createTextCtrl('D', 'DISPLAY', font="Arial", size=scale)
	riggUtils.grpCtrl(ctrl='DISPLAY')
	pm.parent('DISPLAY_ZERO', placer)
	riggUtils.makeExportable([placer, mover, direction, 'DISPLAY'])





### TODO build skinJnts form template
def build_skinJnts_body():
	return 'Building body skinJnts from template'


def build_ctrlJnts_body(jntsDic={}):
	# delete existing
	pm.delete(pm.ls(['Skeleton_grp', 'C_body_jntGrp']))

	pm.createNode('transform', name='Skeleton_grp')
	pm.createNode('transform', name='C_body_jntGrp', p='Skeleton_grp')

	for bodyLimb in ['C_head', 'C_neck', 'C_spine']:
		pm.createNode('transform', name='%s_jntGrp' % bodyLimb, p='C_body_jntGrp')

	# spine
	########################
	jntsDic['spine01'] = {'ctrlJnt': pm.duplicate('C_spine01_skinJnt', n='C_spine01_ctrlJnt')[0]}
	pm.select(jntsDic['spine01']['ctrlJnt'])
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")

	pm.parent(jntsDic['spine01']['ctrlJnt'], 'C_spine_jntGrp')
	riggUtils.grpCtrl(jntsDic['spine01']['ctrlJnt'])

	# number of spine jntsDic for naming endjoint
	spine_jnt_amount = len(pm.ls('C_spine*_ctrlJnt'))

	# deal with children, make endJnt or delete
	i=2
	for childJnt in pm.listRelatives(jntsDic['spine01']['ctrlJnt'], children=1, type='joint', ad=1):
		if 'spine' in childJnt.name():  # spine02, 03 ...
			continue
		elif childJnt == 'C_chest01_ctrlJnt':  # end joint
			log_debug( 'endjoint. %s' % childJnt)
			pm.rename(childJnt, 'C_spine%02d_ctrlJntEnd' % (spine_jnt_amount + 1))  # create end joint from head
		else:
			pm.delete(childJnt)
		i += 1

	# chest
	########################
	jntsDic['chest01'] = {'ctrlJnt': pm.duplicate('C_chest01_skinJnt', n='C_chest01_ctrlJnt')[0]}
	pm.select(jntsDic['chest01']['ctrlJnt'])
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")

	pm.parent(jntsDic['chest01']['ctrlJnt'], 'C_spine_jntGrp')
	riggUtils.grpCtrl(jntsDic['chest01']['ctrlJnt'])

	# deal with children, make endJnt or delete
	i = 2
	for childJnt in pm.listRelatives(jntsDic['chest01']['ctrlJnt'], children=1, type='joint', ad=1):
		#print 'childJnt chest %s' % childJnt
		if childJnt == 'C_neck01_ctrlJnt':
			pm.rename(childJnt, 'C_chest02_endJnt')
		else:
			pm.delete(childJnt)

	# neck
	########################
	jntsDic['neck01'] = {'ctrlJnt': pm.duplicate('C_neck01_skinJnt', n='C_neck01_ctrlJnt')}
	pm.select(jntsDic['neck01']['ctrlJnt'])  # rename
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")
	# parent n grp
	pm.parent(jntsDic['neck01']['ctrlJnt'], 'C_neck_jntGrp')
	riggUtils.grpCtrl(jntsDic['neck01']['ctrlJnt'])
	# deal with children, make endJnt or delete
	for childJnt in pm.listRelatives(jntsDic['neck01']['ctrlJnt'], children=1, type='joint', ad=1):
		#print 'childJnt neck %s' % childJnt
		if childJnt == 'C_head01_ctrlJnt':
			pm.rename(childJnt, 'C_neck02_ctrlJntEnd')  # create end joint from head
			jntsDic['neck02'] = childJnt
		else:
			pm.delete(childJnt)

	# head
	########################
	jntsDic['head01'] = {'ctrlJnt': pm.duplicate('C_head01_skinJnt', n='C_head01_ctrlJnt')}
	pm.select(jntsDic['head01']['ctrlJnt'])  # rename
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")
	# parent n grp
	pm.parent(jntsDic['head01']['ctrlJnt'], 'C_head_jntGrp')
	riggUtils.grpCtrl(jntsDic['head01']['ctrlJnt'])
	# deal with children, make endJnt or delete
	i=2
	for childJnt in pm.listRelatives(jntsDic['head01']['ctrlJnt'], children=1, type='joint', ad=1):
		#print 'childJnt head is %s' % childJnt
		if childJnt.split('_')[-1] == 'ctrlJnt':
			jntsDic['head%02d'%i] = childJnt
			riggUtils.grpCtrl(childJnt)
			i += 1
	# pelvis
	########################
	jntsDic['pelvis01'] = {'ctrlJnt': pm.duplicate('C_pelvis01_skinJnt', n='C_pelvis01_ctrlJnt')[0]}
	pm.select(jntsDic['pelvis01']['ctrlJnt'])
	pm.mel.searchReplaceNames("_skinJnt", "_ctrlJnt", "hierarchy")
	# parent n grp
	pm.parent(jntsDic['pelvis01']['ctrlJnt'], 'C_spine_jntGrp')
	riggUtils.grpCtrl(jntsDic['pelvis01']['ctrlJnt'])
	# delete legs, children of pelvis endJoint
	pm.delete(jntsDic['pelvis01']['ctrlJnt'].listRelatives(children=1)[0].listRelatives(children=1))
	lg.info('Done build_ctrlJnts_body')
	return jntsDic

def deleteExisting(node):
	if pm.objExists(node):
		pm.delete(node)
		return True
	else:
		return False

''''
# below Mocappy suggested joint orient and rotation order
#TODO update to meet my rig naming

def orientJoint():
	# based on http://mocappys.com/how-to-rig-a-character-for-motionbuilder/#.XIEicChKj4b
	#hips
	jnts = pm.ls('*:Hips*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='yzx', secondaryAxisOrient='xup')

	#spine + hierarchy (head)
	jnts = pm.ls('*:Spine*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='xzy', secondaryAxisOrient='xup', ch=1)

	#arms
	jnts = pm.ls('*:*Arm*') + pm.ls('*:Clavicle*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='xzy', secondaryAxisOrient='ydown', ch=1)

	#hand and finger
	jnts = pm.ls('*:*Hand*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='xzy', secondaryAxisOrient='zdown', ch=1)

	#thumb
	jnts = pm.ls('*:*Thumb*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='xzy', secondaryAxisOrient='ydown')

	#leg
	jnts = pm.ls('*:*Leg*')
	pm.select(jnts)
	pm.joint(zso=1, e=1, oj='xzy', secondaryAxisOrient='xup', ch=1)

def setRotationOrder():
	# rotation order
	
	# xyz-0
	# yzx-1
	# zxy-2
	# xzy-3
	# yxz-4
	# zyx-5
	

	#hips
	jnts = pm.ls('*:Hips*')
	for jnt in jnts:
		jnt.rotateOrder.set(3)
		
	#spine
	jnts = pm.ls('*:Spine*')
	for jnt in jnts:
		jnt.rotateOrder.set(0)
	#head
	jnts = pm.ls('*:Head*')
	for jnt in jnts:
		jnt.rotateOrder.set(3)
	#clavicle
	jnts = pm.ls('*:Clavicle*')
	for jnt in jnts:
		jnt.rotateOrder.set(3)
	#UpperArm
	jnts = pm.ls('*:UpperArm*')
	for jnt in jnts:
		jnt.rotateOrder.set(3)
	#UpperArm
	jnts = pm.ls('*:LowerArm*')
	for jnt in jnts:
		jnt.rotateOrder.set(3)
	#hand and finger
	jnts = pm.ls('*:*Hand*')
	for jnt in jnts:
		jnt.rotateOrder.set(4)
	#thumb
	jnts = pm.ls('*:*Thumb*')
	for jnt in jnts:
		jnt.rotateOrder.set(0)
	#leg
	jnts = pm.ls('*:*Leg*')
	for jnt in jnts:
		jnt.rotateOrder.set(0)

'''