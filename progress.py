'''
base is skinJnt's

1. duplicate skinJnts to create ctrlJnts
2. ik/fk. 2 replika of ctrlJnts replace _ctrlJnt with _ikJnt, fk_jnts
3. create ctrls for fk/ik jnts
4. hook up fk/ik jntrls with jnts
5. blend between fk and ik
6. space switch



'''
#TODO fkStretch Arm connect with Ctrl

'''
CODE
import sys

#sys.path.append('D:\Google Drive\PythonScripting\my_autoRigger')
#sys.path.append('D:\Google Drive\PythonScripting\scripts')
import mo_biped as biped
import mo_spine as spine
import mo_arm as arm
import mo_leg as leg
reload(biped)
reload(arm)
reload(leg)
## TODO Build skinJnts form template
## temporary work with autoRigger_lumaHuman.003

# Build ctrlJnts form skinJnts
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
biped.createWorld()
arm.create_ctrl_fk_arm(jnts)
arm.create_ctrl_ik_arm(jnts)


leg.create_ctrl_fk_leg(jnts)
leg.create_ctrl_ik_leg(jnts)

reload(arm)
biped.define_fkCtrls(jnts)

# ikfk with switch
arm.setup_fk_arm(jnts, RL='L')
arm.setup_ik_arm(jnts, RL='L')
arm.setup_ikfkSwitch_arm(jnts)
arm.setup_ik_stretch_arm(jnts)

reload(leg)
leg.setup_fk_leg(jnts, RL='L')
leg.setup_ik_leg(jnts, RL='L')
leg.setup_ikfkSwitch_leg(jnts)

# spine
biped.create_ctrl_spine(jnts, spine_count=3, size=2.0)
spine.setup_spine(jnts)

# space switch
arm.setup_fk_spaceswitch_arm(jnts)

'''