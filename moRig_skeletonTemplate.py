import pymel.core as pm
import moRig_settings as settings
import moRig_utils as utils
import mo_Utils.mo_curveLib as curveLib
from mo_Utils.mo_logging import log_debug
from mo_Utils.mo_logging import log_info
reload(utils)


#log_debug('aAimLocsAndTargets is %s' % aAimLocsAndTargets)
def makeProxySkeletonFromSaveNode():
    '''
    Given a node with a template_string attribute storing the proxy information
    Reconstruct the proxy skeleton
    Returns:
    '''
    savetemplateString = pm.getAttr('skeleton_template_store.template_string')
    aData  = savetemplateString.split(',')
    aData = [str(i).replace('\'', '').replace('\"', '').replace(']', '').replace(' ', '') for i in aData]

    rootLoc = recallLocStructureV2(aData, False)

    connectLocStructure(rootLoc)

    return rootLoc

def makeProxySkeleton():

    disableProblemFeatures(True)

    # if we find a store node we can rebuild proxy from it
    if pm.objExists('%s_template_store'%settings.globalPrefs["skeletonName"]):
        rootLoc = makeProxySkeletonFromSaveNode()
        log_info('Success recreating proxy skeleton from store node %s.'%settings.globalPrefs["skeletonName"])
        return rootLoc

    # makes a proxy skeleton
    aData = ["skeleton_proxy_grpLoc", "0", "0|0|0&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "hip_loc", "*","0|28.78353936|-0.03793848382&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_grpLoc", "*", "0|31.15716066|-0.04843504669&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_leg_grpLoc", "*", "3.013497598|27.54369647|-0.07347699371&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_leg_grpLoc", "*", "-3.013326526|27.54369647|-0.07347699371&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_low_loc","spine_grpLoc", "0|31.15716066|-0.04843504669&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_mid_loc","spine_grpLoc", "0|35.13522079|-0.295672241&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_hi_loc", "spine_grpLoc", "0|40.30690808|-0.5424012602&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_end_grpLoc","spine_grpLoc", "0|43.19712444|-0.5424012602&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_leg02_loc", "L_leg_grpLoc", "3.013497598|14.85122758|0.336829834&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_leg01_loc",
             "L_leg_grpLoc", "3.013497598|27.54369647|-0.07347699371&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_foot_grpLoc", "L_leg_grpLoc", "3.013497598|2.032517305|-0.09561233996&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1","1",
             "R_leg02_loc", "R_leg_grpLoc", "-3.013326526|14.85122758|0.336829834&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1","1",
             "R_leg01_loc", "R_leg_grpLoc","-3.013497598|27.54369647|-0.07347699371&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_foot_grpLoc","R_leg_grpLoc", "-3.013497598|2.032517305|-0.09561233996&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "spine_end_loc", "spine_end_grpLoc", "0|43.19712444|-0.5424012602&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_arm_grpLoc", "spine_end_grpLoc", "6.034036297|44.76636291|-0.1956620128&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_clavicle_loc", "spine_end_grpLoc",
             "2.576254409|44.09779615|-0.5424012602&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_clavicle_loc",
             "spine_end_grpLoc", "-2.576254368|44.09779615|-0.5424012602&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_arm_grpLoc", "spine_end_grpLoc",
             "-6.033693755|44.76636291|-0.1956620128&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "head_grpLoc",
             "spine_end_grpLoc", "0|49.64237862|0.4188537574&0|0|0&1|1|1&0|-0.3068560494|-0.02760879863&0|0|0&1|1|1",
             "1", "neck_1_loc", "spine_end_grpLoc", "0|45.81468835|-0.08889763514&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "neck_2_loc", "spine_end_grpLoc", "0|46.77161092|0.038040213&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "neck_3_loc", "spine_end_grpLoc", "0|47.72853349|0.1649780611&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_toe_loc", "L_foot_grpLoc", "3.013497598|0.3777597796|9.104148301&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ball_loc", "L_foot_grpLoc",
             "3.013497598|0.4743170541|5.743069406&0|0|0&1|1|1&0|0|-0.8128087993&0|0|0&1|1|1", "1", "L_ankle_loc",
             "L_foot_grpLoc", "3.013497598|2.032517305|-0.09561233996&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_bigToe_grpLoc", "L_foot_grpLoc", "1.263494409|0.37775978|6.047476016&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_longToe_grpLoc", "L_foot_grpLoc",
             "2.277884259|0.37775978|6.578870073&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_middleToe_grpLoc",
             "L_foot_grpLoc", "3.34127198|0.37775978|6.478780752&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ringToe_grpLoc", "L_foot_grpLoc", "4.242210263|0.37775978|6.14152708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_pinkyToe_grpLoc", "L_foot_grpLoc",
             "4.977582|0.37775978|5.780492847&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ankle_loc", "R_foot_grpLoc",
             "-3.013326526|2.032517305|-0.09561233996&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ball_loc",
             "R_foot_grpLoc", "-3.013326526|0.4743170541|5.743069406&0|0|0&1|1|1&0|0|-0.8128087993&0|0|0&1|1|1", "1",
             "R_toe_loc", "R_foot_grpLoc", "-3.013326526|0.3777597796|9.104148301&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_bigToe_grpLoc", "R_foot_grpLoc", "-1.263494409|0.37775978|6.047476016&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_longToe_grpLoc", "R_foot_grpLoc",
             "-2.277884259|0.37775978|6.578870073&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_middleToe_grpLoc",
             "R_foot_grpLoc", "-3.34127198|0.37775978|6.478780752&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_ringToe_grpLoc", "R_foot_grpLoc", "-4.242210263|0.37775978|6.14152708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_pinkyToe_grpLoc", "R_foot_grpLoc",
             "-4.977582|0.37775978|5.780492847&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_hand_grpLoc", "L_arm_grpLoc",
             "18.2687344|44.75524492|-0.0747203956&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_arm02_loc", "L_arm_grpLoc",
             "12.64889295|44.75524492|-0.3871783966&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_arm01_loc",
             "L_arm_grpLoc", "6.034036297|44.75524492|-0.1956620128&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_hand_grpLoc", "R_arm_grpLoc", "-18.2687344|44.75524492|-0.0747203956&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_arm02_loc", "R_arm_grpLoc",
             "-12.64889295|44.75524492|-0.3871783966&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_arm01_loc",
             "R_arm_grpLoc", "-6.034036297|44.75524492|-0.1956620128&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_eye_loc",
             "head_grpLoc",
             "-1.736123706|51.70815386|3.848839017&0|0|0&1|1|1&0.5415357947|-0.4717286911|-0.9454389998&0|0|0&1|1|1",
             "1", "L_eye_loc", "head_grpLoc",
             "1.736222268|51.70815386|3.848839017&0|0|0&1|1|1&-0.5415357981|-0.4717286911|-0.9454389998&0|-0|0&1|1|1",
             "1", "head_01_loc", "head_grpLoc",
             "0|49.64237862|0.4188537574&0|0|0&1|1|1&0|0|5.551115123e-017&0|-0|0&1|1|1", "1", "jaw_01_loc",
             "head_grpLoc", "0|0|1.5&0|0|0&1|1|1&0|49.91368045|0.8941711202&0|-0|0&1|1|1", "1", "head_02_loc", "head_grpLoc",
             "0|0|0&0|0|0&1|1|1&0|55.05203036|0.8302589954&0|-0|0&0.5|0.5|0.5", "1", "L_bigToe_01_loc",
             "L_bigToe_grpLoc", "1.263494409|0.3777597796|6.047476016&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_bigToe_02_loc", "L_bigToe_grpLoc",
             "1.263494409|0.5562590566|8.135239833&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_bigToe_03_loc",
             "L_bigToe_grpLoc", "1.263494409|0.3777597796|9.168850535&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_longToe_01_loc", "L_longToe_grpLoc",
             "2.277884259|0.3777597796|6.578870073&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_longToe_02_loc",
             "L_longToe_grpLoc", "2.277884259|0.5562590566|8.301865281&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_longToe_03_loc", "L_longToe_grpLoc",
             "2.277884259|0.3777597796|9.255811049&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_middleToe_01_loc",
             "L_middleToe_grpLoc", "3.34127198|0.3777597796|6.478780752&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_middleToe_02_loc", "L_middleToe_grpLoc",
             "3.34127198|0.5562590566|8.131900804&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_middleToe_03_loc",
             "L_middleToe_grpLoc", "3.34127198|0.3777597796|8.878849699&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ringToe_01_loc", "L_ringToe_grpLoc",
             "4.242210263|0.3777597796|6.14152708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_ringToe_02_loc",
             "L_ringToe_grpLoc", "4.242210263|0.5562590566|7.802384719&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ringToe_03_loc", "L_ringToe_grpLoc",
             "4.242210263|0.3777597796|8.406833568&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_pinkyToe_01_loc",
             "L_pinkyToe_grpLoc", "4.977582|0.3777597796|5.780492847&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_pinkyToe_02_loc", "L_pinkyToe_grpLoc",
             "4.977582|0.5562590566|7.39184988&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_pinkyToe_03_loc",
             "L_pinkyToe_grpLoc", "4.977582|0.3777597796|7.859139708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_bigToe_01_loc", "R_bigToe_grpLoc",
             "-1.263494409|0.3777597796|6.047476016&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_bigToe_02_loc",
             "R_bigToe_grpLoc", "-1.263494409|0.5562590566|8.135239833&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_bigToe_03_loc", "R_bigToe_grpLoc",
             "-1.263494409|0.3777597796|9.168850535&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_longToe_01_loc",
             "R_longToe_grpLoc", "-2.277884259|0.3777597796|6.578870073&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_longToe_02_loc", "R_longToe_grpLoc",
             "-2.277884259|0.5562590566|8.301865281&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_longToe_03_loc",
             "R_longToe_grpLoc", "-2.277884259|0.3777597796|9.255811049&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_middleToe_01_loc", "R_middleToe_grpLoc",
             "-3.34127198|0.3777597796|6.478780752&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_middleToe_02_loc",
             "R_middleToe_grpLoc", "-3.34127198|0.5562590566|8.131900804&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_middleToe_03_loc", "R_middleToe_grpLoc",
             "-3.34127198|0.3777597796|8.878849699&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ringToe_01_loc",
             "R_ringToe_grpLoc", "-4.242210263|0.3777597796|6.14152708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_ringToe_02_loc", "R_ringToe_grpLoc",
             "-4.242210263|0.5562590566|7.802384719&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ringToe_03_loc",
             "R_ringToe_grpLoc", "-4.242210263|0.3777597796|8.406833568&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_pinkyToe_01_loc", "R_pinkyToe_grpLoc",
             "-4.977582|0.3777597796|5.780492847&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_pinkyToe_02_loc",
             "R_pinkyToe_grpLoc", "-4.977582|0.5562590566|7.39184988&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_pinkyToe_03_loc", "R_pinkyToe_grpLoc",
             "-4.977582|0.3777597796|7.859139708&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_pinky_grpLoc",
             "L_hand_grpLoc", "21.52003688|44.73346199|-1.893816526&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ring_grpLoc", "L_hand_grpLoc", "21.76014178|45.09340754|-0.8076245475&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_middle_grpLoc", "L_hand_grpLoc",
             "21.96855005|45.20015917|0.2817956095&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_index_grpLoc",
             "L_hand_grpLoc", "21.80772721|44.95734133|1.502138942&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_thumb_grpLoc", "L_hand_grpLoc", "19.45185783|44.18055371|1.157473975&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_pinkyCup_loc", "L_hand_grpLoc",
             "19.3014657|44.733462|-1.532765356&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_ringCup_loc", "L_hand_grpLoc",
             "19.28052447|44.943256|-0.6885645133&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_wrist_loc", "L_hand_grpLoc",
             "18.2687344|44.75524492|-0.0747203956&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_pinky_grpLoc",
             "R_hand_grpLoc", "-21.51886348|44.73346199|-1.893890243&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_ring_grpLoc", "R_hand_grpLoc", "-21.75895369|45.09340754|-0.807699187&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_middle_grpLoc", "R_hand_grpLoc",
             "-21.96735674|45.20015917|0.2817206422&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_index_grpLoc",
             "R_hand_grpLoc", "-21.80653866|44.95734133|1.502064273&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_thumb_grpLoc", "R_hand_grpLoc", "-19.45185783|44.18055371|1.157473975&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_pinkyCup_loc", "R_hand_grpLoc",
             "-19.3014657|44.733462|-1.532765356&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ringCup_loc",
             "R_hand_grpLoc", "-19.28052447|44.943256|-0.6885645133&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_wrist_loc", "R_hand_grpLoc", "-18.26775156|44.75524492|-0.07478214142&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1",
             "L_pinky_04_loc", "L_pinky_grpLoc", "25.02529979|44.69431483|-1.893816526&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_pinky_03_loc", "L_pinky_grpLoc",
             "23.75070357|44.77365816|-1.893816526&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_pinky_01_loc",
             "L_pinky_grpLoc", "21.52003688|44.73346199|-1.893816526&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_pinky_02_loc", "L_pinky_grpLoc", "22.64430958|44.84741279|-1.893816526&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_ring_04_loc", "L_ring_grpLoc",
             "26.29234302|45.01729861|-0.8076245475&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_ring_03_loc",
             "L_ring_grpLoc", "24.86857543|45.0968095|-0.8076245475&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_ring_02_loc", "L_ring_grpLoc", "23.27618811|45.1723294|-0.8076245475&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_ring_01_loc", "L_ring_grpLoc",
             "21.76014178|45.09340754|-0.8076245475&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_middle_04_loc",
             "L_middle_grpLoc", "26.63216727|45.11943681|0.2817956095&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_middle_03_loc", "L_middle_grpLoc",
             "25.16365461|45.19873565|0.2817956095&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_middle_02_loc",
             "L_middle_grpLoc", "23.76832148|45.29663976|0.2817956095&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_middle_01_loc", "L_middle_grpLoc",
             "21.96855005|45.20015917|0.2817956095&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_index_01_loc",
             "L_index_grpLoc", "21.80772721|44.95734133|1.502138942&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_index_02_loc", "L_index_grpLoc", "23.49126975|45.06165807|1.502138942&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_index_03_loc", "L_index_grpLoc",
             "24.88645214|44.95647455|1.502138942&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_index_04_loc",
             "L_index_grpLoc", "26.14595354|44.87742857|1.502138942&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_thumb_02_loc", "L_thumb_grpLoc", "20.28999093|43.60887316|2.621890191&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "L_thumb_03_loc", "L_thumb_grpLoc",
             "21.53770845|43.17885332|3.373828551&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "L_thumb_04_loc",
             "L_thumb_grpLoc", "22.99811726|42.54857357|3.761570831&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "L_thumb_01_loc", "L_thumb_grpLoc", "19.45185783|44.18055371|1.157473975&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_pinky_04_loc", "R_pinky_grpLoc",
             "-25.02393697|44.69431483|-1.893890243&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_pinky_03_loc",
             "R_pinky_grpLoc", "-23.74940126|44.77365816|-1.893890243&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_pinky_01_loc", "R_pinky_grpLoc", "-21.51886348|44.73346199|-1.893890243&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_pinky_02_loc", "R_pinky_grpLoc",
             "-22.64307236|44.84741279|-1.893890243&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ring_04_loc",
             "R_ring_grpLoc", "-26.29095591|45.01729861|-0.807699187&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_ring_03_loc", "R_ring_grpLoc", "-24.86724902|45.0968095|-0.807699187&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_ring_02_loc", "R_ring_grpLoc",
             "-23.27492696|45.1723294|-0.807699187&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_ring_01_loc",
             "R_ring_grpLoc", "-21.75895369|45.09340754|-0.807699187&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_middle_04_loc", "R_middle_grpLoc",
             "-26.63074355|45.11943681|0.2817206422&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_middle_03_loc",
             "R_middle_grpLoc", "-25.16229159|45.19873565|0.2817206422&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_middle_02_loc", "R_middle_grpLoc",
             "-23.76702376|45.29663976|0.2817206422&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_middle_01_loc",
             "R_middle_grpLoc", "-21.96735674|45.20015917|0.2817206422&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_index_01_loc", "R_index_grpLoc", "-21.80653866|44.95734133|1.502064273&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_index_02_loc", "R_index_grpLoc",
             "-23.48998563|45.06165807|1.502064273&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_index_03_loc",
             "R_index_grpLoc", "-24.88510295|44.95647455|1.502064273&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_index_04_loc", "R_index_grpLoc", "-26.14454389|44.87742857|1.502064273&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_thumb_01_loc", "R_thumb_grpLoc",
             "-19.45080372|44.18055371|1.157407751&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1", "R_thumb_02_loc",
             "R_thumb_grpLoc", "-20.28887489|43.60887316|2.621820078&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1",
             "R_thumb_03_loc", "R_thumb_grpLoc", "-21.53652678|43.17885332|3.373754315&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1",
             "1", "R_thumb_04_loc", "R_thumb_grpLoc",
             "-22.9968509|42.54857357|3.761491275&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1", "1"]

    rootLoc = recallLocStructureV2(aData, True)

    log_debug('connectLocStructure')

    connectLocStructure(rootLoc)

    log_info('Success creating proxy skeleton %s.' % settings.globalPrefs["skeletonName"])

    return rootLoc


