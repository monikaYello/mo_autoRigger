import sys
import maya.cmds as mc
sys.path.append('D:\Google Drive\PythonScripting\mo_autoRigger')
sys.path.append('D:\Google Drive\PythonScripting\scripts')

# Build template and skinJnts with UI
import moRig_UI as moRig_UI
reload(moRig_UI)
moRig_UI.skeletonMakerUI()


# Build tempate script
import moRig_skeletonTemplate as skelTemp
reload(skelTemp)
import moRig_settings as settings
settings.initGlobals()
settings.globalPrefs["spineCtrlNum"] = "3"
settings.globalPrefs["globalScale"] = ".4"
skelTemp.makeProxySkeleton()
mc.scale('skeleton_proxy_grpLoc', [0.34,0.34,0.34])

# Build skinJnts from template
import moRig_skeletonTemplate as skelTemp
reload(skelTemp)
settings.globalPrefs["spineJntNum"] = "6"
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
jnts={}
biped.define_ctrlJnts(jnts)

# ikfk jnts
arm.build_jnts_arm(jnts, mode=['ik', 'fk'])
leg.build_jnts_leg(jnts, mode=['ik', 'fk'])

biped.define_fkJnts(jnts)
biped.define_ikJnts(jnts)

# ctrls
scale = 1
biped.createWorld(scale=scale)
arm.create_ctrl_fk_arm(jnts, scale=scale)
arm.create_ctrl_ik_arm(jnts, scale=scale)


reload(leg)
leg.create_ctrl_fk_leg(jnts, scale=scale)
leg.create_ctrl_ik_leg(jnts, scale=scale)

biped.define_ikJnts(jnts)

# ikfk with switch
arm.setup_fk_arm(jnts, RL='L')
arm.setup_ik_arm(jnts, RL='L')
arm.setup_ikfkSwitch_arm(jnts)

# spine
reload(spine)
spine.create_fk_spine(amount=3)
reload(spine)
spine.create_ctrl_spine(jnts)

spine.setup_spine(jnts)

# space switch
arm.setup_fk_spaceswitch_arm(jnts)



def test():
    stringnode = 'abc'
    numbernode = 343
    print stringnode
    return

test()