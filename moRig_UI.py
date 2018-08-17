import pymel.core as pm
import moRig_skeletonTemplate as skelTemp
import moRig_settings as settings
reload(skelTemp)
reload(settings)
settings.initGlobals()
moInit = True


'''
import moRig_UI as moRig_UI
reload(moRig_UI)
moRig_UI.skeletonMakerUI()


def abAutoRig():
    vNum = "Premium"
    versionName = "Premium"
    str = ""
    pm.mel.moDisableProblemFeatures(True)
    if pm.window('moWin', exists=1):
        pm.deleteUI('moWin', window=1)

    winW = 384
    if pm.windowPref('moWin', ex=1):
        pm.windowPref('moWin', e=1, w=winW)

    pm.window('moWin', minimizeButton=False, maximizeButton=False, h=445, t=("abAutoRig " + versionName + " " + vNum),
              w=winW, menuBar=True)

    # autoMirror = int(int(getGlobal("autoMirror")))
    # rhUseRivet = int(int(getGlobal("rhUseRivet")))
    #
    # pm.menu(postMenuCommand=lambda *args: pm.mel.moOptionsOpMn(), label="Options")
    # pm.menuItem('moAutoMirMnIt', checkBox=autoMirror,
    #             command=lambda *args: pm.mel.moToggleMenuItem("moAutoMirMnIt", "autoMirror"), label="Auto Mirror")
    # pm.menuItem('moRHUseRivetMnIt', checkBox=rhUseRivet,
    #             ann="If enabled, limb control joints will be attached to the ribbon using the \"rivet.mel\" script (which must exist in your script path), otherwise follicles will be used (which, due to a Maya bug, can flip when the upper joint is rotated exactly ninety degrees).",
    #             en=(pm.mel.exists("rivet.mel")),
    #             command=lambda *args: pm.mel.moToggleMenuItem("moRHUseRivetMnIt", "rhUseRivet"),
    #             label="Use \"Rivet.mel\" To Attach RH Joints To Ribbon")
    # pm.menuItem(p='moOptionsOpMn', divider=True)
    # pm.menuItem(command=lambda *args: pm.mel.moSplitJointDefaultsUI(0), label="Set Split Joint Weight Defaults")
    # pm.menuItem(command=lambda *args: [
    #     pm.mel.moSetGlobal("upLegSpltBlndSettings", getGlobal("initUpLegSpltBlndSettings")),
    #     pm.mel.moSetGlobal("dnLegSpltBlndSettings", getGlobal("initDnLegSpltBlndSettings")),
    #     pm.mel.moSetGlobal("upArmSpltBlndSettings", getGlobal("initUpArmSpltBlndSettings")),
    #     pm.mel.moSetGlobal("dnArmSpltBlndSettings", getGlobal("initDnArmSpltBlndSettings"))],
    #             label="Revert To Default Split Weight Settings")
    # pm.menuItem(p='moOptionsOpMn', divider=True)
    # pm.menuItem('moHandOptionsMnIt', sm=True, label="Hand Options")
    # str = str(getGlobal("thumbCurlSpreadRoll"))
    # pm.menuItem('moThumbCurlSpreadRollMnIt', p='moHandOptionsMnIt', sm=True, label="Thumb Curl Spread Roll Axes")
    # pm.radioMenuItemCollection()
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "xyz"),
    #             l="xyz", rb=(str == "xyz"))
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "yzx"),
    #             l="yzx", rb=(str == "yzx"))
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "zxy"),
    #             l="zxy", rb=(str == "zxy"))
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "xzy"),
    #             l="xzy", rb=(str == "xzy"))
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "yxz"),
    #             l="yxz", rb=(str == "yxz"))
    # pm.menuItem(p='moThumbCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("thumbCurlSpreadRoll", "zyx"),
    #             l="zyx", rb=(str == "zyx"))
    # pm.setParent('..')
    # str = str(getGlobal("fingerCurlSpreadRoll"))
    # pm.menuItem('moFingerCurlSpreadRollMnIt', p='moHandOptionsMnIt', sm=True, label="Finger Curl Spread Roll Axes")
    # pm.radioMenuItemCollection()
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "xyz"),
    #             l="xyz", rb=(str == "xyz"))
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "yzx"),
    #             l="yzx", rb=(str == "yzx"))
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "zxy"),
    #             l="zxy", rb=(str == "zxy"))
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "xzy"),
    #             l="xzy", rb=(str == "xzy"))
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "yxz"),
    #             l="yxz", rb=(str == "yxz"))
    # pm.menuItem(p='moFingerCurlSpreadRollMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCurlSpreadRoll", "zyx"),
    #             l="zyx", rb=(str == "zyx"))
    # pm.setParent('..')
    # str = str(getGlobal("fingerCupAxis"))
    # pm.menuItem('moFingerCupAxisMnIt', p='moHandOptionsMnIt', sm=True, label="Finger Cup Axis")
    # pm.radioMenuItemCollection()
    # pm.menuItem(p='moFingerCupAxisMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCupAxis", "x"), l="x",
    #             rb=(str == "x"))
    # pm.menuItem(p='moFingerCupAxisMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCupAxis", "y"), l="y",
    #             rb=(str == "y"))
    # pm.menuItem(p='moFingerCupAxisMnIt', c=lambda *args: pm.mel.moSetGlobal("fingerCupAxis", "z"), l="z",
    #             rb=(str == "z"))
    # pm.setParent('..')
    # pm.menuItem(p='moHandOptionsMnIt', divider=True)
    # pm.menuItem('moReverseFingerCurlMnIt', cb=(int(getGlobal("reverseFingerCurl"))),
    #             c=lambda *args: pm.mel.moSetGlobal("reverseFingerCurl",
    #                                                  (1 - int(getGlobal("reverseFingerCurl")))),
    #             l="Reverse Right Curl", p='moHandOptionsMnIt')
    # pm.setParent('..')
    # pm.menuItem(p='moOptionsOpMn', divider=True)
    # pm.menuItem(p='moOptionsOpMn',
    #             ann="Update the UI with values for the currently selected character, specified by the Char Name field in the \"Start\" tab.",
    #             command=lambda *args: [pm.mel.moCheckUIItems(""), pm.mel.moGuessUIItems(),
    #                                    pm.tabLayout('moTabLayout', selectTabIndex=(
    #                                        pm.tabLayout('moTabLayout', q=1, selectTabIndex=1)), e=1)],
    #             label="Refresh UI")
    # pm.menu(postMenuCommand=lambda *args: pm.mel.moDisableProblemFeatures(False), label="Tools")
    # pm.menuItem(
    #     ann="Select all of the control curves for a character.  Select any one of your character control curves first.",
    #     command=lambda *args: pm.mel.moSelectAllCharControls(), label="Select All Character Controls")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Create a skeleton.", command=lambda *args: pm.mel.moSkeletonMaker(), label="Skeleton Maker")
    # pm.menuItem(command=lambda *args: pm.mel.moRigRemover(), label="Rig Remover")
    # pm.menuItem(
    #     ann="Create a strictly hierarchical skeleton which can be constrained to your rig.  Useful for importing your character into some game engines.",
    #     command=lambda *args: pm.mel.moSimpleSkeletonUI(), label="Simple Skeleton Creator")
    # # menuItem -label "Skeleton Updater" -ann "A tool to convert the older skeleton limbs and split joints to the type used by the current rig.  All old joints will be unbound from any skinClusters and their weights copied to the new joints." -command "moUpdateSkeletonSplitsJointsUI();";
    # pm.menuItem(ann="Install the abAutoRig Character Marking Menu on any available hotkey.",
    #             command=lambda *args: pm.mel.moInstallCharacterMMUI(), label="Install Character Marking Menu")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Find abAutoRig nodes with clashing names in the current scene.",
    #             command=lambda *args: pm.mel.moRemoveNameClashes(False), label="Find Clashing Nodes")
    # pm.menuItem(ann="Rename any nodes associated with the rig with identical names.",
    #             command=lambda *args: pm.mel.moRemoveNameClashes(True), label="Rename Clashing Nodes")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="A UI to help select the joints on your skeleton to which you can bind your character mesh.",
    #             command=lambda *args: pm.mel.moSelWeightJntsUI(), label="Weight Joint Selector")
    # pm.menuItem(
    #     ann="A UI to help quickly set the twist contributions of multiple upLimb split joints by specifying the first and last joint twist amounts.  Select a character control curve first.  Hold control for advanced options.",
    #     command=lambda *args: pm.mel.moSplitJointWeighterUI(), label="Split Joint Weight Tool")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Simple joint orient tool for rotating LRAs in 90 degree increments.",
    #             command=lambda *args: pm.mel.moRotateOrientUI(), label="Joint Orient Rotation Tool")
    # pm.menuItem(ann="Change the rotation order of controls that have already been animated.",
    #             command=lambda *args: pm.mel.moChangeRotOrderWindow(), label="Change Rotation Order Tool")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Add a stretchy spline to your character.",
    #             command=lambda *args: pm.mel.moMakeStretchySplineWin(), label="Stretchy Spline From Curve")
    # pm.menuItem(divider=True)
    # pm.menuItem(
    #     ann="Save your rig control curve shapes and colors to a shelf button.  Select a character control curve first.",
    #     command=lambda *args: pm.mel.moWireReplaceUI(), label="Wire Replacer")
    # pm.menuItem(ann="Change the colors of your rig control curves.  Select a character control curve first.",
    #             command=lambda *args: pm.mel.moColorCtrlUI(), label="Wire Color Control")
    # pm.menuItem(
    #     ann="Save your modified wires to a shelf button for later recall.  Select any one of your character control curves first.",
    #     command=lambda *args: pm.mel.moCaptureControlCurves(), label="Save Wires To Shelf")
    # pm.menuItem(divider=True)
    # pm.menuItem(
    #     ann="Creates a character set for all of your character's animatable attributes.  Select any one of your character control curves first.",
    #     command=lambda *args: pm.mel.moMakeCharSetFromSel(), label="Quick Create Character Set")
    # pm.menuItem(
    #     ann="Creates a node for use with the abxPicker script.  Select any one of your character control curves first.",
    #     command=lambda *args: pm.mel.moMakeAbxPickerUI(), label="Make abxPicker Character Sheet")
    # pm.menuItem(divider=True)
    # pm.menuItem(
    #     ann="Displays a simple UI that allows you to snap to FK or IK on limbs associated with the selected controls.  Hold Ctrl(Command)+Shift and click this menu item to create a shelf button.",
    #     command=lambda *args: pm.mel.moMakeFKIKSnapBn(False), label="Show IK/FK Snap UI")
    # pm.menuItem(
    #     ann="Displays a simple UI that allows you to toggle between IK and FK on limbs associated with the selected controls.  Hold Ctrl(Command)+Shift and click this menu item to create a shelf button.",
    #     command=lambda *args: pm.mel.moMakeFKIKSnapBn(True), label="Show IK/FK Toggle UI")
    # # menuItem -divider true;
    # # menuItem -label "Unstickify IK Limb" -ann "For use on IK limbs that lock before solving all the way (sometimes the result of re-rigging with a different number of split joints).  Select a control curve on the selected limb and click this menu item.  You can also click the this menu item with nothing selected to unstickify all of the IK limbs in the current scene." -command "moUnStickifyIKLimb();";
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Switch spaces on a selected control while maintaining its position in worldSpace.",
    #             command=lambda *args: pm.mel.moSpaceSwitcherUI(), label="Space Switcher")
    # pm.menuItem(ann="Match the position of controls between space switches.",
    #             command=lambda *args: pm.mel.moSpaceSwitchWindow(), label="Space Switch Matcher")
    # pm.menuItem(
    #     ann="Change the position of the root, worldSpace and/or COG controls relative to the rig.  Use this to change how the rig pivots around the rootCtrl, worldSpacePivotCtrl, and cogCtrl.",
    #     command=lambda *args: pm.mel.abMovePivotCtrlsUI(), label="Move Cog, Root, Or WorldSpace Controls")
    # pm.menuItem(ann="A UI that allows you to easily add new spaces to your rig controls.",
    #             command=lambda *args: pm.mel.moAddSpaceToCtrlUI(), label="Add A New Control Space")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Mirror a character's pose.", command=lambda *args: pm.mel.moMirrorPoseUI(),
    #             label="Mirror Pose Tool")
    # pm.menuItem(divider=True)
    # pm.menu(postMenuCommand=lambda *args: pm.mel.DUMMY(), label="Reset Pose")
    # pm.menuItem(ann="Reset a character to its default pose.  Select any one of your character control curves first.",
    #             command=lambda *args: pm.mel.moResetCharPose(1), label="Reset Character to Default Pose")
    # pm.menuItem(
    #     ann="Reset selected control curves to their default pose.  Highlight entries in the ChannelBox to revert selected attributes.",
    #     command=lambda *args: pm.mel.moResetCharPose(0), label="Reset Selected Control Curves to Default")
    # pm.menuItem(divider=True)
    # pm.menuItem(ann="Reset a character to its proxy pose if it wasn't a traditional T-Pose.",
    #             command=lambda *args: pm.mel.moSetRigToSavedProxyPose(), label="Reset Character to Proxy Pose")
    # pm.menuItem(divider=True)
    # pm.menuItem(
    #     ann="Group freeze all of the selected character's controls so that the current pose will become the character's default pose (Create Zero Freeze Groups).",
    #     command=lambda *args: pm.mel.moSetBasePose(1), label="Set Current Pose As Default")
    # pm.menuItem(ann="Reset the Zero Freeze Groups so that the build pose will become the character's default pose.",
    #             command=lambda *args: pm.mel.moSetBasePose(0), label="Restore Build Pose As Default")
    # pm.menuItem(
    #     ann="Remove all Zero Freeze Groups from the selected character.  The build pose will be restored as the character's default pose.",
    #     command=lambda *args: pm.mel.moSetBasePose(-1), label="Remove Zero Pose Freeze Groups")
    # pm.menu(postMenuCommand=lambda *args: pm.mel.DUMMY(), label="Help")
    # pm.menuItem(command=lambda *args: pm.showHelp("http://www.supercrumbly.com/archive/post/abAutoRig_II", a=1),
    #             label="Online Help")
    # pm.menuItem(divider=True)
    # pm.menuItem(command=lambda *args: pm.showHelp(
    #     "http://www.supercrumbly.com/updatecheck.php?script=abAutoRig_II&userver= + vNum + &prem= + str(getGlobal(premiumVersion)) + ",
    #     a=1), label="Check For Updates")
    lmargin = 3
    rmargin = 3
    lCol = 70
    lSliderCol = 130
    rSliderCol = lmargin
    cCol = 100
    rCol = 60
    pm.formLayout('moForm', numberOfDivisions=100)
    pm.tabLayout('moTabLayout', innerMarginHeight=0, innerMarginWidth=0)
    # start form
    pm.formLayout('moStartTabForm', numberOfDivisions=cCol)
    pm.textFieldGrp('moNameTxFldGrp', columnWidth2=(lCol, cCol), text=(getGlobal("name")),
                    adjustableColumn2=2, cc=lambda *args: pm.mel.moServiceNameFld(), label="Char Name:")
    pm.popupMenu('moCharNamePopUpMn', postMenuCommand=lambda *args: pm.mel.moServiceNameFldPopUp(), button=3,
                 p='moNameTxFldGrp')
    pm.textFieldButtonGrp('moMasterScaleJntTxFldBnGrp', ed=False, manage=False, text="", label="Master Scale Jnt:")
    # used to determine if masterscale has been set for a skeleton
    pm.button('moCreateSkeletonBn', h=28, c=lambda *args: [pm.mel.moClearUIItems(), pm.mel.moSkeletonMaker()],
              label="Create a Skeleton")
    # spine form
    pm.setParent('..')
    name = getGlobal("name")

    pm.formLayout('moSpineTabForm', numberOfDivisions=cCol)
    pm.intSliderGrp('moSpineJntsIntSldrGrp', adjustableColumn3=3, min=4,
                    cc=lambda *args: setGlobal("spineJntNum",
                                                          pm.intSliderGrp('moSpineJntsIntSldrGrp', q=1, v=1)), max=18,
                    ann="Select the number of joints you want on the ik spine.", label="Spine Joints:", field=True,
                    v=(int(getGlobal("spineJntNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.textFieldButtonGrp('moSpineRootTxFldBnGrp', adjustableColumn3=2,
                          bc=lambda *args: pm.mel.moServiceUI("spineRoot"), ed=False,
                          ann="Select the root spine joint.", label="Spine Root:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moHipTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("hip"),
                          ed=False, ann="Select the hip joint.", label="Hip:", text="", columnWidth3=(lCol, cCol, rCol),
                          buttonLabel=" Select ")
    pm.textFieldButtonGrp('moRootCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Root Ctrl:")
    pm.textFieldButtonGrp('moHipCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Hip Ctrl:")
    pm.textFieldButtonGrp('moCogCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Cog Ctrl:")
    pm.textFieldButtonGrp('moLowSpineCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Low Spine Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_1TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 1 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_2TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 2 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_3TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 3 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_4TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 4 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_5TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 5 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_6TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 6 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_7TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 7 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_8TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 8 Ctrl:")
    pm.textFieldButtonGrp('moMidSpineCtrl_9TxFldBnGrp', ed=False, manage=False, text="", label="Mid Spine 9 Ctrl:")
    pm.textFieldButtonGrp('moHiSpineCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Hi Spine Ctrl:")
    pm.textFieldButtonGrp('moMasterSpineCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Master Spine Ctrl:")
    pm.textFieldButtonGrp('moRigSettingsCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Rig Settings Ctrl:")
    pm.textFieldButtonGrp('moWorldSpaceCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Rig Pivot Ctrl:")
    pm.checkBox('moOrientSpineCtrlsChkBx', cc=lambda *args: setGlobal("alignCtrlCrvsToSpine", 1 - (
        int(getGlobal("alignCtrlCrvsToSpine")))),
                ann="If enabled, the mid and high spine control curves will be oriented to their respective spine joints; otherwise they'll lie on the XZ plane.",
                value=(int(getGlobal("alignCtrlCrvsToSpine"))), label="Align Control Curves to Spine")
    pm.checkBox('moSpineSqStChkBx', cc=lambda *args: setGlobal("squashStretchSpine", 1 - (
        int(getGlobal("squashStretchSpine")))),
                ann="If enabled, the spine will be created with built in squash and stretch attributes.",
                value=(int(getGlobal("squashStretchSpine"))), label="Add Squash And Stretch To Spine")
    pm.checkBox('moAddSpineShaperChkBx', cc=lambda *args: setGlobal("addSpineShaper", 1 - (
        int(getGlobal("addSpineShaper")))),
                ann="Enable to add a spine shaper control between the top two spine control curves.",
                value=(int(getGlobal("addSpineShaper"))), label="Add Spine Shaper Curve")
    pm.button('moCreateSpineBn', h=28, c=lambda *args: pm.mel.moServiceUIButton("createSpine"),
              label="Create Spine Rig")
    # head form
    pm.setParent('..')
    pm.formLayout('moHeadTabForm', numberOfDivisions=cCol)
    pm.textFieldButtonGrp('moNeckTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("neck"),
                          ed=False, ann="Select a neck joint.", label="Neck:", text="", columnWidth3=(lCol, cCol, rCol),
                          buttonLabel=" Select ")
    pm.textFieldButtonGrp('moHeadTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("head"),
                          ed=False, ann="Select the head joint.", label="Head:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moEyeTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("eye"),
                          ed=False, ann="Select an eye joint.", label="Eye:", text="", columnWidth3=(lCol, cCol, rCol),
                          buttonLabel=" Select ")
    pm.checkBox('moIncludeHeadNeckTransAttsChkBx', cc=lambda *args: setGlobal("includeHeadNeckTransAtts", (
                1 - (int(getGlobal("includeHeadNeckTransAtts"))))),
                ann="The actual rig will be unaffected, but the translate and FK channels on the head and neck controls will be locked and hidden.",
                value=(1 - (int(getGlobal("includeHeadNeckTransAtts")))),
                label="Hide Translate on Head/Neck Controls")
    pm.textFieldButtonGrp('moNeck_1TxFldBnGrp', ed=False, manage=False, text="", label="Neck_1:")
    pm.textFieldButtonGrp('moNeck_2TxFldBnGrp', ed=False, manage=False, text="", label="Neck_2:")
    pm.textFieldButtonGrp('moNeck_3TxFldBnGrp', ed=False, manage=False, text="", label="Neck_3:")
    pm.textFieldButtonGrp('moNeck_4TxFldBnGrp', ed=False, manage=False, text="", label="Neck_4:")
    pm.textFieldButtonGrp('moNeck_1_CtrlTxFldBnGrp', ed=False, manage=False, text="", label="Neck_1 Ctrl:")
    pm.textFieldButtonGrp('moNeck_2_CtrlTxFldBnGrp', ed=False, manage=False, text="", label="Neck_2 Ctrl:")
    pm.textFieldButtonGrp('moNeck_3_CtrlTxFldBnGrp', ed=False, manage=False, text="", label="Neck_3 Ctrl:")
    pm.textFieldButtonGrp('moNeck_4_CtrlTxFldBnGrp', ed=False, manage=False, text="", label="Neck_4 Ctrl:")
    pm.textFieldButtonGrp('moNeckCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Neck Ctrl:", eb=False)
    pm.textFieldButtonGrp('moHeadCtrlTxFldBnGrp', ed=False, manage=False, text="", label="Head Ctrl:", eb=False)
    pm.textFieldButtonGrp('moJawTxFldBnGrp', ed=False, manage=False, text="", label="Jaw:")
    # head s&s button
    pm.button('mocreateHeadSqStrBn',
              ann="Add squash and stretch to an existing head rig.  Select at least one of your character control curves first.",
              c=lambda *args: pm.mel.moHeadSquashAndStretchSelectUI(), label=" Add Squash And Stretch To Head ")
    pm.button('moCreateHeadBn', h=28, c=lambda *args: pm.mel.moServiceUIButton("createHead"),
              label="Create Head Rig")
    # leg form
    pm.setParent('..')
    pm.formLayout('moLegTabForm', numberOfDivisions=cCol)
    pm.textFieldButtonGrp('moUpLegTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("upLeg"),
                          ed=False, label="UpLeg:", text="", columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moToeTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("toe"),
                          ed=False, label="Toe:", text="", columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.intSliderGrp('moUpLegSpltIntSldrGrp', adjustableColumn3=3, min=0, cc=lambda *args: [
        setGlobal("upLegSplitNum", pm.intSliderGrp('moUpLegSpltIntSldrGrp', q=1, v=1)),
        pm.mel.moServiceUIButton("legSplitJointSlider")], max=6, label="UpLeg Split Joints:", field=True,
                    v=(int(getGlobal("upLegSplitNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.intSliderGrp('moLowLegSpltIntSldrGrp', adjustableColumn3=3, min=0, cc=lambda *args: [
        setGlobal("lowLegSplitNum", pm.intSliderGrp('moLowLegSpltIntSldrGrp', q=1, v=1)),
        pm.mel.moServiceUIButton("legSplitJointSlider")], max=6, label="LowerLeg Split Joints:", field=True,
                    v=(int(getGlobal("lowLegSplitNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.textFieldButtonGrp('moHeelLocTxFldBnGrp', adjustableColumn3=2,
                          bc=lambda *args: pm.mel.moServiceUI("heelLoc"), ed=False, label="Heel Loc:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.button('mocreateHeelLocBn', c=lambda *args: pm.mel.moMakeHeelLoc(), label=" Create Heel Locator ")
    pm.checkBox('moCreateBothHeelLocChkBx', value=1, label="Create Mirror Loc")
    rhLegs = 0
    enRhLegOptions = 0
    enRhLegsBn = 0
    rhLegs = int(int(getGlobal("rubberHoseLegs")))
    if (pm.intSliderGrp('moUpLegSpltIntSldrGrp', q=1, v=1)) > 0 and (
    pm.intSliderGrp('moLowLegSpltIntSldrGrp', q=1, v=1)) > 0:
        enRhLegOptions = rhLegs
        enRhLegsBn = int(True)


    else:
        enRhLegsBn = enRhLegOptions = int(False)

    pm.text('moSetLegSpltJntWtVarsTxt', align="right", l="Split Joint Weights:")
    pm.button('moSetUpLegSpltJntWtVarsBn', c=lambda *args: pm.mel.moSplitJointDefaultsUI(-1),
              l=" Set UpLeg Weights ")
    pm.button('moSetLowLegSpltJntWtVarsBn', c=lambda *args: pm.mel.moSplitJointDefaultsUI(-2),
              l=" Set LowLeg Weights ")
    pm.checkBox('moCreateRubberHoseLegsChkBx', cc=lambda *args: [
        setGlobal("rubberHoseLegs", 1 - (int(getGlobal("rubberHoseLegs")))),
        pm.mel.moServiceUIButton("legRubberHoseBn")], en=enRhLegsBn, value=rhLegs, label="Build Rubberhose (RH) Legs")
    pm.checkBox('moLegsSqStChkBx', cc=lambda *args: setGlobal("squashStretchLegs", 1 - (
        int(getGlobal("squashStretchLegs")))),
                ann="If enabled, the rubber hose legs will be created with built in squash and stretch attributes.",
                en=enRhLegOptions, v=(int(getGlobal("squashStretchLegs"))), label="Add Squash And Stretch")
    pm.intSliderGrp('moUpLegRhCtrlNumIntSldrGrp', en=enRhLegOptions, min=0,
                    cc=lambda *args: setGlobal("rhUpLegCtrlNum",
                                                          pm.intSliderGrp('moUpLegRhCtrlNumIntSldrGrp', q=1, v=1)),
                    max=6, label="UpLeg RH Controls:", field=True, adjustableColumn3=3,
                    v=(int(getGlobal("rhUpLegCtrlNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.intSliderGrp('moLowLegRhCtrlNumIntSldrGrp', en=enRhLegOptions, min=0,
                    cc=lambda *args: setGlobal("rhLowLegCtrlNum",
                                                          pm.intSliderGrp('moLowLegRhCtrlNumIntSldrGrp', q=1, v=1)),
                    max=6, label="LowerLeg RH Controls:", field=True, adjustableColumn3=3,
                    v=(int(getGlobal("rhLowLegCtrlNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.checkBox('moFootIKCtrlAtAnkleChkBx', cc=lambda *args: setGlobal("footIKCtrlAtAnkle", 1 - (
        int(getGlobal("footIKCtrlAtAnkle")))),
                ann="If enabled, the foot IK control will rotate the foot around the ankle instead of the heel.",
                value=(int(getGlobal("footIKCtrlAtAnkle"))), label="Center Foot IK Control On Ankle")
    pm.textFieldButtonGrp('moLfLegIkCtrlTxFldBnGrp', ed=False, manage=False, text="", label="LfLegIkCtrl:", eb=False)
    pm.textFieldButtonGrp('moRtLegIkCtrlTxFldBnGrp', ed=False, manage=False, text="", label="RtLegIkCtrl:", eb=False)
    # toe value holders
    pm.textFieldButtonGrp('moLfToeTxFldBnGrp', ed=False, manage=False, text="", label="LfToe:", eb=False)
    pm.textFieldButtonGrp('moLfNoRotToeTxFldBnGrp', ed=False, manage=False, text="", label="LfNoRotToe:", eb=False)
    pm.textFieldButtonGrp('moLfBigToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="LfBigToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moLfLongToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="LfLongToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moLfMiddleToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="LfMiddleToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moLfRingToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="LfRingToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moLfPinkyToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="LfPinkyToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moRtToeTxFldBnGrp', ed=False, manage=False, text="", label="RtToe:", eb=False)
    pm.textFieldButtonGrp('moRtNoRotToeTxFldBnGrp', ed=False, manage=False, text="", label="RtNoRotToe:", eb=False)
    pm.textFieldButtonGrp('moRtBigToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="RtBigToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moRtLongToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="RtLongToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moRtMiddleToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="RtMiddleToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moRtRingToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="RtRingToeRollBreak:", eb=False)
    pm.textFieldButtonGrp('moRtPinkyToeRollBreakTxFldBnGrp', ed=False, manage=False, text="",
                          label="RtPinkyToeRollBreak:", eb=False)
    pm.button('moCreateLegBn', h=28, c=lambda *args: pm.mel.moServiceUIButton("createLeg"), label="Create Leg Rig")
    # arm form
    pm.setParent('..')
    pm.formLayout('moArmTabForm', numberOfDivisions=cCol)
    pm.textFieldButtonGrp('moUpArmTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("upArm"),
                          ed=False, label="Up Arm:", text="", columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.intSliderGrp('moUpArmSpltIntSldrGrp', adjustableColumn3=3, min=0, cc=lambda *args: [
        setGlobal("upArmSplitNum", pm.intSliderGrp('moUpArmSpltIntSldrGrp', q=1, v=1)),
        pm.mel.moServiceUIButton("armSplitJointSlider")], max=6, label="UpArm Split Joints:", field=True,
                    v=(int(getGlobal("upArmSplitNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.intSliderGrp('moForeArmSpltIntSldrGrp', adjustableColumn3=3, min=0, cc=lambda *args: [
        setGlobal("foreArmSplitNum", pm.intSliderGrp('moForeArmSpltIntSldrGrp', q=1, v=1)),
        pm.mel.moServiceUIButton("armSplitJointSlider")], max=6, label="ForeArm Split Joints:", field=True,
                    v=(int(getGlobal("foreArmSplitNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.checkBox('moAlignHandIKChkBx', cc=lambda *args: setGlobal("alignHandIkToWorld", 1 - (
        int(getGlobal("alignHandIkToWorld")))),
                ann="If enabled, the IK control will be aligned to the world axes.",
                value=(int(getGlobal("alignHandIkToWorld"))), label="Align Hand IK to World Axes")
    enRhArmOptions = 0
    enRhArmsBn = 0
    rhArms = int(int(getGlobal("rubberHoseArms")))
    if (pm.intSliderGrp('moUpArmSpltIntSldrGrp', q=1, v=1)) > 0 and (
    pm.intSliderGrp('moForeArmSpltIntSldrGrp', q=1, v=1)) > 0:
        enRhArmOptions = rhArms
        enRhArmsBn = int(True)


    else:
        enRhArmsBn = enRhArmOptions = int(False)

    pm.text('moSetArmSpltJntWtVarsTxt', align="right", l="Split Joint Weights:")
    pm.button('moSetUpArmSpltJntWtVarsBn', c=lambda *args: pm.mel.moSplitJointDefaultsUI(-3),
              l=" Set UpArm Weights ")
    pm.button('moSetForeArmSpltJntWtVarsBn', c=lambda *args: pm.mel.moSplitJointDefaultsUI(-4),
              l=" Set ForeArm Weights ")
    pm.checkBox('moCreateRubberHoseArmsChkBx', cc=lambda *args: [
        setGlobal("rubberHoseArms", 1 - (int(getGlobal("rubberHoseArms")))),
        pm.mel.moServiceUIButton("armRubberHoseBn")], en=enRhArmsBn, value=rhArms, label="Build Rubberhose (RH) Arms")
    pm.checkBox('moArmsSqStChkBx', cc=lambda *args: setGlobal("squashStretchArms", 1 - (
        int(getGlobal("squashStretchArms")))),
                ann="If enabled, the rubber hose arms will be created with built in squash and stretch attributes.",
                en=enRhArmOptions, v=(int(getGlobal("squashStretchArms"))), label="Add Squash And Stretch")
    pm.intSliderGrp('moUpArmRhCtrlNumIntSldrGrp', en=enRhArmOptions, min=0,
                    cc=lambda *args: setGlobal("rhUpArmCtrlNum",
                                                          pm.intSliderGrp('moUpArmRhCtrlNumIntSldrGrp', q=1, v=1)),
                    max=6, label="UpArm RH Controls:", field=True, adjustableColumn3=3,
                    v=(int(getGlobal("rhUpArmCtrlNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.intSliderGrp('moForeArmRhCtrlNumIntSldrGrp', en=enRhArmOptions, min=0,
                    cc=lambda *args: setGlobal("rhForeArmCtrlNum",
                                                          pm.intSliderGrp('moForeArmRhCtrlNumIntSldrGrp', q=1, v=1)),
                    max=6, label="ForeArm RH Controls:", field=True, adjustableColumn3=3,
                    v=(int(getGlobal("rhForeArmCtrlNum"))), columnWidth3=(lSliderCol, 40, 100))
    pm.textFieldButtonGrp('moLfArmIkCtrlTxFldBnGrp', ed=False, manage=False, text="", label="LfArmIkCtrl:", eb=False)
    pm.textFieldButtonGrp('moRtArmIkCtrlTxFldBnGrp', ed=False, manage=False, text="", label="RtArmIkCtrl:", eb=False)
    pm.button('mocreateArmBn', h=28, c=lambda *args: pm.mel.moServiceUIButton("createArm"), label="Create Arm Rig")
    # hand form
    pm.setParent('..')
    pm.formLayout('moHandTabForm', numberOfDivisions=cCol)
    pm.textFieldButtonGrp('moHandCtrlTxFldBnGrp', adjustableColumn3=2,
                          bc=lambda *args: pm.mel.moServiceUI("handCtrl"), ed=False,
                          ann="Select the hand control (must be a nurbs curve).", label="Hand Ctrl:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moThumbTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("thumb"),
                          ed=False, ann="Select the first thumb joint (optional).", label="Thumb:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moIndexTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("index"),
                          ed=False, ann="Select the first index finger joint (optional).", label="Index:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moMiddleTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("middle"),
                          ed=False, ann="Select the middle finger joint (optional).", label="Middle:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moRingTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("ring"),
                          ed=False, ann="Select the first ring finger joint (optional).", label="Ring:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moPinkyTxFldBnGrp', adjustableColumn3=2, bc=lambda *args: pm.mel.moServiceUI("pinky"),
                          ed=False, ann="Select the first pinky finger joint (optional).", label="Pinky:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moRingCupTxFldBnGrp', adjustableColumn3=2,
                          bc=lambda *args: pm.mel.moServiceUI("ringCup"), ed=False,
                          ann="Select the ring cup joint (optional).", label="Ring Cup:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.textFieldButtonGrp('moPinkyCupTxFldBnGrp', adjustableColumn3=2,
                          bc=lambda *args: pm.mel.moServiceUI("pinkyCup"), ed=False,
                          ann="Select the first pinky cup joint (optional).", label="Pinky Cup:", text="",
                          columnWidth3=(lCol, cCol, rCol), buttonLabel=" Select ")
    pm.button('moHandQuickSelBn', c=lambda *args: pm.mel.moServiceUIButton("handQuickSel"),
              ann="Select controls in order that the fields on this tab are listed and press this button to fill them.",
              label=" Hand Quick Select ")
    pm.textFieldButtonGrp('moLfHandCtrlTxFldBnGrp', ed=False, manage=False, text="", label="LfHandCtrl:", eb=False)
    pm.textFieldButtonGrp('moRtHandCtrlTxFldBnGrp', ed=False, manage=False, text="", label="RtHandCtrl:", eb=False)
    pm.checkBox('moCreateIkFingerChkBx', cc=lambda *args: setGlobal("createIkFingerCtrls", 1 - (
        int(getGlobal("createIkFingerCtrls")))), value=(int(getGlobal("createIkFingerCtrls"))),
                label="Create Ik Finger Controls")
    pm.button('mocreateHandBn', h=28, c=lambda *args: pm.mel.moServiceUIButton("createHand"),
              label="Create Hand Rig")
    pm.formLayout('moForm', edit=1,
                  af=[('moTabLayout', "top", 0), ('moTabLayout', "left", 0), ('moTabLayout', "right", 0),
                      ('moTabLayout', "bottom", 0)])
    # start tab
    pm.formLayout('moStartTabForm', edit=1,
                  af=[('moNameTxFldGrp', "top", 14), ('moNameTxFldGrp', "left", lmargin),
                      ('moNameTxFldGrp', "right", (rCol + rmargin)), ('moCreateSkeletonBn', "bottom", 2),
                      ('moCreateSkeletonBn', "left", 2), ('moCreateSkeletonBn', "right", 2)])
    # spine tab
    pm.formLayout('moSpineTabForm', edit=1,
                  ac=[('moSpineRootTxFldBnGrp', "top", 4, 'moSpineJntsIntSldrGrp'),
                      ('moHipTxFldBnGrp', "top", 4, 'moSpineRootTxFldBnGrp'),
                      ('moSpineSqStChkBx', "top", 9, 'moHipTxFldBnGrp'),
                      ('moOrientSpineCtrlsChkBx', "top", 5, 'moSpineSqStChkBx'),
                      ('moAddSpineShaperChkBx', "top", 5, 'moOrientSpineCtrlsChkBx')],
                  af=[('moSpineJntsIntSldrGrp', "top", 14), ('moSpineJntsIntSldrGrp', "left", lmargin),
                      ('moSpineJntsIntSldrGrp', "right", rSliderCol), ('moSpineRootTxFldBnGrp', "left", lmargin),
                      ('moSpineRootTxFldBnGrp', "right", rmargin), ('moHipTxFldBnGrp', "left", lmargin),
                      ('moHipTxFldBnGrp', "right", rmargin), ('moSpineSqStChkBx', "left", (70 + lmargin)),
                      ('moOrientSpineCtrlsChkBx', "left", (70 + lmargin)),
                      ('moAddSpineShaperChkBx', "left", (70 + lmargin)), ('moCreateSpineBn', "bottom", 2),
                      ('moCreateSpineBn', "left", 2), ('moCreateSpineBn', "right", 2)])
    # head/neck tab
    pm.formLayout('moHeadTabForm', edit=1,
                  ac=[('moHeadTxFldBnGrp', "top", 4, 'moNeckTxFldBnGrp'),
                      ('moEyeTxFldBnGrp', "top", 4, 'moHeadTxFldBnGrp'),
                      ('moIncludeHeadNeckTransAttsChkBx', "top", 9, 'moEyeTxFldBnGrp'),
                      ('mocreateHeadSqStrBn', "top", 12, 'moIncludeHeadNeckTransAttsChkBx')],
                  af=[('moNeckTxFldBnGrp', "top", 14), ('moNeckTxFldBnGrp', "left", lmargin),
                      ('moNeckTxFldBnGrp', "right", rmargin), ('moHeadTxFldBnGrp', "left", lmargin),
                      ('moHeadTxFldBnGrp', "right", rmargin), ('moEyeTxFldBnGrp', "left", lmargin),
                      ('moEyeTxFldBnGrp', "right", rmargin),
                      ('moIncludeHeadNeckTransAttsChkBx', "left", (70 + lmargin)),
                      ('mocreateHeadSqStrBn', "left", (70 + lmargin)), ('moCreateHeadBn', "bottom", 2),
                      ('moCreateHeadBn', "left", 2), ('moCreateHeadBn', "right", 2)])
    # leg tab
    pm.formLayout('moLegTabForm', edit=1,
                  ac=[('moToeTxFldBnGrp', "top", 5, 'moUpLegTxFldBnGrp'),
                      ('moUpLegSpltIntSldrGrp', "top", 5, 'moToeTxFldBnGrp'),
                      ('moLowLegSpltIntSldrGrp', "top", 5, 'moUpLegSpltIntSldrGrp'),
                      ('moSetUpLegSpltJntWtVarsBn', "top", 5, 'moLowLegSpltIntSldrGrp'),
                      ('moSetLowLegSpltJntWtVarsBn', "top", 5, 'moLowLegSpltIntSldrGrp'),
                      ('moSetLowLegSpltJntWtVarsBn', "left", lmargin, 'moSetUpLegSpltJntWtVarsBn'),
                      ('moSetLegSpltJntWtVarsTxt', "top", 8, 'moLowLegSpltIntSldrGrp'),
                      ('moSetLegSpltJntWtVarsTxt', "right", rmargin, 'moSetUpLegSpltJntWtVarsBn'),
                      ('moCreateRubberHoseLegsChkBx', "top", 6, 'moSetUpLegSpltJntWtVarsBn'),
                      ('moLegsSqStChkBx', "top", 4, 'moCreateRubberHoseLegsChkBx'),
                      ('moUpLegRhCtrlNumIntSldrGrp', "top", 4, 'moLegsSqStChkBx'),
                      ('moLowLegRhCtrlNumIntSldrGrp', "top", 4, 'moUpLegRhCtrlNumIntSldrGrp'),
                      ('moHeelLocTxFldBnGrp', "top", 8, 'moLowLegRhCtrlNumIntSldrGrp'),
                      ('mocreateHeelLocBn', "top", 6, 'moHeelLocTxFldBnGrp'),
                      ('moCreateBothHeelLocChkBx', "top", 9, 'moHeelLocTxFldBnGrp'),
                      ('moCreateBothHeelLocChkBx', "left", 12, 'mocreateHeelLocBn'),
                      ('moFootIKCtrlAtAnkleChkBx', "top", 9, 'mocreateHeelLocBn')],
                  af=[('moUpLegTxFldBnGrp', "top", 14), ('moUpLegTxFldBnGrp', "left", lmargin),
                      ('moUpLegTxFldBnGrp', "right", rmargin), ('moToeTxFldBnGrp', "left", lmargin),
                      ('moToeTxFldBnGrp', "right", rSliderCol), ('moUpLegSpltIntSldrGrp', "left", lmargin),
                      ('moUpLegSpltIntSldrGrp', "right", rSliderCol), ('moLowLegSpltIntSldrGrp', "left", lmargin),
                      ('moLowLegSpltIntSldrGrp', "right", rSliderCol),
                      ('moSetUpLegSpltJntWtVarsBn', "left", (lSliderCol + 8)),
                      ('moSetLegSpltJntWtVarsTxt', "left", lmargin),
                      ('moCreateRubberHoseLegsChkBx', "left", (lSliderCol + 8)),
                      ('moLegsSqStChkBx', "left", (lSliderCol + 8)),
                      ('moUpLegRhCtrlNumIntSldrGrp', "left", lmargin),
                      ('moUpLegRhCtrlNumIntSldrGrp', "right", rSliderCol),
                      ('moLowLegRhCtrlNumIntSldrGrp', "left", lmargin),
                      ('moLowLegRhCtrlNumIntSldrGrp', "right", rSliderCol),
                      ('moHeelLocTxFldBnGrp', "left", lmargin), ('moHeelLocTxFldBnGrp', "right", rmargin),
                      ('mocreateHeelLocBn', "left", (70 + lmargin)),
                      ('moFootIKCtrlAtAnkleChkBx', "left", (70 + lmargin)), ('moCreateLegBn', "bottom", 2),
                      ('moCreateLegBn', "left", 2), ('moCreateLegBn', "right", 2)])
    # arm tab
    pm.formLayout('moArmTabForm', edit=1,
                  ac=[('moUpArmSpltIntSldrGrp', "top", 5, 'moUpArmTxFldBnGrp'),
                      ('moForeArmSpltIntSldrGrp', "top", 5, 'moUpArmSpltIntSldrGrp'),
                      ('moSetUpArmSpltJntWtVarsBn', "top", 5, 'moForeArmSpltIntSldrGrp'),
                      ('moSetForeArmSpltJntWtVarsBn', "top", 5, 'moForeArmSpltIntSldrGrp'),
                      ('moSetForeArmSpltJntWtVarsBn', "left", lmargin, 'moSetUpArmSpltJntWtVarsBn'),
                      ('moSetArmSpltJntWtVarsTxt', "top", 8, 'moForeArmSpltIntSldrGrp'),
                      ('moSetArmSpltJntWtVarsTxt', "right", rmargin, 'moSetUpArmSpltJntWtVarsBn'),
                      ('moCreateRubberHoseArmsChkBx', "top", 6, 'moSetUpArmSpltJntWtVarsBn'),
                      ('moArmsSqStChkBx', "top", 4, 'moCreateRubberHoseArmsChkBx'),
                      ('moUpArmRhCtrlNumIntSldrGrp', "top", 4, 'moArmsSqStChkBx'),
                      ('moForeArmRhCtrlNumIntSldrGrp', "top", 4, 'moUpArmRhCtrlNumIntSldrGrp'),
                      ('moAlignHandIKChkBx', "top", 9, 'moForeArmRhCtrlNumIntSldrGrp')],
                  af=[('moUpArmTxFldBnGrp', "top", 14), ('moUpArmTxFldBnGrp', "left", lmargin),
                      ('moUpArmTxFldBnGrp', "right", rmargin), ('moUpArmSpltIntSldrGrp', "left", lmargin),
                      ('moUpArmSpltIntSldrGrp', "right", rSliderCol), ('moForeArmSpltIntSldrGrp', "left", lmargin),
                      ('moForeArmSpltIntSldrGrp', "right", rSliderCol),
                      ('moSetUpArmSpltJntWtVarsBn', "left", (lSliderCol + 8)),
                      ('moSetArmSpltJntWtVarsTxt', "left", lmargin),
                      ('moCreateRubberHoseArmsChkBx', "left", (lSliderCol + 8)),
                      ('moArmsSqStChkBx', "left", (lSliderCol + 8)),
                      ('moUpArmRhCtrlNumIntSldrGrp', "left", lmargin),
                      ('moUpArmRhCtrlNumIntSldrGrp', "right", rSliderCol),
                      ('moForeArmRhCtrlNumIntSldrGrp', "left", lmargin),
                      ('moForeArmRhCtrlNumIntSldrGrp', "right", rSliderCol),
                      ('moAlignHandIKChkBx', "left", (70 + lmargin)), ('mocreateArmBn', "bottom", 2),
                      ('mocreateArmBn', "left", 2), ('mocreateArmBn', "right", 2)])
    # hand tab
    pm.formLayout('moHandTabForm', edit=1,
                  ac=[('moThumbTxFldBnGrp', "top", 6, 'moHandCtrlTxFldBnGrp'),
                      ('moIndexTxFldBnGrp', "top", 4, 'moThumbTxFldBnGrp'),
                      ('moMiddleTxFldBnGrp', "top", 4, 'moIndexTxFldBnGrp'),
                      ('moRingTxFldBnGrp', "top", 4, 'moMiddleTxFldBnGrp'),
                      ('moPinkyTxFldBnGrp', "top", 4, 'moRingTxFldBnGrp'),
                      ('moPinkyCupTxFldBnGrp', "top", 6, 'moPinkyTxFldBnGrp'),
                      ('moRingCupTxFldBnGrp', "top", 4, 'moPinkyCupTxFldBnGrp'),
                      ('moHandQuickSelBn', "top", 4, 'moRingCupTxFldBnGrp'),
                      ('moCreateIkFingerChkBx', "top", 6, 'moHandQuickSelBn')],
                  af=[('moHandCtrlTxFldBnGrp', "top", 14), ('moHandCtrlTxFldBnGrp', "left", lmargin),
                      ('moHandCtrlTxFldBnGrp', "right", rmargin), ('moThumbTxFldBnGrp', "left", lmargin),
                      ('moThumbTxFldBnGrp', "right", rmargin), ('moIndexTxFldBnGrp', "left", lmargin),
                      ('moIndexTxFldBnGrp', "right", rmargin), ('moMiddleTxFldBnGrp', "left", lmargin),
                      ('moMiddleTxFldBnGrp', "right", rmargin), ('moRingTxFldBnGrp', "left", lmargin),
                      ('moRingTxFldBnGrp', "right", rmargin), ('moPinkyTxFldBnGrp', "left", lmargin),
                      ('moPinkyTxFldBnGrp', "right", rmargin), ('moPinkyCupTxFldBnGrp', "left", lmargin),
                      ('moPinkyCupTxFldBnGrp', "right", rmargin), ('moRingCupTxFldBnGrp', "left", lmargin),
                      ('moRingCupTxFldBnGrp', "right", rmargin), ('moHandQuickSelBn', "left", (lCol + lmargin)),
                      ('moCreateIkFingerChkBx', "left", (lCol + lmargin)), ('mocreateHandBn', "bottom", 2),
                      ('mocreateHandBn', "left", 2), ('mocreateHandBn', "right", 2)])
    pm.tabLayout('moTabLayout', edit=1, preSelectCommand=lambda *args: pm.mel.moCheckUIItems(""),
                 tabLabel=[('moStartTabForm', "Start"), ('moSpineTabForm', "Spine"),
                           ('moHeadTabForm', "Head/Neck"), ('moLegTabForm', "Legs/Feet"),
                           ('moArmTabForm', "Arms"), ('moHandTabForm', "Hands")])
    pm.showWindow('moWin')
    pm.mel.moGuessUIItems()
    # update fields with existing ctrls
    # show shelf if it's hidden
    if not pm.mel.isUIComponentVisible("Shelf"):
        pm.mel.toggleUIComponentVisibility("Shelf")
        pm.pm.mel.warning("Enabling the shelf so the script will work.")

'''
import pymel.core as pm