def  recallLocStructureV2(aData, useUIParams):
    """==========================================================================================================\\
    ==========================================================================================================\\
    ====================          moRecallLocStructureV2            ====================\\
    ====================        (supports multiple neck and spine joints)     ====================\\
    ==========================================================================================================\\
    ==========================================================================================================\\"""

    objName = ""
    parent = ""
    locTransStr = ""
    aStr = []
    aSubStr = []
    loc = ""
    aRel = []
    baseName = ""
    aRestoreAttTable = []
    restoreAttData = ""
    # recalls a given loc structure ($aData which is created by moEncodeLocStructure)
    # if $useUIParams, it respects the values in the skeletonMaker UI (usually only when building a skeleton for the first time, not when recalling one).
    # returns rootLoc
    aTrans = []
    aRot = []
    i = 0
    k = 0
    frozen = 0
    colorInd = 0
    rootLocColorInd = 13
    grpLocColorInd = 13
    locColorInd = 15
    # useUIParams if ctrl key is pressed
    mods = int(pm.getModifiers())
    if mods / 4 % 2:
        useUIParams = int(True)
    # need to offset scale for wire controller proc -- which bases size relative to global scale

    so = 0.0
    gScale = float(settings.globalPrefs["globalScale"])
    if gScale == 0:
        so = float(1)


    else:
        so = float(1 / gScale)

    rootLocName = "skeleton_proxy_grpLoc"
    if pm.objExists(rootLocName):
        pm.delete(rootLocName)

    rootLoc = makeLocator(rootLocName)
    utils.cleanUpAttr(rootLoc, ["tx", "ty", "tz", "rx", "ry", "rz"])
    aRel = pm.listRelatives(rootLoc, type='shape')
    pm.setAttr((aRel[0] + ".overrideEnabled"), True)
    pm.setAttr((aRel[0] + ".overrideColor"),
               rootLocColorInd)
    aXAxisUpCircleJnts = ["L_clavicle_loc", "L_arm01_loc", "L_arm02_loc", "L_wrist_loc", "R_clavicle_loc",
                          "R_arm01_loc", "R_arm02_loc", "R_wrist_loc"]
    aXAxisLocSize = [3, 6, 5, 4, 3, 6, 5, 4]
    aYAxisUpCircleJnts = ["hip_loc", "spine_low_loc", "spine_mid_loc", "spine_hi_loc", "L_leg01_loc", "L_leg02_loc",
                          "L_ankle_loc", "R_leg01_loc", "R_leg02_loc", "R_ankle_loc", "neck_loc", "head_01_loc"]
    aYAxisLocSize = [14, 16, 17, 18, 10, 7, 6, 10, 7, 6, 8, 12]
    aZAxisUpCircleJnts = ["L_ball_loc", "R_ball_loc"]
    aZAxisLocSize = [4, 4]
    axisUpIndex = 0
    wireScale = 0.0
    aRootLocScale = []
    locScale = float(settings.globalPrefs["proxyLocScale"])
    # following three arrays are look ups.  Loc in $aAimLocs will be aimed at loc in same index in $aAimLocsAndTargets.
    # $aAimLocTargData[] will hold the aData entry for the target, which is required in case the target doesn't exist when the loc (or grpLoc) to be aimed is created.
    aAimLocs = ["L_thumb_grpLoc", "R_thumb_grpLoc", "L_thumb_01_loc", "L_thumb_02_loc", "L_thumb_03_loc",
                "L_thumb_04_loc", "R_thumb_01_loc", "R_thumb_02_loc", "R_thumb_03_loc", "R_thumb_04_loc"]
    aAimLocsAndTargets = ["L_thumb_02_loc", "R_thumb_02_loc", "L_thumb_02_loc", "L_thumb_03_loc", "L_thumb_04_loc",
                          "L_thumb_03_loc", "R_thumb_02_loc", "R_thumb_03_loc", "R_thumb_04_loc", "R_thumb_03_loc"]
    aAimLocsNegateAimAxis = ["L_thumb_04_loc", "R_thumb_04_loc"]
    # will be aimed along negative aim axis
    aAimLocTargData = []
    aimLoc = ""
    aAimDataStr = []
    aimConst = []
    vAim = pm.dt.Vector()
    vUp = pm.dt.Vector()
    aimIndex = 0
    leftLoc = 0
    neckCtrlSize = 8
    midSpineCtrlSize = 17
    fingerNum = 0
    toeNum = 0
    midSpineJntNum = 0
    neckJntNum = 0
    aDataFingerNum = 0
    aDataToeNum = 0
    aDataMidSpineJntNum = 0
    aDataNeckJntNum = 0
    # following two vars are used with UIParams == true and recalling a proxy with the same number of joints as specified in the UI.  In that case just use the existing structure specified in aData for the spine or neck.
    spineAlreadySpecified = int(False)
    neckAlreadySpecified = int(False)
    # get fingerNum, spineNum, and neckNum values from aData
    fingerNum = 2
    # always at least two fingers
    toeNum = midSpineJntNum = neckJntNum = 0
    for i in range(0, len(aData), 4):
        #log_debug("i in aData is %s" %i)
        if pm.mel.match("spine_mid[0-9_]+loc", aData[i]) == aData[i]:
            log_debug('aData has spine mid01_loc %s'%aData[i])
            aDataMidSpineJntNum += 1

            # make sure curves get built
            aYAxisUpCircleJnts.append(aData[i])
            aYAxisLocSize.append(float(midSpineCtrlSize))

        if aData[i] == "L_thumb_01_loc" or aData[i] == "L_index_01_loc" or aData[i] == "L_middle_01_loc" or aData[
            i] == "L_ring_01_loc" or aData[i] == "L_pinky_01_loc":
            aDataFingerNum += 1

        if aData[i] == "L_bigToe_01_loc" or aData[i] == "L_longToe_01_loc" or aData[i] == "L_middleToe_01_loc" or aData[
            i] == "L_ringToe_01_loc" or aData[i] == "L_pinkyToe_01_loc":
            aDataToeNum += 1

        if pm.mel.match("neck[0-9_]+loc", aData[i]) == aData[i]:
            aDataNeckJntNum += 1
            # make sure curves get built
            aYAxisUpCircleJnts.append(aData[i])
            aYAxisLocSize.append(float(neckCtrlSize))



        # want to prefetch any data for locs in the $aAimLocsAndTargets[]; will need it to aim locs in $aAimLocs[] (and the likelyhood that the targets are created first is low)
        for k in range(0, len(aAimLocsAndTargets)):
            aAimLocTargData.append("")
            if pm.mel.match(aAimLocsAndTargets[k], aData[i]) == aAimLocsAndTargets[k]:
                aAimLocTargData[k] = aData[i + 2]

    log_debug("Window moSklMkrWin exists: %s" %aData)
    log_debug("midSpineJntNum: %s" % midSpineJntNum)
    log_debug("useUIParams: %s" % useUIParams)
    log_debug("spineAlreadySpecified: %s" % spineAlreadySpecified)
    #return
    #midSpineJntNum > 1 and useUIParams and not spineAlreadySpecified
    if useUIParams:
        fingerNum = int(settings.globalPrefs["fingerNum"])
        # done
        toeNum = int(settings.globalPrefs["toeNum"])
        midSpineJntNum = int(settings.globalPrefs["spineCtrlNum"]) - 2
        neckJntNum = int(settings.globalPrefs["neckNum"])

        #log_debug("before neckJntNum != aDataNeckJntNum: aData is %s" % aData)
        if neckJntNum != aDataNeckJntNum:
            aExistingNeckJnts = objExistInProxyDataStr(
                ["neck_loc", "neck_1_loc", "neck_2_loc", "neck_3_loc", "neck_4_loc"], aData)
            # log_debug("before len(aExistingNeckJnts) > 1: aData is %s" % aData)
            if len(aExistingNeckJnts) > 1:
                aData = renameProxyLocInDataStr(aExistingNeckJnts[0], "neck_loc", aData)
            # log_debug("before for i in range(1, len(aExistingNeckJnts)): aData is %s" % aData)
            # multiple neck joints in aData, rename neck_1_loc to neck_loc and delete others
            for i in range(1, len(aExistingNeckJnts)):
                aData = removeProxyLocFromDataStr(aExistingNeckJnts[i], aData)

        # log_debug("neckJntNum != aDataNeckJntNum: aData is %s" % aData)
        else:
            log_debug("neckAlreadySpecified: aData is %s" % aData)
            neckAlreadySpecified = int(True)

        if midSpineJntNum != aDataMidSpineJntNum:
            aExistingMidSpineJnts = objExistInProxyDataStr(
                ["spine_mid_loc", "spine_mid_1_loc", "spine_mid_2_loc", "spine_mid_3_loc", "spine_mid_4_loc",
                    "spine_mid_5_loc", "spine_mid_6_loc", "spine_mid_7_loc", "spine_mid_8_loc", "spine_mid_9_loc"],
                aData)
            if len(aExistingMidSpineJnts) > 1:
                aData = renameProxyLocInDataStr(aExistingMidSpineJnts[0], "spine_mid_loc", aData)
                # multiple midSpine joints in aData, rename spine_mid_1_loc to spine_mid_loc and delete others
                for i in range(1, len(aExistingMidSpineJnts)):
                    aData = removeProxyLocFromDataStr(aExistingMidSpineJnts[i], aData)
            log_debug("midSpineJntNum != aDataMidSpineJntNum: aData is %s" % aData)
        else:
            log_debug("spineAlreadySpecified: aData is %s" % aData)
            spineAlreadySpecified = int(True)
        log_debug("useUIParams: aData is %s" % aData)
    else:
        fingerNum = aDataFingerNum
        toeNum = aDataToeNum
        midSpineJntNum = aDataMidSpineJntNum
        neckJntNum = aDataNeckJntNum
        # update sliders with current proxy values

        if pm.intSliderGrp('moSklMkrFingerNumIntSldrGrp', q=1, ex=1):
            pm.intSliderGrp('moSklMkrFingerNumIntSldrGrp', e=1, v=fingerNum)
        if pm.intSliderGrp('moSklMkrToeNumIntSldrGrp', q=1, ex=1):
            pm.intSliderGrp('moSklMkrToeNumIntSldrGrp', e=1, v=toeNum)
        if pm.intSliderGrp('moSklMkrMidSpineNumIntSldrGrp', q=1, ex=1):
            pm.intSliderGrp('moSklMkrMidSpineNumIntSldrGrp', e=1, v=(midSpineJntNum + 2))
        if pm.intSliderGrp('moSklMkrNeckNumIntSldrGrp', q=1, ex=1):
            pm.intSliderGrp('moSklMkrNeckNumIntSldrGrp', e=1, v=neckJntNum)


    log_info("\n$fingerNum = " + str(fingerNum))

    delRingCup = 0
    delPinkyCup = 0
    aFingersToDelete = []
    if fingerNum == 2:
        aFingersToDelete = ["middle", "ring", "pinky"]

        delRingCup = delPinkyCup = int(True)

    elif fingerNum == 3:
        aFingersToDelete = ["middle", "ring"]

        delRingCup = int(True)


    elif fingerNum == 4:
        aFingersToDelete = ["ring"]

        delRingCup = int(True)

    aToesToDelete = []
    if toeNum == 0:
        aToesToDelete = ["bigToe", "longToe", "middleToe", "ringToe", "pinkyToe"]


    elif toeNum == 1:
        aToesToDelete = ["longToe", "middleToe", "ringToe", "pinkyToe"]


    elif toeNum == 2:
        aToesToDelete = ["longToe", "middleToe", "ringToe"]


    elif toeNum == 3:
        aToesToDelete = ["longToe", "ringToe"]


    elif toeNum == 4:
        aToesToDelete = ["middleToe"]

    aMidSpineLocs = []
    aMidSpineLocNames = []
    aExtraDataStr = []
    tempLocGrp = ""
    aNeckLocs = []
    aNeckLocNames = []
    # neck joints
    if neckJntNum == 1:
        pass
    # nothing

    elif neckJntNum > 1 and useUIParams and not neckAlreadySpecified:
        aHeadPos = getProxyLocLocation("head_01_loc", aData)
        log_debug('ProxyLocLocation is %s' % aHeadPos)

        aNeckBasePos = getProxyLocLocation("neck_loc", aData)
        # get parent group
        neckParent = getProxyLocParent("neck_loc", aData)
        # make temp grp to hold locs
        tempLocGrp = str(pm.group(em=1, name="tempProxySpineLocGrp", w=1))
        for i in range(1, neckJntNum + 1):
            aNeckLocNames.append("neck_" + str(i) + "_loc")

        aNeckLocNames.append("temp_neckSpacer_1_loc")
        aNeckLocNames.append("temp_neckSpacer_2_loc")
        # make curve string
        neckCurve = ""
        neckCurveStr = ""
        neckCurveStr = "curve -d 1"
        neckCurveStr += " -p " + str(aNeckBasePos[0]) + " " + str(aNeckBasePos[1]) + " " + str(aNeckBasePos[2])
        neckCurveStr += " -p " + str(aHeadPos[0]) + " " + str(aHeadPos[1]) + " " + str(aHeadPos[2])
        neckCurveStr += " -n \"tempProxyNeckCurve\""
        neckCurve = str(pm.mel.eval(neckCurveStr))
        aNeckLocs = makeSpineJntsFromCurve(neckCurve, aNeckLocNames, tempLocGrp, True)
        # delete curves
        pm.delete(neckCurve)
        # get loc positions, add them to controller curve arrays
        aExtraDataStr = []
        for i in range(0, (len(aNeckLocs) - 2)):
            aTrans = pm.pointPosition(aNeckLocs[i], w=1)
            aRot = pm.xform(aNeckLocs[i], q=1, ro=1, ws=1)
            aExtraDataStr.append(aNeckLocNames[i])
            aExtraDataStr.append(neckParent)
            aExtraDataStr.append(
                str(aTrans[0]) + "|" + str(aTrans[1]) + "|" + str(aTrans[2]) + "&" + str(aRot[0]) + "|" + str(
                    aRot[1]) + "|" + str(aRot[2]) + "&1|1|1&0|0|0&0|0|0&1|1|1")
            aExtraDataStr.append("1")
            # make sure the control curves get built
            aYAxisUpCircleJnts.append(aNeckLocNames[i])
            aYAxisLocSize.append(float(neckCtrlSize))

        pm.delete(tempLocGrp)
        # get rid of temp locs
        if len(aExtraDataStr) > 0:
            aData = removeProxyLocFromDataStr("neck_loc", aData)
            # remove spine_mid_loc from aData
            # and add new locs
            aData = aData + aExtraDataStr
        #log_debug("neckJntNum > 1 and useUIParams and not neckAlreadySpecified. aData is %s" % aData)

    if midSpineJntNum == 1:
        pass
    # now do spine joints (number of mid joints are variable from 1 to 5)
    # nothing

    elif midSpineJntNum > 1 and useUIParams and not spineAlreadySpecified:
        log_debug("Enter midSpineJntNum %s"%midSpineJntNum)
        aSpineLowPos = getProxyLocLocation("spine_low_loc", aData)
        aSpineMidPos = getProxyLocLocation("spine_mid_loc", aData)
        aSpineHighPos = getProxyLocLocation("spine_hi_loc", aData)
        # get parent group
        spineLowParent = getProxyLocParent("spine_low_loc", aData)
        # make array of spine loc names (including placeholders for low and high joints)
        aMidSpineLocNames.append( "spine_low_tempLoc" )
        # make temp grp to hold locs
        tempLocGrp = str(pm.group(em=1, name="tempProxySpineLocGrp", w=1))
        for i in range(1, midSpineJntNum + 1):
            aMidSpineLocNames.append("spine_mid_" + str(i) + "_loc")

        aMidSpineLocNames.append("spine_hi_tempLoc")
        # make curve
        spineCurve = pm.curve(n='tempProxySpineCurve', d=1, p=[(aSpineLowPos[0],aSpineLowPos[1],aSpineLowPos[2]),
                                                (aSpineMidPos[0], aSpineMidPos[1], aSpineMidPos[2]),
                                                (aSpineHighPos[0], aSpineHighPos[1], aSpineHighPos[2]),])

        log_debug("spineCurve is %s" % spineCurve)
        # fit an ep curve over our chimpy 1 degree spineCurve
        aStr = pm.fitBspline(spineCurve, ch=1, tol=0.01)
        log_debug("fitBspline is %s" % spineCurve)

        bSplineSpineCurve = aStr[0]
        log_debug("rebuild curve %s"%aStr)
        aStr = pm.rebuildCurve(bSplineSpineCurve, rt=0, ch=1, end=1, d=3, kr=0, s=0, kcp=0, tol=0.01, kt=0, rpo=1,
                               kep=1)
        bSplineSpineCurve = aStr[0]
        log_debug("rebuild makeSpineJntsFromCurve %s" % aMidSpineLocNames)

        aMidSpineLocs = makeSpineJntsFromCurve(bSplineSpineCurve, aMidSpineLocNames, tempLocGrp, True)
        log_debug("done make spine jnts from  curve %s" % aStr)
        # delete curves
        log_debug("delete %s" % spineCurve)
        log_debug("delete %s" % spineCurve)
        pm.delete(spineCurve)
        log_debug("delete %s" % bSplineSpineCurve)
        pm.delete(bSplineSpineCurve)
        log_debug("enter for aMidSpineLocs %s" % aMidSpineLocs)
        # get loc positions, add them to controller curve arrays
        aExtraDataStr = []
        for i in range(1, (len(aMidSpineLocs) - 1)):
            aTrans = pm.pointPosition(aMidSpineLocs[i], w=1)
            # skip first and last placeholder locs
            aRot = pm.xform(aMidSpineLocs[i], q=1, ro=1, ws=1)
            aExtraDataStr.append(aMidSpineLocNames[i])
            aExtraDataStr.append(spineLowParent)
            aExtraDataStr.append(
                str(aTrans[0]) + "|" + str(aTrans[1]) + "|" + str(aTrans[2]) + "&" + str(aRot[0]) + "|" + str(
                    aRot[1]) + "|" + str(aRot[2]) + "&1|1|1&0|0|0&0|0|0&1|1|1")
            aExtraDataStr.append("1")
            # make sure the control curves get built
            aYAxisUpCircleJnts.append(aMidSpineLocNames[i])
            aYAxisLocSize.append(float(midSpineCtrlSize))

        pm.delete(tempLocGrp)
        # get rid of temp locs
        if len(aExtraDataStr) > 0:
            aData = removeProxyLocFromDataStr("spine_mid_loc", aData)
            # remove spine_mid_loc from aData
            # and add new locs
            aData = aData + aExtraDataStr

    if len(aData) > 4:
        if aData[1] == "0":
            aStr = aData[2].split("&")
            # check first four items in $aData contain info about rootLoc scale (only in saves made with versions 2.1 and up) -- if it does it needs to be removed from $aData
            # yep, this is a post 2.1 save -- get the scale info and remove these first four items from $aData
            aSubStr = aStr[5].split("|")
            aRootLocScale = [float(aSubStr[0]), float(aSubStr[1]), float(aSubStr[2])]
            # now remove first four items (rootLoc info) from $aData

            aStr = []
            for i in range(0, len(aData), 4):
                if i > 0:
                    aStr.append(aData[i])
                    aStr.append(aData[i + 1])
                    aStr.append(aData[i + 2])
                    aStr.append(aData[i + 3])

            aData = aStr
            log_debug('aData is %s'%aData)
    log_debug('Enter aData list run trough %s'%len(aData))

    for i in range(0, len(aData), 4):

        objName = aData[i]
        #log_debug('Run aData is %s'%aData[i])
        #log_debug('Parent is %s' % aData[i+1])
        #log_debug('locTransStr is %s' % aData[i+2])
        parent = aData[i + 1]
        locTransStr = aData[i + 2]
        #log_debug('frozen int aData is %s'%aData[i+3])
        frozen = int(aData[i + 3])
        if parent == "*":
            parent = rootLoc
        #log_debug('parent is %s' % parent)
        if not pm.objExists(parent):
            continue
        # get baseName

        aStr = objName.split("_")
        log_debug('aStr is %s' % aStr)

        if len(aStr) == 3:
            baseName = aStr[1]
        else:
            baseName = ""

        if delRingCup and baseName == "ringCup":
            continue

        if delPinkyCup and baseName == "pinkyCup":
            continue
        #log_debug('Before If aStr is %s'%aStr)

        if pm.mel.match("_grpLoc$", objName) != "":
            log_debug("pm.mel.match grpLoc$ %s"%objName)
            if len(aFingersToDelete) > 0:
                if getPosInStrArray(baseName, aFingersToDelete) != -1:
                    continue
                # need to compare baseName of current obj with items in $aFingersToDelete -- if this finger is in $aFingersToDelete then skip it

            if len(aToesToDelete) > 0:
                if getPosInStrArray(baseName, aToesToDelete) != -1:
                    continue

            loc = str(makeWireController("sphere", 1, [], 1.5 * so))
            aStr = str(pm.rename(loc, objName))
            loc = aStr


        elif getPosInStrArray(objName, aYAxisUpCircleJnts) != -1:
            #log_debug("getPosInStrArray(objName, aYAxisUpCircleJnts %s" % objName)
            axisUpIndex = int(getPosInStrArray(objName, aYAxisUpCircleJnts))
            #log_debug("before make wire %s" % objName)
            wireScale = aYAxisLocSize[axisUpIndex]

            loc = makeWireController("circle", 1, [], wireScale * so)
            #log_debug("after make wire %s" % objName)
            aStr = str(pm.rename(loc, objName))
            loc = aStr


        elif getPosInStrArray(objName, aXAxisUpCircleJnts) != -1:
            axisUpIndex = int(getPosInStrArray(objName, aXAxisUpCircleJnts))
            wireScale = aXAxisLocSize[axisUpIndex]
            loc = str(makeWireController("circle", 0, [], wireScale * so))
            aStr = str(pm.rename(loc, objName))
            loc = aStr


        elif getPosInStrArray(objName, aZAxisUpCircleJnts) != -1:
            axisUpIndex = int(getPosInStrArray(objName, aZAxisUpCircleJnts))
            wireScale = aZAxisLocSize[axisUpIndex]
            loc = str(makeWireController("circle", 2, [], wireScale * so))
            aStr =  str(pm.rename(loc, objName))
            loc = aStr


        else:
            log_debug("else make locator %s" % objName)
            loc = makeLocator(objName)
            aStr = str(loc)
            if len(aStr) == 1:
                pm.setAttr((aStr + ".localScale"), locScale, locScale, locScale)

        # position
        aStr = locTransStr.split("&")
        log_debug("aStr locTransStr.split & is %s" % aStr)
        # recall locTransStr
        # trans

        if not pm.objExists(loc):
            log_debug("obj not exisiting. %s. skipping" % (loc))
            continue

        aSubStr = aStr[0].split("|")
        pm.setAttr((loc + ".t"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
        #log_debug("transform %s to aSubStr from aStr[0] is %s" % (loc,aSubStr))
        # rot

        aSubStr = aStr[1].split("|")
        pm.setAttr((loc + ".r"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
        log_debug("rotation aSubStr from aStr[1] is %s" % aSubStr)
        # scale
        aSubStr = aStr[2].split("|")
        pm.setAttr((loc + ".s"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
        #log_debug("scale aSubStr from aStr[2] is %s" % aSubStr)
        loc = str(parentSave(loc, parent))
        log_debug("loc is %s" % loc)
        # is this an aim loc?


        aimIndex = int(getPosInStrArray(objName, aAimLocs))
        log_debug(" aimIndex %s " % aimIndex)
        if aimIndex != -1 and aAimLocTargData[aimIndex] != "":
            #log_debug("Enter aimIndex %s "%aimIndex)
            aimLoc = makeLocator(objName + "_tempAimTarget_loc")
            # create temp loc and its parent
            # read loc data and position loc
            aAimDataStr = aAimLocTargData[aimIndex].split("&")
            aSubStr = aAimDataStr[0].split("|")
            #log_debug("aAimDataStr %s" % aAimDataStr)
            #log_debug("aSubStr %s" % aSubStr)
            pm.setAttr((aimLoc + ".t"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
            aSubStr = aAimDataStr[1].split("|")
            pm.setAttr((aimLoc + ".r"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
            # create aim constraint
            leftLoc = int((pm.getAttr(aimLoc + ".tx") > 0))

            #log_debug("leftLoc %s" % leftLoc)
            vAim = pm.dt.Vector((leftLoc))
            vAim and pm.dt.Vector([1, 0, 0]) or pm.dt.Vector([-1, 0, 0])
            vUp = pm.dt.Vector((leftLoc))
            vUp and pm.dt.Vector([0, 1, 0]) or pm.dt.Vector([0, 1, 0])
            # negate aim axis, if req'd
            if getPosInStrArray(objName, aAimLocsNegateAimAxis) != -1:
                vAim *= pm.dt.Vector(-1)
            #log_debug("aimLoc, loc %s %s" % (aimLoc, loc))
            aimConst = pm.aimConstraint(aimLoc, loc, weight=1, upVector=((vUp.x), (vUp.y), (vUp.z)),
                                        worldUpObject=aimLoc, worldUpType="objectrotation", offset=(0, 0, 0),
                                        aimVector=((vAim.x), (vAim.y), (vAim.z)), worldUpVector=(0, 1, 0))

            # grpFrz
            loc = groupFreezeReturnObj(loc)
            # clean up
            pm.delete(aimConst)
            pm.delete(aimLoc)
        if frozen:
            pm.makeIdentity(loc, apply=True, s=1, r=1, t=1)
        # save the control attributes values (if any) to restore once the loc structure has been completely recreated
        log_debug("if len(aStr) >= 6: %s') " % aStr)
        if len(aStr) >= 6:
            aRestoreAttTable.append(objName + "&" + aStr[3] + "&" + aStr[4] + "&" + aStr[5])
        # color the controls
        # log_debug("aRel = pm.listRelatives(loc, type='shape') %s " % aRestoreAttTable)
        aRel = pm.listRelatives(loc, type='shape')
        if len(aRel) == 1:
            if pm.mel.match("_grpLoc$", objName) != "":
                colorInd = grpLocColorInd
            # if (endsWith($objName, "_grpLoc"))

            else:
                colorInd = locColorInd

            pm.setAttr((aRel[0] + ".overrideEnabled"), True)
            pm.setAttr((aRel[0] + ".overrideColor"),
                       colorInd)

    #log_debug("can now restore control attributes values (if any) %s" % aimIndex)
    # can now restore control attributes values (if any)
    for restoreAttData in aRestoreAttTable:
        aStr = restoreAttData.split("&")
        objName = aStr[0]
        # trans
        aSubStr = aStr[1].split("|")
        pm.setAttr((objName + ".t"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
        # rot
        aSubStr = aStr[2].split("|")
        pm.setAttr((objName + ".r"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))
        # scale
        aSubStr = aStr[3].split("|")
        pm.setAttr((objName + ".s"), (float(aSubStr[0])), (float(aSubStr[1])), (float(aSubStr[2])))

    if len(aRootLocScale) > 0:
        pm.setAttr((rootLoc + ".s"),
                   aRootLocScale[0], aRootLocScale[1], aRootLocScale[2])

    return rootLoc


def connectLocStructure(rootLoc):
    log_debug("Connecting loc structure")
    if pm.objExists(rootLoc):
        log_debug("rootLoc exist")
        data = ""
        obj = ""
        aSub = []
        startLoc = ""
        endLoc = ""
        aStr = []
        # if $rootLoc exists, this proc will make the connections and draw the lines to make it a real true proxy skeleton
        i = 0
        lockAxes = int(settings.globalPrefs["lockProxyCtlAxes"])
        useBones = int(settings.globalPrefs["useBonesForProxyDisplay"])
        # draw lines
        aLineConnections = getJointConnectionsArray(False)
        log_debug("aLineConnections is exist %s"%aLineConnections)
        for data in aLineConnections:
            #log_debug("aLineConnections data is %s"%data )
            data = pm.mel.substituteAllString(data, "_hand_loc", "_wrist_loc")
            # need to replace "hand_loc" with "wrist_loc" (hand locs haven't been created yet)
            aSub = data.split(">")


            for i in range(0, (len(aSub) - 1)):
                startLoc = aSub[i]
                # connect locs with lines
                endLoc = aSub[i + 1]

                if pm.objExists(startLoc) and pm.objExists(endLoc):
                    moConnectWithLine(startLoc, endLoc, useBones)

        aMirrorObj = ["L_arm_grpLoc", "L_hand_grpLoc", "L_pinkyCup_loc", "L_ringCup_loc", "L_pinky_grpLoc",
                      "L_pinky_04_loc", "L_pinky_03_loc", "L_pinky_01_loc", "L_pinky_02_loc", "L_ring_grpLoc",
                      "L_ring_04_loc", "L_ring_03_loc", "L_ring_02_loc", "L_ring_01_loc", "L_middle_grpLoc",
                      "L_middle_04_loc", "L_middle_03_loc", "L_middle_02_loc", "L_middle_01_loc", "L_index_grpLoc",
                      "L_index_01_loc", "L_index_02_loc", "L_index_03_loc", "L_index_04_loc", "L_thumb_grpLoc",
                      "L_thumb_02_loc", "L_thumb_03_loc", "L_thumb_04_loc", "L_thumb_01_loc", "L_cup_loc",
                      "L_wrist_loc", "L_arm02_loc", "L_arm01_loc", "L_clavicle_loc", "L_eye_loc", "L_leg_grpLoc",
                      "L_foot_grpLoc", "L_toe_loc", "L_ball_loc", "L_ankle_loc", "L_leg02_loc", "L_leg01_loc"]
        aToeGrpLocs = ["L_bigToe_grpLoc", "L_longToe_grpLoc", "L_middleToe_grpLoc", "L_ringToe_grpLoc",
                       "L_pinkyToe_grpLoc"]
        aToes = ["L_bigToe_01_loc", "L_bigToe_02_loc", "L_bigToe_03_loc", "L_longToe_01_loc", "L_longToe_02_loc",
                 "L_longToe_03_loc", "L_middleToe_01_loc", "L_middleToe_02_loc", "L_middleToe_03_loc",
                 "L_ringToe_01_loc", "L_ringToe_02_loc", "L_ringToe_03_loc", "L_pinkyToe_01_loc", "L_pinkyToe_02_loc",
                 "L_pinkyToe_03_loc"]
        # add Toes
        aMirrorObj = aMirrorObj + aToeGrpLocs
        aMirrorObj = aMirrorObj + aToes
        mObj = ""
        for obj in aMirrorObj:
            mObj = obj.replace("L_", "R_")
            if pm.objExists(mObj):
                connectMirrorTrans(obj, mObj, 0)
                pointConnect(obj, mObj, 6)
                connectMirrorRot(obj, mObj, 1)
                connectMirrorRot(obj, mObj, 2)
                orientConnect(obj, mObj, 1)
                if obj.endswith("_grpLoc"):
                    pm.connectAttr((str(obj) + ".s"), (mObj + ".s"))
                # connect grpLoc scale with mirror

        aOriginObj = ["head_grpLoc", "spine_grpLoc", "spine_end_grpLoc", "head_01_loc",
                      "head_02_loc", "neck_loc", "neck_1_loc", "neck_2_loc", "neck_3_loc", "neck_4_loc",
                      "hip_loc", "spine_low_loc", "spine_mid_loc", "spine_mid_1_loc", "spine_mid_2_loc",
                      "spine_mid_3_loc", "spine_mid_4_loc", "spine_mid_5_loc", "spine_mid_6_loc", "spine_mid_7_loc",
                      "spine_mid_8_loc", "spine_mid_9_loc", "spine_hi_loc", "spine_end_loc", "jaw_01_loc"]
        for obj in aOriginObj:
            if pm.objExists(obj):
                pm.setAttr((str(obj) + ".tx"),
                           lock=True)
            # lock off tx

        if lockAxes:
            aLockTX = ["L_foot_grpLoc", "L_index_01_loc", "L_leg01_loc", "L_leg02_loc", "L_ankle_loc", "L_ball_loc",
                       "L_toe_loc"]
            aLockTY = ["L_hand_grpLoc", "L_arm01_loc", "L_arm02_loc", "L_wrist_loc"]
            aLockTZ = ["L_index_01_loc", "L_index_02_loc", "L_index_03_loc", "L_index_04_loc", "L_index_02_loc",
                       "L_index_03_loc", "L_index_04_loc", "L_middle_01_loc", "L_middle_02_loc", "L_middle_03_loc",
                       "L_middle_04_loc", "L_ring_01_loc", "L_ring_02_loc", "L_ring_03_loc", "L_ring_04_loc",
                       "L_pinky_01_loc", "L_pinky_02_loc", "L_pinky_03_loc", "L_pinky_04_loc"]
            # add toes to lockTx
            aLockTX = aLockTX + aToes
            for obj in aLockTX:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".tx"),
                               lock=True)

            for obj in aLockTY:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".ty"),
                               lock=True)

            for obj in aLockTZ:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".tz"),
                               lock=True)
                # string $aLockRX[] = {"spine_grpLoc","L_arm_grpLoc","spine_end_grpLoc"};

            aLockRX = ["spine_grpLoc", "spine_end_grpLoc"]
            aLockRY = ["spine_grpLoc", "spine_end_grpLoc", "head_grpLoc"]
            aLockRZ = ["spine_grpLoc", "spine_end_grpLoc", "head_grpLoc"]
            # string $aLockRZ[] = {"spine_grpLoc","spine_end_grpLoc","head_grpLoc","L_leg_grpLoc","L_foot_grpLoc"};
            for obj in aLockRX:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".rx"),
                               lock=True)

            for obj in aLockRY:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".ry"),
                               lock=True)

            for obj in aLockRZ:
                if pm.objExists(obj):
                    pm.setAttr((str(obj) + ".rz"),
                               lock=True)

    if pm.objExists("skeleton_proxy_grpLoc"):
        if pm.nodeType("skeleton_proxy_grpLoc") == "transform":
            scaleSkeletonJntRadius(pm.listRelatives('skeleton_proxy_grpLoc', type='joint', ad=1),
                                              "template_hip_loc_jnt", True)

    pm.select(clear=1)


def disableProblemFeatures(warn):
    smWarning = int(False)
    # if softmod is enabled this proc disables it and issues a warning if $warn
    # softMod
    if pm.mel.exists("softSelect"):
        if pm.softSelect(q=1, softSelectEnabled=1):
            pm.softSelect(softSelectEnabled=False)
            smWarning = int(True)

    if pm.currentCtx() == "softModContext":
        pm.setToolTo('moveSuperContext')
        smWarning = int(True)

    installedVersion = str(pm.about(iv=1))
    if pm.mel.match("2016 SP1$", installedVersion) != "":
        autoKeyframe = int(pm.autoKeyframe(q=1, state=1))
        if autoKeyframe:
            pm.autoKeyframe(state=False)
            if warn:
                pm.warning(
                    "Auto Keyframe has been disabled. Otherwise this script would run like molasses in this version of Maya.")

    if smWarning and warn:
        pm.warning(
            "This script doesn't work with sofMod of any kind.  Soft selection has been disabled and the current context has been switched to move.  Let us not discuss this again")


def getJointConnectionsArray(lfSideOnly):
    aSub = []
    aLocConnections = []
    aStr = []
    # returns array of loc connections (used in connectLocStructures and skeletonizeProxy)
    # if $lfSideOnly == false, returns both connections for lf and rt
    i = 0
    aLocConnections = [
        "hip_loc>spine_low_loc>spine_mid_loc>spine_mid_1_loc>spine_mid_2_loc>spine_mid_3_loc>spine_mid_4_loc>spine_mid_5_loc>spine_mid_6_loc>spine_mid_7_loc>spine_mid_8_loc>spine_mid_9_loc>spine_hi_loc>spine_end_loc>neck_loc>neck_1_loc>neck_2_loc>neck_3_loc>neck_4_loc>head_01_loc>head_02_loc",
        "head_01_loc>L_eye_loc",
        "head_01_loc>jaw_01_loc",
        "spine_end_loc>L_clavicle_loc>L_arm01_loc>L_arm02_loc>L_wrist_loc>L_hand_loc",
        "L_hand_loc>L_thumb_01_loc>L_thumb_02_loc>L_thumb_03_loc>L_thumb_04_loc",
        "L_hand_loc>L_index_01_loc>L_index_02_loc>L_index_03_loc>L_index_04_loc",
        "L_hand_loc>L_middle_01_loc>L_middle_02_loc>L_middle_03_loc>L_middle_04_loc",
        "L_hand_loc>L_ringCup_loc>L_ring_01_loc>L_ring_02_loc>L_ring_03_loc>L_ring_04_loc",
        "L_hand_loc>L_pinkyCup_loc>L_pinky_01_loc>L_pinky_02_loc>L_pinky_03_loc>L_pinky_04_loc",
        "hip_loc>L_leg01_loc>L_leg02_loc>L_ankle_loc>L_ball_loc>L_toe_loc",
        "L_ball_loc>L_bigToe_01_loc>L_bigToe_02_loc>L_bigToe_03_loc",
        "L_ball_loc>L_longToe_01_loc>L_longToe_02_loc>L_longToe_03_loc",
        "L_ball_loc>L_middleToe_01_loc>L_middleToe_02_loc>L_middleToe_03_loc",
        "L_ball_loc>L_ringToe_01_loc>L_ringToe_02_loc>L_ringToe_03_loc",
        "L_ball_loc>L_pinkyToe_01_loc>L_pinkyToe_02_loc>L_pinkyToe_03_loc"]
    # update $aLineConnections[0] with existing spine joints
    aSub = aLocConnections[0].split(">")
    for i in range(0, len(aSub)):
        if pm.objExists(aSub[i]):
            aStr.append(aSub[i])

    aLocConnections[0] = ">".join(aStr)
    # add rt side if required
    if not lfSideOnly:
        aStr = []
        for i in range(1, len(aLocConnections)):
            aStr.append(substituteAll("L_", aLocConnections[i], "R_"))

        aLocConnections = aLocConnections + aStr

    return aLocConnections


def makeLocator(name, snapToTarget=False, grp=False):
    # creates a locator named $name in the position of $snapToTarget, and puts it in $grp;  returns full path to locator
    loc = pm.spaceLocator(name=name)

    if snapToTarget and pm.objExists(snapToTarget):
        snapConstrain(snapToTarget, loc, 1)

    if snapToTarget and pm.objExists(grp):
        pm.parent(loc, grp)

    return loc.fullPath()

def snapConstrain(driver, driven, delete=1):
    """
    delete: 0 -- keep created constraints
    delete: 1 -- delete both constraints
    delete: 2 -- keep point constraint
    delete: 3 -- keep orient constraint
    """
    pointCons = pm.pointConstraint(driver, driven, weight=1, offset=(0, 0, 0))
    if delete == 1 or delete == 3:
        pm.delete(pointCons)
    orientCons = pm.orientConstraint(driver, driven, weight=1, offset=(0, 0, 0))
    if delete == 1 or delete == 2:
        pm.delete(orientCons)


def objExistInProxyDataStr(aObj, aData):
    aRet = []
    # returns objects in $aObj that exist in $aData
    i = 0
    for i in range(0, len(aData), 4):
        if aData[i] in aObj:
            aRet.append(aData[i])

    return aRet


def getProxyLocParent(proxyLocName, aData):
    i = 0
    # returns parent of given proxy loc or nothing on failure
    ret = ""
    for i in range(0, len(aData), 4):
        if aData[i] == proxyLocName:
            ret = aData[i + 1]
            break

    return ret

def renameProxyLocInDataStr(proxyLocName, newName, aData):
    i = 0
    # renames all instances of proxyLocName to newName in $aData, returns modified aData
    ret = int(False)
    for i in range(0, len(aData), 4):
        if aData[i] == proxyLocName:
            aData[i] = newName

        if aData[i + 3] == proxyLocName:
            aData[i + 3] = newName

    return aData


def removeProxyLocFromDataStr(proxyLocName, aData):
    i = 0
    # returns aData without entry for $proxyLocName
    aRetData = []
    proxyParent = ""
    proxyParent = getProxyLocParent(proxyLocName, aData)

    for i in range(0, len(aData), 4):
        if aData[i] != proxyLocName:
            # parent = aData[i + 1]
            # if parent == proxyLocName:
            #     parent = proxyParent
            aRetData.append(aData[i])
            aRetData.append((aData[i + 1] == proxyLocName) and proxyParent or aData[i + 1])
            aRetData.append(aData[i + 2])
            aRetData.append(aData[i + 3])

    return aRetData


def substituteAll(regEx, subject, replace):

    lastSubject = ""
    # like substitute all, but will replace all occurences of $regEx in $subject with $replace
    str = subject
    while str != lastSubject:
        lastSubject = str
        str = str.replace(regEx, replace)

    return str


def scaleSkeletonJntRadius(aJnts, hipJnt, proxyStyle):
    # sets skeleton joint radii to make it all beautiful
    # set proxyStyle to true if this is a proxy skeleton, where jnts are separated into up and down joint pairs.
    aDnJnts = []
    aUpJnts = []
    aJntSizeLU = []
    floatVal = 0.0
    vector = pm.dt.Vector()
    maxTx = float(0)
    minRad = .5
    if len(aJnts) == 0:
        return

    if proxyStyle:
        minRad = .4
        for jnt in aJnts:
            jnt = str(pm.mel.longNameOf(jnt))
            if pm.mel.attributeExists("overrideEnabled", jnt):
                pm.setAttr((jnt + ".overrideEnabled"),1)
                pm.setAttr((jnt + ".overrideDisplayType"),2)

            tObj = str(pm.mel.firstParentOf(pm.mel.longNameOf(jnt)))
            if pm.objExists(tObj):
                if pm.nodeType(tObj) == "joint":
                    aDnJnts.append(str(pm.mel.longNameOf(jnt)))

        if len(aDnJnts) > 0:
            for jnt in aDnJnts:
                tUpJnt = str(pm.mel.firstParentOf(pm.mel.longNameOf(jnt)))
                # get distance between up and down joint
                aTrans1 = pm.xform(tUpJnt, q=1, ws=1, t=1)
                aTrans2 = pm.xform(jnt, q=1, ws=1, t=1)
                vector = pm.dt.Vector([aTrans2[0] - aTrans1[0], aTrans2[1] - aTrans1[1], aTrans2[2] - aTrans1[2]])
                floatVal = float(pm.mel.mag(vector))
                maxTx = float(max(maxTx, floatVal))
                aUpJnts.append(tUpJnt)
                aJntSizeLU.append(floatVal)

            for i in range(0, len(aUpJnts)):
                length = aJntSizeLU[i]
                floatVal = (length / maxTx) * (1 - minRad) + minRad
                pm.setAttr((aUpJnts[i] + ".radius"), floatVal)

        return

    # do non proxy style skeletons
    for jnt in aJnts:
        floatVal = float(pm.getAttr(jnt + ".tx"))
        maxTx = float(max(maxTx, floatVal))

    for jnt in aJnts:
        if pm.mel.longNameOf(jnt) == pm.mel.longNameOf(hipJnt):
            pm.setAttr((jnt + ".radius"), 1)
        else:
            aRel = pm.listRelatives(jnt, c=1, type='joint')
            if len(aRel) > 0:
                length = float(pm.getAttr(aRel[0] + ".tx"))
                floatVal = (length / maxTx) * (1 - minRad) + minRad
                pm.setAttr((jnt + ".radius"), floatVal)
            else:
                pm.setAttr((jnt + ".radius"), minRad)


def getProxyLocLocation(proxyLocName, aData):
    aSubData = []
    transStr = []
    rotStr = []
    scaleStr = []
    # returns ws translate, rotation, and scale info for a given proxy loc from the dataString $aData, or an empty array on failure.
    # form of {tx, ty, tz, rx, ry, rz, sx, sy, sz}
    i = 0
    aRet = range(9)
    for i in range(0, len(aData), 4):
        if aData[i] == proxyLocName:
            aSubData = aData[i + 2].split("&")
            # {"skeleton_proxy_grpLoc","0","0|0|0&0|0|0&1|1|1&0|0|0&0|0|0&1|1|1","1","hip_loc","*"
            # only need first three sub arrays (don't need channelBox offsets)
            transStr = aSubData[0].split("|")
            rotStr = aSubData[1].split("|")
            scaleStr = aSubData[2].split("|")
            log_debug(" transStr %s"%transStr)
            # trans
            aRet[0] = float(transStr[0])
            aRet[1] = float(transStr[1])
            aRet[2] = float(transStr[2])
            # rot
            aRet[3] = float(rotStr[0])
            aRet[4] = float(rotStr[1])
            aRet[5] = float(rotStr[2])
            # scale
            aRet[6] = float(scaleStr[0])
            aRet[7] = float(scaleStr[1])
            aRet[8] = float(scaleStr[2])
            break

    return aRet





def makeWireController(wireType, facingAxis, aOffset, size):
    if facingAxis == 0: facingString = "x+"
    elif facingAxis == 1: facingString = "y+"
    elif facingAxis == 2: facingString = "z+"
    elif facingAxis == 3: facingString = "x-"
    elif facingAxis == 4: facingString = "y-"
    elif facingAxis == 5: facingString = "z-"

    curve = curveLib.wireController(type=wireType, facingAxis=facingString, aOffset=aOffset, size=size, getIns=False, useWS=True)

    # builds a control curve
    # add hidden atts
    globalScale = float(settings.globalPrefs["globalScale"])
    utils.setWireAttributes(curve, ["wireScale",
                                         (str(size / globalScale)),
                                         "wireType", wireType, "wireFacingAxis",
                                         (str(facingAxis))])
    return curve



def makeSpineJntsFromCurve(curve, aJntNames, grp, makeLocsInsteadOfJnts):
    numJnts = len(aJntNames)
    # makes size($aJntNames) joints (or locs if $makeLocsInsteadOfJnts) following $curve and places them in $grp (if it exists)
    # returns new joint paths
    aRet = []
    if len(aJntNames) >= 2:
        pm.select(clear=1)
        aJnts = []
        jnt = ""
        aParam = range(numJnts)
        i = 0
        for i in range(0, (numJnts - 1)):
            if i == 0:
                aParam[i] = float(0)
            else:
                aParam[i] = float(float(i) / (numJnts - 1))
        # rebuild curve
        jntPath = ""
        for i in range(0, len(aParam)):

            param = aParam[i]
            aTrans = pm.pointOnCurve(curve, position=1, parameter=param, turnOnPercentage=True)

            if makeLocsInsteadOfJnts:
                jnt = pm.spaceLocator(name=aJntNames[i])
                pm.move(jnt, aTrans[0], aTrans[1], aTrans[2],  absolute=1)
            else:
                jnt = pm.joint(p=(aTrans[0], aTrans[1], aTrans[2]), n=aJntNames[i])

            if (i == 0 or makeLocsInsteadOfJnts) and grp != "" and pm.objExists(grp):
                jnt = pm.parent(jnt, grp)[0]
            elif not makeLocsInsteadOfJnts:
                jnt = jntPath + "|" + jnt

            aJnts.append(jnt)
            aRet.append(jnt)
            jntPath = jnt

        aRet = aJnts

    return aRet

def parentSave(child, parent):
    ret = ""
    # parents $child to $parent and returns new full path of $child
    parent = pm.ls(parent, long=1)[0]
    child = pm.ls(child, long=1)[0]
    if child.getParent() != parent:
        aStr = pm.parent(child, parent)
        ret = aStr[0].fullPath()
    else:
        ret = child
    return ret



def getPosInStrArray(str, aStr):
    i = 0
    # returns int (0 based) position of string in string array or -1 on fail.
    ret = -1
    for i in range(0, len(aStr)):
        if aStr[i] == str:
            ret = i
            break

    return ret


def groupFreezeReturnObj(obj):
    gpName = ""
    aRel = []
    frzGrpName = ""
    # same function as above, but returns new obj path
    frzGrpName = "%sfrzGrp"%(pm.ls(obj)[0].name())
    gpName = pm.group(em=1, name=frzGrpName).fullPath()
    #log_debug('gpName is %s' % gpName)
    utils.snap(obj, gpName)

    aRel = pm.listRelatives(obj, p=1, fullPath=1, type='transform')

    if len(aRel) > 0:
        gpName = pm.parent(gpName, aRel[0])[0]
    #log_debug('gpName 2 is %s' % gpName)
    obj = str(pm.parent(obj, gpName)[0].fullPath())
    return obj


def moConnectWithLine(obj1, obj2, useBones):
    lineName = ""
    obj1=pm.PyNode(obj1)
    obj2=pm.PyNode(obj2)
    aObj2Children = []
    aObj2UpChildren = []
    lineShape = ""
    aStr = []
    aRel = []
    obj2Parent = ""
    origName = ""
    origPath = ""
    tObjPath = ""
    taChildrenPath = []
    tGrp = ""
    tGrp2 = ""
    # connects two transforms with a line or a bone
    if not useBones:
        aObj2Children = pm.listRelatives(obj2, fullPath=1, type='transform', children=1)
        # unparent children
        if len(aObj2Children) > 0:
            aObj2UpChildren = pm.parent(aObj2Children, w=1)[0]
        # done

        # annotate
        annLoc = makeLocator(obj2 + "_annLoc")
        lineShape = str(pm.annotate(annLoc, tx=""))
        pm.pointConstraint(obj2, annLoc)
        pm.setAttr((annLoc + ".v"), 0)

        # parent $annLoc $obj2;
        annLoc = pm.parent(annLoc, obj2)[0].fullPath()
        aStr = pm.listRelatives(lineShape, p=1, type='transform')
        if len(aStr) == 1:
            lineName = aStr[0]
        # problem when obj2 has been frozen
        # parent $lineName $obj1;

        lineName = str(pm.parent(lineName, obj1)[0].fullPath())
        utils.snap(obj1, lineName)
        pm.setAttr((lineShape + ".overrideEnabled"),1)
        pm.setAttr((lineShape + ".overrideDisplayType"), 2)
        # reparent children
        if len(aObj2Children) > 0:
            i = 0
            aObj2UpChildren = pm.parent(aObj2UpChildren, obj2)[0]
            for i in range(0, len(aObj2UpChildren)):
                origName = aObj2Children[i].name()
                if aObj2UpChildren[i] != origName:
                    pm.rename(aObj2UpChildren[i], origName)

        pm.select(clear=1)
        # done
        lineName = pm.rename(lineName, "template_" + obj1.name())


    else:
        aTrans1 = []
        aTrans2 = []
        aTrans1 = pm.xform(obj1, q=1, ws=1, t=1)
        aTrans2 = pm.xform(obj2, q=1, ws=1, t=1)
        # make joint
        pm.select(d=1)
        jnt1 = str(pm.joint(p=(aTrans1[0], aTrans1[1], aTrans1[2]),
                            n=("template_" + obj1.name() + "_jnt")))
        jnt2 = str(pm.joint(p=(aTrans2[0], aTrans2[1], aTrans2[2]),
                            n=("template_" +(obj1).name() + "_end_jnt")))
        pm.select(d=1)
        # set dnJnt vis and radius
        pm.setAttr((jnt2 + ".radius"),
                   0)
        pm.setAttr((jnt2 + ".v"),
                   0)
        # position and parent
        utils.snap(obj1, jnt1)
        pm.parentConstraint(obj2, jnt2)
        jnt1 = pm.parent(jnt1, obj1)[0]
        utils.cleanUpAttr(sel=[jnt1, jnt2], listAttr=['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'], l=1, k=1, cb=1)
        lineName = jnt1

    return lineName


def pointConnect(target, follower, type):
    if (type % 2) == 1 and not (pm.isConnected((target + ".tx"), (follower + ".tx"))):
        pm.connectAttr((target + ".tx"), (follower + ".tx"))
        """
        creates something like a point constraint by connecting translation attribtutes of $follower to $target
        $type is x=1 y=2 z=4 -- add them together to specify which atts you want connected xy would be 3, zx would be 5, etc
        """

    if type != 4 and type != 5 and type != 1 and not (pm.isConnected((target + ".ty"), (follower + ".ty"))):
        pm.connectAttr((target + ".ty"), (follower + ".ty"))

    if type >= 4 and not (pm.isConnected((target + ".tz"), (follower + ".tz"))):
        pm.connectAttr((target + ".tz"), (follower + ".tz"))


def orientConnect(target, follower, type):
    if (type % 2) == 1 and not (pm.isConnected((target + ".rx"), (follower + ".rx"))):
        pm.connectAttr((target + ".rx"), (follower + ".rx"))
        """
        creates something like an orient constraint by connecting translation attribtutes of $follower to $target
        $type is x=1 y=2 z=4 -- add them together to specify which atts you want connected xy would be 3, zx would be 5, etc
        """

    if type != 4 and type != 5 and type != 1 and not (pm.isConnected((target + ".ry"), (follower + ".ry"))):
        pm.connectAttr((target + ".ry"), (follower + ".ry"))

    if type >= 4 and not (pm.isConnected((target + ".rz"), (follower + ".rz"))):
        pm.connectAttr((target + ".rz"), (follower + ".rz"))

def connectMirrorTrans(obj1, obj2, axis):
    aAxisStr = ["x", "y", "z"]
    # connects $obj1 and $obj2 translation on $axis axis to mirror across the origin ($axis: 0,1,2 = x,y,z)
    axisStr = ".t" + aAxisStr[axis]
    revNode = str(pm.createNode('plusMinusAverage', n="abRTMirrorTransPlsMns"))
    pm.setAttr((revNode + ".operation"),2)
    pm.setAttr((revNode + ".input1D[0]"),0)
    pm.connectAttr((obj1 + axisStr), (revNode + ".input1D[1]"),f=1)
    pm.connectAttr((revNode + ".output1D"), (obj2 + axisStr),f=1)


def connectMirrorRot(obj1, obj2, axis):
    aAxisStr = ["x", "y", "z"]
    # connects $obj1 and $obj2 translation on $axis axis to mirror across the origin ($axis: 0,1,2 = x,y,z)
    axisStr = ".r" + aAxisStr[axis]
    revNode = str(pm.createNode('plusMinusAverage', n="abRTMirrorRotPlsMns"))
    pm.setAttr((revNode + ".operation"),2)
    pm.setAttr((revNode + ".input1D[0]"),0)
    pm.connectAttr((obj1 + axisStr), (revNode + ".input1D[1]"),f=1)
    pm.connectAttr((revNode + ".output1D"), (obj2 + axisStr),f=1)


def saveProxySkeleton(deleteExisting=True):

    disableProblemFeatures(True)
    settings.initGlobals()

    # save current proxy skeleton string to a node
    templateString = encodeLocStructure("%s_proxy_grpLoc"%settings.globalPrefs["skeletonName"]
                                                               , 1)
    storenodename = '%s_template_store'%settings.globalPrefs["skeletonName"]
    # create node to store
    if pm.objExists(storenodename) and deleteExisting:
        pm.delete(storenodename)
    if not pm.objExists(storenodename):
        pm.createNode('transform', n=storenodename)
        pm.addAttr(storenodename, ln="template_string", dt="string", k=0)

    pm.select(clear=1)
    pm.setAttr('%s.template_string'%storenodename, '%s'%templateString, type="string")

    log_info('Success saving proxy skeleton.')

def encodeLocStructure(rootLoc, preserveOffsets):
    aRet = []
    aRel = []
    # given the root loc of a proxy rig (under which all others are parented) this will arrange the locs in an array that can be used to
    # rebuild the hierarchy.
    # return string form is {locator1Name, locator1Parent, locator2Name, locator2Parent} -- if parent is $rootLoc, locatorParent will be represented with "*"
    # string will be returned in order so that parents of locators are created before their children, so, if you create locs starting with the
    # beginning of the array, you'll never parent a loc to a nonexistent node
    # returns (locName, locParent, locTransString("tx|ty|tz&rx|ry|rz&sx|sy|sz"), frozen(bool))
    # as of v 2.1 of the script, the return string also includes the current offsets tacked on to the end of the locTransString, so it now looks like "tx|ty|tz&rx|ry|rz&sx|sy|sz|cbTx|cbTy|cbTz&cbRx|cbRy|cbRz&cbSx|cbSy|cbSz" where "cb" prefix stands for the channelBox value of an attribute (not the ws value)
    # if $preserveOffsets, existing rotations and translations will be preseerved, otherwise, loc structure will be saved zseroed out
    if pm.objExists(rootLoc):
        aChildren = []
        aParents = []
        aTempSort = []
        # used to sort locs by the depth of their path
        k = 0
        aSel = pm.listRelatives(rootLoc, fullPath=1, type='transform', allDescendents=1)
        for objPath in aSel:
            if objPath.name().endswith("_loc") or objPath.name().endswith("_grpLoc"):
                baseName = objPath.name()
                if not baseName.startswith("template_"):
                    aChildren.append(objPath)

        # sort locs by the depth of their path
        for objPath in aChildren:
            parent = ""
            # ignore line related transforms
            objName = objPath.name()
            # size of $aParents will never be smaller than 2
            aParents = objPath.fullPath().split("|")
            # find parents that aren't frzGrps
            for k in range(len(aParents) - 2, 0 - 1, -1):
                if pm.mel.match("_frz_grp$", aParents[k]) != "":
                    continue
                else:
                    parent = aParents[k]
                    break

            if parent == "":
                print "\nUnable to find parent (\"" + parent + "\") for object: \"" + objName + "\"."
                pm.error("Unable to continue")

            if parent == rootLoc:
                parent = "*"
            # $parent = $aParents[size($aParents)-2];

            aTempSort.append(objPath.fullPath())
            aTempSort.append(objName)
            aTempSort.append(parent)
            aTempSort.append(str(len(aParents) - 2))

        aTemp = []
        aRestoreTransTable = []
        aLockedAtts = []
        aConnectedAtts = []
        depth = 0
        cDepth = 0
        aOverride = []
        aTrans = []
        aRot = []
        aScale = []
        aCbTrans = []
        aCbRot = []
        aCbScale = []
        aLockCheckAtts = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
        aConnectedCheckAtts = ["tx", "ty", "tz", "rx", "ry", "rz", "s"]

        # save rootLoc transform atts
        aRootLocScale = pm.getAttr(rootLoc + ".s")
        pm.setAttr((rootLoc + ".s"),1, 1, 1)
        aRet.append(rootLoc)
        aRet.append("0")
        aRet.append("0|0|0&0|0|0&1|1|1&0|0|0&0|0|0&" + str(aRootLocScale[0]) + "|" + str(aRootLocScale[1]) + "|" + str(
            aRootLocScale[2]))
        aRet.append("1")
        # have to disconnect all connected objs first, otherwise resetting the positive x t, r, and s attributes will similarly affect the connected objs
        for i in range(0, len(aTempSort), 4):
            objPath = aTempSort[i]
            # disconnect conected atts and save them to reconnect when save is complete
            for att in aConnectedCheckAtts:
                objAttStr = str(objPath) + "." + str(att)
                # check for connected attributes
                attSfd = str(pm.connectionInfo(objAttStr, sourceFromDestination=1))
                if attSfd != "":
                    aConnectedAtts.append(attSfd + ">" + objAttStr)
                    pm.disconnectAttr(attSfd, objAttStr)

        tLoc = makeLocator("moEncodeStructureLoc")
        # done
        while len(aTempSort) > 0:
            aTemp = []
            for i in range(0, len(aTempSort), 4):
                objPath = aTempSort[i]
                objName = aTempSort[i + 1]
                parent = aTempSort[i + 2]
                depth = int(aTempSort[i + 3])
                if depth == cDepth:
                    log_debug('depth is cDepth: %s'%objPath)
                    aRel = pm.listRelatives(objPath, type='shape')
                    shape = str((len(aRel) > 0))
                    shape and aRel[0] or ""
                    if preserveOffsets:
                        aCbTrans = pm.getAttr(str(objPath) + ".t")
                        # set the $obj channelBox trans, rot, and scale atts back to 0 and save those values as offsets (so when skeleton is recalled its local t, r, and s values are preserved)
                        aCbRot = pm.getAttr(str(objPath) + ".r")
                        aCbScale = pm.getAttr(str(objPath) + ".s")
                        # save cb atts to restore once proxy has been saved ("objPath&tx|ty|tz&rx|ry|rz&sx|sy|sz"
                        aRestoreTransTable.append(
                            str(objPath) + "&" + str(aCbTrans[0]) + "|" + str(aCbTrans[1]) + "|" + str(
                                aCbTrans[2]) + "&" + str(aCbRot[0]) + "|" + str(aCbRot[1]) + "|" + str(
                                aCbRot[2]) + "&" + str(aCbScale[0]) + "|" + str(aCbScale[1]) + "|" + str(aCbScale[2]))


                    else:
                        aCbTrans = [0, 0, 0]
                        aCbRot = [0, 0, 0]
                        aCbScale = [1, 1, 1]

                    # unlock locked attributes and save them to lock again once save is complete
                    for att in aLockCheckAtts:
                        objAttStr = str(objPath) + "." + str(att)
                        # check for locked attributes
                        if pm.getAttr(objAttStr, lock=1):
                            aLockedAtts.append(objAttStr)
                            pm.setAttr(objAttStr, lock=False)

                    if preserveOffsets:
                        pm.setAttr((str(objPath) + ".t"),0, 0, 0)
                        # set atts to default
                        pm.setAttr((str(objPath) + ".r"),0, 0, 0)
                        pm.setAttr((str(objPath) + ".s"),1, 1, 1)

                    utils.snap(objPath, tLoc)
                    # make loc trans string
                    # now get the absolute values
                    aTrans = pm.xform(tLoc, q=1, ws=1, t=1)
                    aRot = [0, 0, 0]
                    # $aRot = `xform -q -os -ro $tLoc`;
                    aScale = pm.xform(objPath, q=1, s=1, r=1)
                    locTransStr = str(aTrans[0]) + "|" + str(aTrans[1]) + "|" + str(aTrans[2]) + "&" + str(
                        aRot[0]) + "|" + str(aRot[1]) + "|" + str(aRot[2]) + "&" + str(aScale[0]) + "|" + str(
                        aScale[1]) + "|" + str(aScale[2]) + "&" + str(aCbTrans[0]) + "|" + str(aCbTrans[1]) + "|" + str(
                        aCbTrans[2]) + "&" + str(aCbRot[0]) + "|" + str(aCbRot[1]) + "|" + str(aCbRot[2]) + "&" + str(
                        aCbScale[0]) + "|" + str(aCbScale[1]) + "|" + str(aCbScale[2])
                    aRet.append(str(objName))
                    aRet.append(str(parent))
                    aRet.append(str(locTransStr))
                    aRet.append("1")


                else:
                    log_debug('depth is NOT cDepth: %s' % objPath)
                    aTemp.append(str(objPath))
                    aTemp.append(objName)
                    aTemp.append(parent)
                    aTemp.append(str(depth))

            aTempSort = aTemp
            cDepth += 1

        pm.delete(tLoc)
        # restore channelBox attribute values
        data = ""
        aData = []
        aTransData = []
        aRotData = []
        aScaleData = []
        for data in aRestoreTransTable:
            aData = data.split("&")
            objPath = aData[0]
            # retrieve cb values
            aTransData = aData[1].split("|")
            aRotData = aData[2].split("|")
            aScaleData = aData[3].split("|")
            # restore cb values
            pm.setAttr((str(objPath) + ".t"), (float(aTransData[0])), (float(aTransData[1])), (float(aTransData[2])))
            pm.setAttr((str(objPath) + ".r"), (float(aRotData[0])), (float(aRotData[1])), (float(aRotData[2])))
            pm.setAttr((str(objPath) + ".s"), (float(aScaleData[0])), (float(aScaleData[1])), (float(aScaleData[2])))

        # relock previously locked atts
        for att in aLockedAtts:
            pm.setAttr(att, lock=True)
        # reconnected previously connected atts

        for data in aConnectedAtts:
            aData = data.split(">")
            pm.connectAttr(aData[0], aData[1])

        pm.setAttr((rootLoc + ".s"), aRootLocScale[0], aRootLocScale[1], aRootLocScale[2])
    # reset rootLoc scale att

    return aRet



def skeletonizeProxy(spineWtJntNum='global', jointRadius=0.4):
    """
    create skinJnt from
        :param spineWtJntNum='global': 
    """
    # root
    tJntGrp = ''
    pm.delete(pm.ls('C_root_jnt'))
    aJnts = duplicateJointHierarchy(['spine_grpLoc'], ['C_root_jnt'], tJntGrp)
    tJntGrp = aJnts[0]

    ######### spine #########

    if spineWtJntNum == 'global':
        spineWtJntNum=int(settings.globalPrefs["spineJntNum"])

    # insert weight split jnts
    upArmSplitNum=int(settings.globalPrefs["upArmSplitNum"])
    foreArmSplitNum=int(settings.globalPrefs["foreArmSplitNum"])
    upLegSplitNum=int(settings.globalPrefs["upLegSplitNum"])
    kneeSplitNum=int(settings.globalPrefs["lowLegSplitNum"])

    spineMidJntsNum = len(pm.ls('spine_mid_*_loc'))
    aMidSpineJnts = []
    if spineMidJntsNum > 0:
        for i in range(spineMidJntsNum):
            aMidSpineJnts.append('spine_mid_%s_loc' %(i+1))
    else:
        aMidSpineJnts.append('spine_mid_loc')
    if spineWtJntNum>0:

        aSpineRigCtrlJnts=['spine_low_loc']
        # need to get spine jnts -- {$hipJnt, $rootJnt, $midJnt1, [$midJnt2, $midJnt3, ...], $hiJnt, $endJnt}
        aSpineRigCtrlJnts=aSpineRigCtrlJnts + aMidSpineJnts
        aSpineRigCtrlJnts.append('spine_hi_loc')


        log_debug('aSpineRigCtrlJnts is %s '%aSpineRigCtrlJnts)
        log_debug('spineWtJntNum is %s '%spineWtJntNum)

        spineJnts = makeSpine(aSpineRigCtrlJnts, spineWtJntNum, parentTo='C_root_jnt')

    log_debug('Done skeletonProxy spine')

    ######### chest #########

    aJnts = duplicateJointHierarchy(['spine_hi_loc', 'spine_end_loc'],
                                    ['C_chest01_skinJnt', 'C_chest02_skinJntEnd'],
                                    tJntGrp)
    orientJoints(aJnts, "xzy", "zup")
    pm.joint(aJnts[-1], zso=1, ch=1, e=1, oj='none')

    pm.parent('C_chest01_skinJnt', spineJnts[-1])

    log_debug('Done skeletonProxy chest')

    ######### pelvis #########

    aJnts = duplicateJointHierarchy(['spine_low_loc', 'hip_loc'],
                                    ['C_pelvis01_skinJnt', 'C_pelvis02_skinJntEnd'],
                                    tJntGrp)
    orientJoints(aJnts, "xzy", "zup")
    pm.joint(aJnts[-1], zso=1, ch=1, e=1, oj='none')

    log_debug('Done skeletonProxy pelvis')


    ######### neck #########

    tJntGrp = 'C_chest01_skinJnt'
    neck_proxy_names = []
    neck_rig_names = []
    i = 0
    neck_proxy_names.append('spine_end_loc')
    neck_rig_names.append('C_neck01_skinJnt')

    neckJnts = pm.ls('neck_loc') + pm.ls('neck_*_loc')

    for i in range(len(neckJnts)):
        i = int(i)
        neck_proxy_names.append(neckJnts[i])
        neck_rig_names.append('C_neck%02d_skinJnt' % (i + 2))

    neck_proxy_names.append('head_01_loc')
    neck_rig_names.append('C_head01_skinJnt')
    neck_proxy_names.append('head_02_loc')
    neck_rig_names.append('C_head02_skinJnt')

    aJnts = duplicateJointHierarchy(neck_proxy_names,
                                    neck_rig_names,
                                    tJntGrp)
    orientJoints(aJnts, "xzy", "zup")

    ######### jaw and eyes #########

    tJntGrp = 'C_head01_skinJnt'
    aJnts = duplicateJointHierarchy(["head_01_loc", "jaw_01_loc"],
                                    ["C_jaw01_skinJnt", "C_jaw02_skinJnt"],
                                    tJntGrp)
    orientJoints(aJnts, "xzy", "zup")
    aJnts = duplicateJointHierarchy(["head_01_loc", "L_eye_loc"],
                                    ["L_eye01_skinJnt", "L_eye02_skinJnt"],
                                    tJntGrp)
    orientJoints(aJnts, "xzy", "zup")
    pm.mirrorJoint(aJnts[0], mirrorBehavior=1, searchReplace=("L_", "R_"))


    #########  Arm #########

    tJntGrp = 'C_chest01_skinJnt'
    aJnts = duplicateJointHierarchy(["spine_end_loc", "L_arm01_loc", "L_arm02_loc", "L_wrist_loc"],
                                    ["L_clav01_skinJnt", "L_arm01_skinJnt", "L_arm02_skinJnt", "L_hand01_skinJnt"],
                                    tJntGrp)
    pm.parent(aJnts[0], tJntGrp)
    # orient
    orientJoints([aJnts[3]], "xyz", "ydown")
    # orient wrist, then other upArm and elbow (different orientations)
    orientJoints([aJnts[0], aJnts[1], aJnts[2]], "xzy", "zdown")

    #utils.addTwistJnts(foreArmSplitNum, "L_arm02_skinJnt", "L_hand01_skinJnt")

    ######### Finger #########

    fingers = ['pinky', 'ring', 'middle', 'index', 'thumb']
    tJntGrp = 'L_hand01_skinJnt'
    for finger in fingers:
        proxy_fingers = pm.ls("L_%s_*_loc" % finger)
        if len(proxy_fingers) == 0:
            log_debug('no fingers found %s' % finger)
            continue
        finger_proxy_names = []
        finger_rig_names = []
        s = 1
        if (finger is 'pinky') or (finger is 'ring'):
            log_debug('it is cupfinger %s' % finger)
            finger_proxy_names.append('L_%sCup_loc' % finger)
            finger_rig_names.append('L_%sCup_skinJnt' % finger)

        for i in range(len(proxy_fingers)):
            finger_proxy_names.append("L_%s_%02d_loc" % (finger, int(i) + 1))
            finger_rig_names.append("L_fng%s%02d_skinJnt" % (finger.capitalize(), int(i) + 1))
        # make joints
        aFingerJnts = duplicateJointHierarchy(
            finger_proxy_names,
            finger_rig_names,
            tJntGrp)

        orientJoints(aFingerJnts, "xyz", "zdown")
    
    # mirror jnts
    pm.mirrorJoint(aJnts[0], mirrorBehavior=0, searchReplace=("L_", "R_"))
    log_debug('Done skeletonProxy arm')

    ######### Leg #########
    tJntGrp = 'C_pelvis02_skinJntEnd'
    aJnts = duplicateJointHierarchy(
        ["L_leg01_loc", "L_leg02_loc", "L_ankle_loc", "L_ball_loc", "L_toe_loc"],
        ["L_leg01_skinJnt", "L_leg02_skinJnt", "L_foot01_skinJnt", "L_foot02_skinJnt", "L_foot03_skinJntEnd"],
        tJntGrp)

    orientJoints(aJnts, "xzy", "zup")
    zeroJointorient([aJnts[-1]])
    # orient ankle, then other upLeg and knee (different orientations)
    # orientJointBasedOnChildJntPos(aJnts[0], aJnts[1], [0, 0, -1], "xzy", "ydown", "zup")
    # orientJointBasedOnChildJntPos(aJnts[1], aJnts[2], [0, 0, 1], "xzy", "zup", "ydown")

    pm.mirrorJoint(aJnts[0], mirrorBehavior=0, searchReplace=("L_", "R_"))

    # resize joints
    utils.setJointRadiusHierarchy("C_root_jnt", jointRadius)

    log_debug('Done skeletonProxy leg')

    # hide root loc
    rootLocName = "skeleton_proxy_grpLoc"
    pm.setAttr("%s.v"%rootLocName, 0)
    return

def duplicateJointHierarchy(aTargets, aNames, grp):

    # will create joint chain based on location of objects in $aTargets, rename them the names in $aNames, and place the result in the existing group $grp
    # returns new pathNames
    aTargetLen = len(aTargets)
    jnt = ""
    aRet = range(aTargetLen)
    aStr = range(aTargetLen)

    xForm = range(aTargetLen)
    aIsJnt = range(aTargetLen)
    i = 0
    # tracks non joints so they can be aligned after the chain has been created
    if len(aTargets) > len(aNames):
        log_debug('lenght of aTrargets and aNames do not match %s'%(len(aTargets)))
        return aRet

    tLoc = pm.spaceLocator(n="abRTDupJntHierarchy_loc")
    for i in range(0, len(aTargets)):
        if pm.nodeType(aTargets[i]) == "joint":
            aStr = pm.duplicate(aTargets[i], po=1, name=aNames[i])
            # duplicate the joint
            # $aStr = `duplicate -rr -name $aNames[$i] $aTargets[$i]`;
            # $aRel = `listRelatives -c -fullPath $aStr[0]`;
            # if (size($aRel) > 0)
            #  delete $aRel;
            jnt = aStr[0]
            aIsJnt[i] = 1


        else:
            utils.snap(aTargets[i], tLoc)
            xForm = pm.xform(tLoc, q=1, ws=1, t=1)
            jnt = str(pm.joint(p=(xForm[0], xForm[1], xForm[2]), n=aNames[i]))
            aIsJnt[i] = 0

        if i == 0:
            if grp != "" and pm.objExists(grp):
                jnt = pm.parent(jnt, grp)[0].fullPath()


            elif pm.listRelatives(jnt, parent=1) != []:
                jnt = pm.parent(jnt, w=1)[0].fullPath()
        else:
            jnt = pm.parent(jnt, aRet[i - 1])[0].fullPath()

        log_debug('jnt is %s'%jnt)
        log_debug('aRet is %s' % aRet)
        aRet[i] = jnt

    pm.delete(tLoc)
    for i in range(0, len(aIsJnt)):
        if not aIsJnt[i]:
            pm.joint(aRet[i], sao='zup', zso=1, e=1, oj='xzy')

    pm.select(clear=1)
    return aRet

def zeroJointorient(aJnts):
    for aJnt in aJnts:
        pm.setAttr('%s.jointOrientX' % aJnt, 0)
        pm.setAttr('%s.jointOrientY' % aJnt, 0)
        pm.setAttr('%s.jointOrientZ' % aJnt, 0)

def orientJoints(aJnts, orient, sao):
    jnt = ""
    aRel = []
    # orients joints.  $orient is value of joint -orientJoint ("xzy") and $sao is value of joint -sao ("zup")
    for jnt in aJnts:
        aRel = pm.listRelatives(jnt, c=1, type='joint')
        if len(aRel) > 0:
            pm.xform(jnt, ro=(0, 0, 0))
            pm.joint(jnt, sao=sao, orientJoint=orient, e=1)


def orientJointBasedOnChildJntPos(jnt, childJnt, aXyzCond, orient, trueSecOrient, falseSecOrient):
    i = 0
    condVal = 0
    # orients $jnt based on child ($childJnt) worldspace position
    # $aXyzCond is x, y, and z values (must have 3 values) of -1, 0, or 1.  If value is:
    # 0 -- ignored
    # 1 -- value of parent ($jnt) must be greater than that of the child ($childJnt) for successOrient to be applied
    # -1 -- value of parent ($jnt) must be less that the child ($childJnt) for successOrient to be applied
    # $orient is primary orient of joint ("xyz", etc)
    # $trueSecOrient and $falseSecOrient are both values taken by joint -sao flag ("yup", "xdown", etc)
    aJntTrans = []
    aChildTrans = []
    sao = ""
    condVal = int(True)
    # return if $aXyzCond is not the right length or has no comparison values
    if len(aXyzCond) < 3:
        return

    if aXyzCond[0] == 0 and aXyzCond[1] == 0 and aXyzCond[2] == 0:
        return

    aJntTrans = pm.joint(jnt, q=1, a=1, position=1)
    aChildTrans = pm.joint(childJnt, q=1, a=1, position=1)
    for i in range(0, 3):
        if aXyzCond[i] == 1:
            if aJntTrans[i] < aChildTrans[i]:
                condVal = int(False)
                # try and prove it wrong
                break
        elif aXyzCond[i] == -1:
            if aJntTrans[i] > aChildTrans[i]:
                condVal = int(False)
                # try and prove it wrong
                break

    sao = str((condVal))
    sao and trueSecOrient or falseSecOrient
    pm.joint(jnt, sao=sao, orientJoint=orient, e=1)




def makeSpine(spineTemplateJnts, spineSkinJntNum, parentTo='C_root_jnt'):

    # creates spine skinJoints from template joints
    # $aSpineRigCtrlJnts = joints on base skeleton to which the spline curve clusters will be parented (no shaper, will be added in this fn)
    # $aSpineRigCtrlJnts = {$hipJnt, $rootJnt, $midJnt1, [$midJnt2, $midJnt3, ...], $hiJnt, $endJnt}
    # $spineJntNum is number of spine jnts to create

    aStr=[]
    aTrans=[]

    spineCurveGrp =str(pm.group(em=1,name="C_spineCrv_grp"))

    tLoc = pm.spaceLocator(name="skeletonizeTemp_loc")
    curveStr="curve -d 2"

    for i in range(0, len(spineTemplateJnts)):
        utils.snap(spineTemplateJnts[i], tLoc)
        aTrans=pm.xform(tLoc, q=1,ws=1,t=1)
        curveStr+=" -p " + str(aTrans[0]) + " " + str(aTrans[1]) + " " + str(aTrans[2])

    curveStr+=" -n " + "C_ikSpline_crv"
    spineCurve=str(pm.mel.eval(curveStr))
    # parent curve
    spineCurve=str(pm.parent(spineCurve, spineCurveGrp)[0])
    pm.delete(tLoc)

    pm.select(clear=1)

    aSpineJntNames=[]
    # fill aSpineJntNames
    #int $spineJntNum = int(abRTGetGlobal("spineJntNum"));

    for i in range(0,spineSkinJntNum - 1):
        aSpineJntNames.append("C_spine%02d_skinJnt"%(i+1))

    #aSpineJntNames.append("C_chest01_skinJnt")
    log_debug('rebuilding Curve with %s divisions'%spineSkinJntNum)
    aStr=pm.rebuildCurve(spineCurve,
        rt=0,ch=1,end=1,d=spineSkinJntNum,kr=0,s=0,kcp=0,tol=0.01,kt=0,rpo=0,kep=1)

    # create spine joints
    rebuiltSpineCurve=aStr[0]


    aRigSpineJnts= makeSpineJntsFromCurve(rebuiltSpineCurve, aSpineJntNames, parentTo, False)
    pm.delete(rebuiltSpineCurve)
    # orient and parent
    orientJoints(aRigSpineJnts, "xzy", "zup")
    
    # zero out last joint orient
    utils.zeroJointOrient(aSpineJntNames[-1])

    pm.parent(aRigSpineJnts[0], parentTo)

    return aSpineJntNames