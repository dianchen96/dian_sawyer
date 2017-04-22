import rospy
import intera_interface
import argparse
import csv
import subprocess
import os

def subprocess_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	print proc_stdout

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('trajectory_file', type=str)
	parser.add_argument('output_file', type=str)
	args = parser.parse_args()

	rospy.init_node("test_readings")
	limb = intera_interface.Limb("right")
	joint_names = limb.joint_names()

	f = open(args.output_file, 'a+')
	writer = csv.DictWriter(f, fieldnames=joint_names)
	writer.writeheader()

	rate = rospy.Rate(10)

	traj_path = os.path.join(os.getcwd(), args.trajectory_file)
	cmd = "rosrun intera_examples joint_trajectory_file_playback.py -f {}".format(traj_path)
	subprocess.Popen(cmd, shell=True)

	try:
		while not rospy.is_shutdown():
			torque_readings = limb._joint_effort
			print torque_readings
			writer.writerow(torque_readings)
			rate.sleep()
	except KeyboardInterrupt:
		rospy.signal_shutdown("Finished")


if __name__ == '__main__':
	main()