def skeletonMakerUI():
    """==========================================================================================================\\
    ==========================================================================================================\\
    ====================              skeleton maker              ====================\\
    ====================           (with multiple neck and spine joints)      ====================\\
    ==========================================================================================================\\
    ==========================================================================================================\\"""

    if pm.window('moSklMkrWin', exists=1):
        pm.deleteUI('moSklMkrWin', window=1)
    # ui to build a skeleton

    pm.window('moSklMkrWin', minimizeButton=False, maximizeButton=False, h=406, t="abSkeletonMaker", w=266,
              menuBar=True)
    lmargin = 3
    rmargin = 3
    cbmargin = 20
    pm.menu(label="Options")
    pm.menuItem('moSklMkrUseBonesFrPrxyMnIt', c=lambda *args: setGlobal("useBonesForProxyDisplay", (
        str(pm.menuItem('moSklMkrUseBonesFrPrxyMnIt', q=1, checkBox=1)))),
                checkBox=(int(getGlobal("useBonesForProxyDisplay"))), label="Use Bones For Proxy Display")
    pm.menuItem('moSklMkrLckPrxyCtlAxMnIt', c=lambda *args: setGlobal("lockProxyCtlAxes", (
        str(pm.menuItem('moSklMkrLckPrxyCtlAxMnIt', q=1, checkBox=1)))),
                checkBox=(int(getGlobal("lockProxyCtlAxes"))), label="Lock Proxy Control Axes")
    pm.menuItem('moSklMkrAutoSaveMnIt', c=lambda *args: setGlobal("autoSaveSkeleton", (
        str(pm.menuItem('moSklMkrAutoSaveMnIt', q=1, checkBox=1)))),
                checkBox=(int(getGlobal("autoSaveSkeleton"))), label="Autosave Skeleton on Build")
    pm.menuItem('moSklMkrMirLegBehaviorMnIt', c=lambda *args: setGlobal("legMirrorBehavior", (
        str(pm.menuItem('moSklMkrMirLegBehaviorMnIt', q=1, checkBox=1)))),
                checkBox=(int(getGlobal("legMirrorBehavior"))), label="Mirror Leg Behavior")
    pm.formLayout('moSklMkrForm', numberOfDivisions=100)
    # string $updateProxyCmd = "string $gStr = \"skeleton_proxy_grpLoc\"; if (objExists($gStr)){int $gInt = `intSliderGrp -q -v moSklMkrFingerNumIntSldrGrp`; intSliderGrp -e -v 5 moSklMkrFingerNumIntSldrGrp; int $gInt1 = `intSliderGrp -q -v moSklMkrToeNumIntSldrGrp`; intSliderGrp -e -v 0 moSklMkrToeNumIntSldrGrp; moRecallLocStructureV2(moEncodeLocStructure($gStr, true), true); moConnectLocStructure($gStr); intSliderGrp -e -v $gInt moSklMkrFingerNumIntSldrGrp; intSliderGrp -e -v $gInt1 moSklMkrToeNumIntSldrGrp;}";
    # intSliderGrp -label "Spine Ctrl Num:" -min 3 -max 8 -v 3 -field true -columnWidth3 80 30 100 -adjustableColumn3 3 -cc $updateProxyCmd moSklMkrMidSpineNumIntSldrGrp;
    # intSliderGrp -label "Neck Num:" -min 1 -max 3 -v 1 -field true -columnWidth3 80 30 100 -adjustableColumn3 3 -cc $updateProxyCmd moSklMkrNeckNumIntSldrGrp;
    pm.intSliderGrp('moSklMkrMidSpineNumIntSldrGrp', adjustableColumn3=3, min=3, max=8, label="Spine Ctrl Num:",
                    field=True, v=3, columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrNeckNumIntSldrGrp', adjustableColumn3=3, min=1, max=3, label="Neck Num:", field=True,
                    v=1, columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrFingerNumIntSldrGrp', adjustableColumn3=3, min=2, max=5, label="Finger Num:", field=True,
                    v=5, columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrToeNumIntSldrGrp', adjustableColumn3=3, min=0, max=5, label="Toe Num:", field=True, v=0,
                    columnWidth3=(80, 30, 100))
    pm.button('moSklMkrPrxyBn', h=28, c=lambda *args: skelTemp.makeProxySkeleton(), l="Make Proxy Skeleton")
    pm.button('printglobalprefs', h=28, c=lambda *args: printGlobalPrefs(), l="print global prefs")
    pm.separator('moSklMkrSep1')
    pm.button('moSklMkrSavePrxyBn', c=lambda *args: skelTemp.saveProxySkeleton(), l="Save Proxy to Shelf")
    pm.separator('moSklMkrSep2')
    pm.intSliderGrp('moSklMkrSpineJntsSldrGrp', adjustableColumn3=3, min=4,
                    cc=lambda *args: setGlobal("spineJntNum",
                                                          pm.intSliderGrp('moSklMkrSpineJntsSldrGrp', q=1, v=1)),
                    max=18, label="Spine Joints:", field=True, v=(int(getGlobal("spineJntNum"))),
                    columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrUpArmSpltIntSldrGrp', adjustableColumn3=3, min=0,
                    cc=lambda *args: setGlobal("upArmSplitNum",
                                                          pm.intSliderGrp('moSklMkrUpArmSpltIntSldrGrp', q=1, v=1)),
                    max=6, label="UpArm Split:", field=True, v=(int(getGlobal("upArmSplitNum"))),
                    columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrForeArmSpltIntSldrGrp', adjustableColumn3=3, min=0,
                    cc=lambda *args: setGlobal("foreArmSplitNum",
                                                          pm.intSliderGrp('moSklMkrForeArmSpltIntSldrGrp', q=1, v=1)),
                    max=6, label="ForeArm Split:", field=True, v=(int(getGlobal("foreArmSplitNum"))),
                    columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrUpLegSpltIntSldrGrp', adjustableColumn3=3, min=0,
                    cc=lambda *args: setGlobal("upLegSplitNum",
                                                          pm.intSliderGrp('moSklMkrUpLegSpltIntSldrGrp', q=1, v=1)),
                    max=6, label="UpLeg Split:", field=True, v=(int(getGlobal("upLegSplitNum"))),
                    columnWidth3=(80, 30, 100))
    pm.intSliderGrp('moSklMkrKneeSpltIntSldrGrp', adjustableColumn3=3, min=0,
                    cc=lambda *args: setGlobal("lowLegSplitNum",
                                                          pm.intSliderGrp('moSklMkrKneeSpltIntSldrGrp', q=1, v=1)),
                    max=6, label="Knee Split:", field=True, v=(int(getGlobal("lowLegSplitNum"))),
                    columnWidth3=(80, 30, 100))
    # checkBox -l "Add Spine Shaper Curve" -v (int(moGetGlobal("addSpineShaper"))) -cc "moSetGlobal(\"addSpineShaper\", (int(`checkBox -q -v moSklMkrAddSpineShaperChkBx`)));" moSklMkrAddSpineShaperChkBx;
    pm.checkBox('moSklMkrAddSpineShaperChkBx', cc=lambda *args: setGlobal("addSpineShaper", (
        int(pm.checkBox('moSklMkrAddSpineShaperChkBx', q=1, v=1)))),
                ann="Enable this checkbox if you want your character to have a Spine Shaper control curve.  The curve of the spine will be adjusted (very very) slightly relative to a spine created without a Shaper.",
                l="Character Will Use A Spine Shaper Control", v=(int(getGlobal("addSpineShaper"))))
    pm.checkBox('moSklMkrHierarchicalWtJntsChkBx',
                cc=lambda *args: setGlobal("createLimbWtJntsInHierarchy", (
                    int(pm.checkBox('moSklMkrHierarchicalWtJntsChkBx', q=1, v=1)))),
                ann="Enable to create arm and leg joints in a hierarchy (which may have skinning benefits).  Otherwise they will be free floating.",
                l="Create Hierarchical Limb Weight Joints",
                v=(int(getGlobal("createLimbWtJntsInHierarchy"))))
    pm.button('moSklMkrBldBn', h=28, c=lambda *args: skelTemp.skeletonizeProxy(), l="Build Skeleton")
    pm.formLayout('moSklMkrForm', ac=[('moSklMkrMidSpineNumIntSldrGrp', "top", 5, 'moSklMkrPrxyBn'),
                                        ('moSklMkrNeckNumIntSldrGrp', "top", 5, 'moSklMkrMidSpineNumIntSldrGrp'),
                                        ('moSklMkrFingerNumIntSldrGrp', "top", 5, 'moSklMkrNeckNumIntSldrGrp'),
                                        ('moSklMkrToeNumIntSldrGrp', "top", 5, 'moSklMkrFingerNumIntSldrGrp'),
                                        ('moSklMkrSep1', "top", 4, 'moSklMkrToeNumIntSldrGrp'),
                                        ('moSklMkrSavePrxyBn', "top", 5, 'moSklMkrSep1'),
                                        ('moSklMkrSep2', "top", 4, 'moSklMkrSavePrxyBn'),
                                        ('moSklMkrSpineJntsSldrGrp', "top", 5, 'moSklMkrSep2'),
                                        ('moSklMkrUpArmSpltIntSldrGrp', "top", 5, 'moSklMkrSpineJntsSldrGrp'),
                                        ('moSklMkrForeArmSpltIntSldrGrp', "top", 5, 'moSklMkrUpArmSpltIntSldrGrp'),
                                        ('moSklMkrUpLegSpltIntSldrGrp', "top", 5, 'moSklMkrForeArmSpltIntSldrGrp'),
                                        ('moSklMkrKneeSpltIntSldrGrp', "top", 5, 'moSklMkrUpLegSpltIntSldrGrp'),
                                        ('moSklMkrAddSpineShaperChkBx', "top", 6, 'moSklMkrKneeSpltIntSldrGrp'), (
                                        'moSklMkrHierarchicalWtJntsChkBx', "top", 5, 'moSklMkrAddSpineShaperChkBx'),
                                        ('moSklMkrBldBn', "top", 16, 'moSklMkrHierarchicalWtJntsChkBx')],
                  e=1, af=[('moSklMkrPrxyBn', "top", 6), ('moSklMkrPrxyBn', "left", lmargin),
                           ('moSklMkrPrxyBn', "right", rmargin), ('moSklMkrMidSpineNumIntSldrGrp', "left", lmargin),
                           ('moSklMkrMidSpineNumIntSldrGrp', "right", rmargin),
                           ('moSklMkrNeckNumIntSldrGrp', "left", lmargin),
                           ('moSklMkrNeckNumIntSldrGrp', "right", rmargin),
                           ('moSklMkrFingerNumIntSldrGrp', "left", lmargin),
                           ('moSklMkrFingerNumIntSldrGrp', "right", rmargin),
                           ('moSklMkrToeNumIntSldrGrp', "left", lmargin),
                           ('moSklMkrToeNumIntSldrGrp', "right", rmargin), ('moSklMkrSep1', "left", lmargin),
                           ('moSklMkrSep1', "right", rmargin), ('moSklMkrSavePrxyBn', "left", lmargin),
                           ('moSklMkrSavePrxyBn', "right", rmargin), ('moSklMkrSep2', "left", lmargin),
                           ('moSklMkrSep2', "right", rmargin), ('moSklMkrSpineJntsSldrGrp', "left", lmargin),
                           ('moSklMkrSpineJntsSldrGrp', "right", rmargin),
                           ('moSklMkrUpArmSpltIntSldrGrp', "left", lmargin),
                           ('moSklMkrUpArmSpltIntSldrGrp', "right", rmargin),
                           ('moSklMkrForeArmSpltIntSldrGrp', "left", lmargin),
                           ('moSklMkrForeArmSpltIntSldrGrp', "right", rmargin),
                           ('moSklMkrUpLegSpltIntSldrGrp', "left", lmargin),
                           ('moSklMkrUpLegSpltIntSldrGrp', "right", rmargin),
                           ('moSklMkrKneeSpltIntSldrGrp', "left", lmargin),
                           ('moSklMkrKneeSpltIntSldrGrp', "right", rmargin),
                           ('moSklMkrAddSpineShaperChkBx', "left", (lmargin + cbmargin)),
                           ('moSklMkrAddSpineShaperChkBx', "right", rmargin),
                           ('moSklMkrHierarchicalWtJntsChkBx', "left", (lmargin + cbmargin)),
                           ('moSklMkrHierarchicalWtJntsChkBx', "right", rmargin),
                           ('moSklMkrBldBn', "left", lmargin), ('moSklMkrBldBn', "right", rmargin)])
    pm.showWindow('moSklMkrWin')

def getGlobal(name):

    if name in settings.globalPrefs:
        return settings.globalPrefs[name]
    else:
        return False

def setGlobal(name, strVal):
    if name not in settings.globalPrefs:
        settings.globalPrefs[name] = strVal

def printGlobalPrefs():
    #settings.initGlobals()
    print settings.globalPrefs

