import genome
import creature
import pybullet as p
import time 
import random
import numpy as np

## ... usual starter code to create a sim and floor
p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(1)


# generate a random creature
cr = creature.Creature(gene_count=5)
# save it to XML
with open('test.urdf', 'w') as f:
    f.write(cr.to_xml())
# load it into the sim
rob1 = p.loadURDF('test.urdf')
start_pos, orn = p.getBasePositionAndOrientation(rob1)

# iterate 
while True:
    motors = cr.get_motors()
    assert len(motors) == p.getNumJoints(rob1), "Something went wrong"
    for jid in range(p.getNumJoints(rob1)):
        mode = p.VELOCITY_CONTROL
        vel = motors[jid].get_output()
        p.setJointMotorControl2(rob1, 
                        jid,  
                        controlMode=mode, 
                        targetVelocity=vel)
    new_pos, orn = p.getBasePositionAndOrientation(rob1)
    #print(new_pos)
    dist_moved = np.linalg.norm(np.asarray(start_pos) - np.asarray(new_pos))
    print(dist_moved)
    time.sleep(0.1)