import pymel.core as pm
globalPrefs = {}

def initGlobals():
    global globalPrefs
    globalPrefs = {}
    globalPrefs["skeletonName"] = "skeleton"
    globalPrefs["leftPrefix"] = "L_"
    globalPrefs["rightPrefix"] = "R_"
    globalPrefs["name"] = "human"
    
    globalPrefs["avgHeight"] = "183" # units in avg height -- used to determine scale {183~6'0")
    globalPrefs["deleteMeGrp"] = "deleteMeWhenDone" # name of group to put temp rig building transforms in
    globalPrefs["ctrlDir"] = "ctrl_grp" # name of group to put control curves in
    globalPrefs["versionNum"] = "1.0" # script version number
    globalPrefs["premiumVersion"] = "1"
    globalPrefs["deleteRigCreatedBindPoses"] = "0" # if true, bindPoses created during the rigging process will be deleted

    globalPrefs["eyeCtrlOffset"] = "40" # eye ctrl offset from eye jnts
    globalPrefs["zeroFreezeGroupSuffix"] = "zeroFrzGrp" # zero group freeze naming suffix (no other nodes will end with this suffix)
    globalPrefs["includeHeadNeckTransAtts"] = "1" # show the fk (trans and useRootSpace) options on head and neck controls
    globalPrefs["createIkFingerCtrls"] = "1" # add IK controls to finger rig
    globalPrefs["alignHandIkToWorld"] = "1" # align the hand IK controls to the world axes
    globalPrefs["alignCtrlCrvsToSpine"] = "0" # align top two spine control curves to the spine
    globalPrefs["footIKCtrlAtAnkle"] = "1" # foot IK control rotates around the heel or the ankle
    globalPrefs["createLimbWtJntsInHierarchy"] = "1" # if true, limb weight joints will be created in a hierarchical chain;  otherwise, they'll be separate and apart
     
    # scaling
    globalPrefs["globalScale"] = "1"
    globalPrefs["jointRadius"] = "0.4"
    globalPrefs["ctrlSize"] = "1"

    # proxy skeleton
    globalPrefs["spineCtrlNum"] = "3" 
    globalPrefs["neckNum"] = "1" 
    globalPrefs["fingerNum"] = "5" # default number of weightSpineJnts
    globalPrefs["toeNum"] = "1" # default number of weightSpineJnts

    # skeleton maker
    globalPrefs["spineJntNum"] = "8" # default number of weightSpineJnts
    globalPrefs["addSpineShaper"] = "0" # enable to add a spine shaper to the spine control curves

    globalPrefs["autoSaveSkeleton"] = "1"
    globalPrefs["autoMirror"] = "1" # autoMirror rigs on creation (legs, arms, hands)
    globalPrefs["proxyLocScale"] = ".7" # size of locs on proxy skeleton
    globalPrefs["lockProxyCtlAxes"] = "1" # lock proxy control axes
    globalPrefs["legMirrorBehavior"] = "1" # if true, the leg joints will be mirrored using behavior, otherwise will be mirrored using orientation
    globalPrefs["useBonesForProxyDisplay"] = "1" # if true, the proxy will be connected with bones instead of lines
    globalPrefs["thumbCurlSpreadRoll"] = "zyx" # axes for thumb curl, spread and roll
    globalPrefs["fingerCurlSpreadRoll"] = "yzx" # axes for finger curl, spread and roll
    globalPrefs["fingerCupAxis"] = "y" # axis for finger cup joints
    globalPrefs["reverseFingerCurl"] = "0" # true if handJoints have been mirrored without -mirrorBehavior (pre 2.0 skeletons), otherwise false
    
    # split joints
    globalPrefs["upArmSplitNum"] = "1" 
    globalPrefs["foreArmSplitNum"] = "2"
    globalPrefs["upLegSplitNum"] = "1"
    globalPrefs["lowLegSplitNum"] = "1"
    globalPrefs["legMirrorBehavior"] = "1"

    # colors
    globalPrefs["ikJntColor"] = "28"
    globalPrefs["fkJntColor"] = "18"
    globalPrefs["lfCtrlColor"] = "6"
    globalPrefs["rtCtrlColor"] = "13"
    globalPrefs["ctrCtrlColor"] = "17"
    globalPrefs["ctrMasterCtrlColor"] = "21"
    globalPrefs["cogCtrlColor"] = "16"
    globalPrefs["rootCtrlColor"] = "3"
    globalPrefs["lfFingerCtrlColor"] = "6"
    globalPrefs["rtFingerCtrlColor"] = "13"
    globalPrefs["masterCtrlColor"] = "23"
    globalPrefs["subMasterCtrlColor"] = "26"


    # marking menu
    globalPrefs["bakeFingersToFkCtrls"] = "1" # bake masterFinger control rotations to FK controls if true, otherwise move them to hand control finger atts
    globalPrefs["filterBySkeletonType"] = "1" # if true, items in the Simple Skeleton UI Guide Skel and Simple skel option menus will be filtered by type (using a root att on the simple skeleton)

    # rubberhose limbs
    globalPrefs["rubberHoseLegs"] = "1" # create rubberhose legs
    globalPrefs["rhUpLegCtrlNum"] = "1" # number of controls on the upLeg rubberhose
    globalPrefs["rhLowLegCtrlNum"] = "1" # number of controls on the lowLeg rubberhose
    globalPrefs["rubberHoseArms"] = "1" # create rubberhose arm
    globalPrefs["rhUpArmCtrlNum"] = "1" # number of controls on the upArm rubberhose
    globalPrefs["rhForeArmCtrlNum"] = "2" # number of controls on the foreArm rubberhose
    globalPrefs["rhMidJointInitRibbonKnotOffset"] = ".015" # offset (in cm) of mid limb softness joints on either side of the mid joint
    globalPrefs["rhUseRivet"] = "1" # if true, RH limbs will use rivet (instead of follicles) to attach joints to the ribbon

    # squash and stretch
    globalPrefs["squashStretchSpine"] = "1"
    globalPrefs["squashStretchLegs"] = "1"
    globalPrefs["squashStretchArms"] = "1"

    # split joint values
    globalPrefs["upLegSpltBlndSettings"] = "0.4,1.0,2,0,1" # start value, end value, blendType, blend from second value, blend to next to last value
    globalPrefs["dnLegSpltBlndSettings"] = "0.0,1.0,6,1,1"
    globalPrefs["upArmSpltBlndSettings"] = "0.4,1.0,2,0,1"
    globalPrefs["dnArmSpltBlndSettings"] = "0.0,1.0,6,1,1"
    # used for reseting split weight vars to default
    globalPrefs["initUpLegSpltBlndSettings"] = globalPrefs["upLegSpltBlndSettings"]
    globalPrefs["initDnLegSpltBlndSettings"] = globalPrefs["dnLegSpltBlndSettings"]
    globalPrefs["initUpArmSpltBlndSettings"] = globalPrefs["upArmSpltBlndSettings"]
    #globalPrefs["initDnArmSpltBlndSettings"] = globalPrefs["dnArmSpltBlndSettings"]
    # maya version num
    globalPrefs["mayaVersionNum"] = str(pm.mel.match("[0-9]*$", pm.about(v=1)))

