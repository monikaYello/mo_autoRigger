import pymel.core as pm
import maya.cmds as cmds
import logging

# CREATE A LOGGER
_logger = logging.getLogger(__name__)

'''
The three template types, Joint Node, Spline Node and Hinge Node templates are defined as methods,
"createJointNodeTemplate", "createSplineNodeTemplate" and "createHingeNodeTemplate" for the main
template class, "MRT_Template".
'''


class Template(object):

    COLOR_PRESETS = {
            "grey": (.5, .5, .5),
            "lightgrey": (.7, .7, .7),
            "darkgrey": (.25, .25, .25),
            "red": (1, 0, 0),
            "lightred": (1, .5, 1),
            "peach": (1, .5, .5),
            "darkred": (.6, 0, 0),
            "orange": (1., .5, 0),
            "lightorange": (1, .7, .1),
            "darkorange": (.7, .25, 0),
            "yellow": (1, 1, 0),
            "lightyellow": (1, 1, .5),
            "darkyellow": (.8, .8, 0.),
            "green": (0, 1, 0),
            "lightgreen": (.4, 1, .2),
            "darkgreen": (0, .5, 0),
            "blue": (0, 0, 1),
            "lightblue": (.4, .55, 1),
            "darkblue": (0, 0, .4),
            "purple": (.7, 0, 1),
            "lightpurple": (.8, .5, 1),
            "darkpurple": (.375, 0, .5),
            "brown": (.57, .49, .39),
            "lightbrown": (.76, .64, .5),
            "darkbrown": (.37, .28, .17)}

    def __init__(self, templateInfo):
        '''
        Common template creation attributes for all template types. The "templateInfo"
        is a dictionary which is passed-in, containing the template creation option/values.
        '''

        # Attributes to store values from "templateInfo":

        # Template name.
        self.basename = templateInfo['template_basename']
        self.prefix = templateInfo['template_prefix']
        self.type = templateInfo['template_type']
        self.name = self.prefix + '_' + self.basename
        self.color = templateInfo['template_colour']
        self.numNodes = templateInfo['num_nodes']
        self.length = templateInfo['template_length']
        self.onPlane = templateInfo['creation_plane'][-2:]
        self.aimAxis = templateInfo['aim_axis']  # direction pointing
        self.initNodePosition = templateInfo['initial_node_position']
        self.proxyStatus = templateInfo['proxy_status']
        self.proxyShape = templateInfo['proxy_shape']
        self.worldScale = templateInfo['world_scale']

        # Create mirror template on/off.
        self.mirrorStatus = templateInfo['mirror_status']  # 0: no mirror, 1: has mirror, 2: is mirror
        self.mirrorPlane = templateInfo['mirror_plane']

        # To store nodes.
        self.nodeList = []

    def createJointNodeTemplate(self):
        '''
        Create a Joint Node template type.
        '''

        # Set the current namespace to root.
        cmds.namespace(setNamespace=':')

        # Create the main groups.
        self.groupNode = pm.group(empty=True, name=self.name + '_templateGrp')
        self.extraGroupNode = pm.group(empty=True, name=self.name + '_extrasGrp')
        pm.parent(self.extraGroupNode, self.groupNode)

        # Add a custom attributes to the template group to store template creation attributes.
        # number and length
        pm.addAttr(self.groupNode, attributeType='short', longName='numberOfNodes', defaultValue=self.numNodes, k=False)
        pm.addAttr(self.groupNode, attributeType='float', longName='templateLength', defaultValue=self.length, k=False)
        # orientaton
        _logger.debug('nodeOrient. %s' % self.groupNode)
        pm.addAttr(self.groupNode, dataType='string', longName='nodeOrient', keyable=False)
        pm.setAttr(self.groupNode + '.nodeOrient', self.aimAxis, type='string')
        # parent
        pm.addAttr(self.groupNode, dataType='string', longName='templateParent', keyable=False)
        pm.setAttr(self.groupNode + '.templateParent', 'None', type='string')

        pm.addAttr(self.groupNode, dataType='string', longName='onPlane', keyable=False)
        pm.setAttr(self.groupNode + '.onPlane', '+' + self.onPlane, type='string')
        # mirror
        pm.addAttr(self.groupNode, at='short', longName='mirrorStatus', keyable=False, dv=0)
        pm.addAttr(self.groupNode, dataType='string', longName='mirrorPlane', keyable=False)
        pm.setAttr(self.groupNode + '.mirrorPlane', '+' + self.mirrorPlane, type='string')

        # Move the joints group to the start position for the first joint node.
        pm.xform(self.groupNode, worldSpace=True, translation=self.initNodePosition)
        _logger.debug('Done crating main groups. %s' % self.groupNode)

        # calculate position
        offset = self.length / (self.numNodes - 1)
        _logger.debug(offset)

        for i in range(self.numNodes):
            knobname = '%s%02d_knob' % (self.name, i + 1)
            if i == 0:
                transform = 0
            else:
                transform = offset * i

            knob = pm.sphere(n=knobname, r=3 * self.worldScale)[0]
            pm.move(knob, transform)

            # self.createKnob(knobname, position)
            self.assignMaterial(knob)
            _logger.debug('Done crating knobs. %s' % knob)
            self.nodeList.append(knob)

            if i > 0:
                connector = self.createConnector(pt1=self.nodeList[i - 1], pt2=self.nodeList[i], radius=1 * self.worldScale)
                self.assignMaterial(connector)

        _logger.debug('Done crating knobs. %s' % self.groupNode)



        return

        # Create the template nodes (joints) by their position and name them accordingly.
        for index, nodePos in enumerate(self.initNodePos):
            if index == 0:
                jointName = cmds.joint(name=self.templateTypespace + ':root_node_transform', position=nodePos,
                                       radius=0.0, scaleCompensate=False)
            elif nodePos == self.initNodePos[-1]:
                jointName = cmds.joint(name=self.templateTypespace + ':end_node_transform', position=nodePos,
                                       radius=0.0, scaleCompensate=False)
            else:
                jointName = cmds.joint(name=self.templateTypespace + ':node_%s_transform' % (index), position=nodePos,
                                       radius=0.0, scaleCompensate=False)
            cmds.setAttr(jointName + '.drawStyle', 2)

            mfunc.lockHideChannelAttrs(jointName, 'r', 's', 'v', 'radi', keyable=False)

            self.nodeList.append(jointName)

        # Orient the joints.
        cmds.select(self.nodeList[0], replace=True)

        # For orientation we'll use the axis perpendicular to the creation plane as the up axis for secondary axis orient.
        secondAxisOrientation = {'XY': 'z', 'YZ': 'x', 'XZ': 'y'}[self.onPlane] + 'up'
        cmds.joint(edit=True, orientJoint=self.aimAxis.lower(), secondaryAxisOrient=secondAxisOrientation,
                   zeroScaleOrient=True, children=True)

        # Orient the end joint node, if the template contains more than one joint node.
        if self.numNodes > 1:
            cmds.setAttr(self.nodeList[-1] + '.jointOrientX', 0)
            cmds.setAttr(self.nodeList[-1] + '.jointOrientY', 0)
            cmds.setAttr(self.nodeList[-1] + '.jointOrientZ', 0)

        # Mirror the template node joints (for the mirrored template) if the template mirroring is enabled
        # and the current template to be created is a mirrored template on the -ve side of the creation plane,
        # and if the mirror rotation function is set to "Behaviour".
        if self.mirrorTemplate:
            mirrorPlane = {'XY': False, 'YZ': False, 'XZ': False}
            mirrorPlane[self.onPlane] = True
            mirroredJoints = cmds.mirrorJoint(self.nodeList[0],
                                              mirrorXY=mirrorPlane['XY'], mirrorYZ=mirrorPlane['YZ'],
                                              mirrorXZ=mirrorPlane['XZ'],
                                              mirrorBehavior=True if self.mirrorRotationFunc == 'Behaviour' else False)

            for joint in mirroredJoints:
                newJoint = cmds.rename(joint, self.templateTypespace + ':' + joint)
                self.nodeList.append(newJoint)

        # Clear selection after joint orientation.
        cmds.select(clear=True)

        # Create and position the template transform control.
        templateHandle = objects.createTemplateTransform(namespace=self.templateTypespace, scale=0.26)
        cmds.delete(cmds.pointConstraint(self.nodeList[0], templateHandle['transform'], maintainOffset=False))
        self.templateTransform = templateHandle['transform']
        self.collectedNodes.append(templateHandle['scaleFactor'])

        # Add the template transform to the template group.
        cmds.parent(templateHandle['preTransform'], self.groupNode, absolute=True)

        # Set up constraints for the template transform.
        template_node_parentConstraint = mfunc.parentConstraint(self.templateTransform, self.templateNodesGrp,
                                                                maintainOffset=True, namespace=self.templateTypespace)
        template_node_scaleConstraint = mfunc.scaleConstraint(self.templateTransform, self.templateNodesGrp,
                                                              maintainOffset=False, namespace=self.templateTypespace)

        # Create hierarchy/orientation representation on joint node(s), depending on number of nodes in the template.
        self.createJointNodeControlHandleRepr()
        if len(self.nodeList) == 1:
            self.templateSingleOrientationReprGrp = cmds.group(empty=True,
                                                               name=self.templateTypespace + ':templateSingleOrientationReprGrp',
                                                               parent=self.templateReprGrp)

            singleOrientationTransform = objects.createRawSingleOrientationRepresentation()
            cmds.setAttr(singleOrientationTransform + '.scale', 0.65, 0.65, 0.65, type='double3')
            cmds.makeIdentity(singleOrientationTransform, scale=True, apply=True)
            cmds.parent(singleOrientationTransform, self.templateSingleOrientationReprGrp, absolute=True)
            cmds.rename(singleOrientationTransform, self.templateTypespace + ':' + singleOrientationTransform)
            cmds.xform(self.templateSingleOrientationReprGrp, worldSpace=True, absolute=True,
                       translation=cmds.xform(self.nodeList[0], query=True, worldSpace=True, translation=True))
            mfunc.parentConstraint(self.nodeList[0], self.templateSingleOrientationReprGrp,
                                   maintainOffset=False, namespace=self.templateTypespace)
            mfunc.scaleConstraint(self.templateTransform, self.templateSingleOrientationReprGrp,
                                  maintainOffset=False, namespace=self.templateTypespace)

            nodeHandles = []

            # Set the sizes for the template node handle shapes.
            for joint in self.nodeList:
                handle = objects.load_xhandleShape(transform=joint, colour=self.tmpHandleColour)
                cmds.setAttr(handle['shape'] + '.localScaleX', 0.089)
                cmds.setAttr(handle['shape'] + '.localScaleY', 0.089)
                cmds.setAttr(handle['shape'] + '.localScaleZ', 0.089)
                cmds.setAttr(handle['shape'] + '.ds', 5)

                nodeHandles.append(handle)

            # If there's more than one node, create orientation/hierarchy representations for all joints, except for
            # the end joint. Also unparent the individual joints in the oriented joint chain to the joint group. This
            # is needed only if there are more than one joint in the template; then the unparenting will begin from the
            # second joint, since the first (start) is already under joints group.
            if len(self.nodeList) > 1:
                for handle in nodeHandles[1:]:
                    cmds.parent(handle['preTransform'], self.templateNodesGrp, absolute=True)
                self.createOrientationHierarchyReprOnNodes()

            # Clear selection.
            cmds.select(clear=True)

            # If the template contains only one node then delete the handle segment and orientation/hierarchy
            # representation groups, since they're not needed.
            if self.numNodes == 1:
                cmds.delete([self.templateHandleSegmentGrp, self.templateOrientationHierarchyReprGrp])

            # Create template parenting representation objects.
            self.createHierarchySegmentForTemplateParentingRepr()

            # Create the proxy geometry for the template if it is enabled.
            if self.proxyGeoStatus:
                if self.proxyGeoElbow:
                    self.createProxyGeo_elbows(self.proxyElbowType)
                if self.proxyGeoBones:
                    self.createProxyGeo_bones()

            # Add the template group to the collected nodes list.
            self.collectedNodes.append(self.groupNode)

            # Add the collected nodes to the template container.
            mfunc.addNodesToContainer(self.templateContainer, self.collectedNodes, includeHierarchyBelow=True,
                                      includeShapes=True)

            # Publish contents to the container.
            # Publish the orientation representation control for template nodes.
            for joint in self.nodeList:
                jointName = mfunc.stripMRTNamespace(joint)[1]  # Nice name for the joint, used as published name.
                cmds.container(self.templateContainer, edit=True,
                               publishAndBind=[joint + '.translate', jointName + '_translate'])
                if joint != self.nodeList[-1]:
                    jointOrientationRepr = joint + '_orient_repr_transform'
                    jointOrientationRotateAxis = self.aimAxis[0]
                    jointOrientationReprName = mfunc.stripMRTNamespace(jointOrientationRepr)[1]
                    cmds.container(self.templateContainer, edit=True,
                                   publishAndBind=[jointOrientationRepr + '.rotate' + jointOrientationRotateAxis,
                                                   jointOrientationReprName + '_rotate' + jointOrientationRotateAxis])

            # Publish the attributes for the template transform.
            templateTransformName = mfunc.stripMRTNamespace(self.templateTransform)[1]
            cmds.container(self.templateContainer, edit=True, publishAndBind=[self.templateTransform + '.translate',
                                                                              templateTransformName + '_translate'])
            cmds.container(self.templateContainer, edit=True, publishAndBind=[self.templateTransform + '.rotate',
                                                                              templateTransformName + '_rotate'])
            cmds.container(self.templateContainer, edit=True, publishAndBind=[self.templateTransform + '.glzobalScale',
                                                                              templateTransformName + '_globalScale'])
            cmds.container(self.templateContainer, edit=True, publishAndBind=[self.templateTransform + '.scaleFactor',
                                                                              templateTransformName + '_scaleFactor'])

            # If the template contains only single node, publish its orientation control.
            if len(self.nodeList) == 1:
                singleOrientationTransform = self.templateTypespace + ':single_orient_repr_transform'
                cmds.container(self.templateContainer, edit=True,
                               publishAndBind=[singleOrientationTransform + '.rotate',
                                               'single_orient_repr_transform_rotate'])
            # Add and publish custom attributes on the template transform.
            self.addCustomAttributesOnTemplateTransform()

            # Connect template orientation representation objects to drive
            # orientation for template proxy geometry.
            if self.numNodes > 1:
                self.connectCustomOrientationReprToTemplateProxies()

            # Set the template pre-scale factor. This is used for adjusting the initial size of the template.
            cmds.setAttr(self.templateTransform + '.scaleFactor', 30)

    def createConnector(self, pt1, pt2, radius=0.5):

        # create cylinder and align between pt1/pt2
        base_name = pt1
        _logger.debug('Connector base name is %s' % base_name)
        viz_shape = pm.cylinder(n=base_name + 'Connector')
        pm.pointConstraint([pt1, pt2], viz_shape[0], mo=0)
        pm.aimConstraint(pt2, viz_shape[0], weight=1, upVector=(0, 1, 0), worldUpType="vector", offset=(0, 0, 0),
                         aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))

        viz_direction = pm.cone(n=base_name + 'Direction', r=3 * radius)
        viz_shape[0].t >> viz_direction[0].t
        viz_shape[0].r >> viz_direction[0].r

        # measure distance between
        dist_node = pm.createNode('distanceBetween', n=base_name + '_distanceBetween')
        pm.connectAttr(pt1 + '.worldMatrix[0]', dist_node + '.inMatrix1', f=True)
        pm.connectAttr(pt2 + '.worldMatrix[0]', dist_node + '.inMatrix2', f=True)
        _logger.debug('Distance between base name is %s' % base_name)

        # length
        divide_half = pm.createNode('multiplyDivide', n=base_name + '_distceBetween_multiplyDivide')
        divide_half.input2X.set(0.5)
        dist_node.distance >> divide_half.input1X
        divide_half.outputX >> viz_shape[0].scaleX

        # radius
        viz_shape[0].scaleZ.set(radius)
        viz_shape[0].scaleY.set(radius)

        return [viz_shape[0], viz_direction[0]]

    def assignMaterial(self, node, shader='surfaceShader'):
        _logger.debug('Creating shader %s'%node)
        pm.delete(self.name + '_templateShader')
        if pm.objExists(self.name + '_templateShader') == False:
            shaderNode = pm.shadingNode(shader, asShader=True, name=self.name + '_templateShader')
            pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderNode + 'SG')


            _logger.debug(Template.COLOR_PRESETS[self.color])
            pm.setAttr(shaderNode + '.outColor',
                       Template.COLOR_PRESETS[self.color][0],
                       Template.COLOR_PRESETS[self.color][1],
                       Template.COLOR_PRESETS[self.color][2], type='double3')
            pm.setAttr(shaderNode + '.outTransparency', [.5, .5, .5] )
            pm.connectAttr(shaderNode + '.outColor', shaderNode + 'SG.surfaceShader')
        else:
            shaderNode = pm.PyNode(self.name + '_templateShader')

        _logger.debug('Assigning color schader %s'% shaderNode )
        pm.sets(shaderNode + 'SG', edit=True, forceElement=node)



def createSimpleJointNodeTemplate(basename='template', prefix='C', num_nodes=2,
                                  creation_plane='xz', axis='x', world_scale=1, initial_position=[0, 0, 0]):
    '''
    Create default joint template

    import sys
    sys.path.append('D:\Google Drive\PythonScripting\my_autoRigger')
    import mog_template as mogt
    mogt.createSimpleJointNodeTemplate()
    '''
    # create joint template
    section_length = 15 * world_scale
    template_length = section_length * num_nodes

    jointTemplate = Template(templateInfo={
        'template_basename': basename,
        'template_prefix': prefix,
        'template_type': 'jointTemplate',
        'template_colour': 'lightblue',
        'num_nodes': num_nodes,
        'template_length': template_length,
        'world_scale': world_scale,
        'creation_plane': creation_plane,
        'aim_axis': axis,
        'initial_node_position': initial_position,
        'proxy_status': 1,
        'proxy_shape': 'sphere',
        'mirror_status': 0,
        'mirror_plane': 'x'
    })

    jointTemplate.createJointNodeTemplate()

    return jointTemplate
