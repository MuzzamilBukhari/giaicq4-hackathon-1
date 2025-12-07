using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Sensor;

public class RobotJointController : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 10000;

    [Header("Joint Configuration")]
    public List<ArticulationBody> jointArticulationBodies = new List<ArticulationBody>();
    public List<string> jointNames = new List<string>();

    [Header("ROS Topics")]
    public string jointStateTopic = "/joint_states";
    public string commandTopic = "/unity_robot_command";

    private ROSConnection ros;
    private bool isInitialized = false;

    void Start()
    {
        InitializeROSConnection();
        SubscribeToJointStates();
    }

    void InitializeROSConnection()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.rosIPAddress = rosIPAddress;
        ros.rosPort = rosPort;
        isInitialized = true;
    }

    void SubscribeToJointStates()
    {
        ros.Subscribe<sensor_msgs.JointState>(jointStateTopic, OnJointStateReceived);
    }

    void OnJointStateReceived(sensor_msgs.JointState jointState)
    {
        if (!isInitialized) return;

        // Update each joint based on received joint states
        for (int i = 0; i < jointNames.Count; i++)
        {
            string jointName = jointNames[i];
            int jointIndex = jointState.name.IndexOf(jointName);

            if (jointIndex != -1 && jointIndex < jointState.position.Count)
            {
                // Convert radians to degrees for Unity ArticulationBody
                float targetAngle = Mathf.Rad2Deg * (float)jointState.position[jointIndex];

                if (i < jointArticulationBodies.Count)
                {
                    ArticulationBody jointBody = jointArticulationBodies[i];
                    ArticulationDrive drive = jointBody.xDrive;
                    drive.target = targetAngle;
                    jointBody.xDrive = drive;
                }
            }
        }
    }

    // Method to publish joint commands (optional)
    public void PublishJointCommand(string jointName, double position)
    {
        if (!isInitialized) return;

        var jointState = new sensor_msgs.JointState();
        jointState.name.Add(jointName);
        jointState.position.Add(position);
        jointState.header.stamp = new builtin_interfaces.Time();

        ros.Publish(jointStateTopic + "_out", jointState);
    }

    // Example method to send a command to ROS
    public void SendCommandToROS(string command)
    {
        if (!isInitialized) return;

        var stringMsg = new StringMsg();
        stringMsg.data = command;

        ros.Publish(commandTopic, stringMsg);
    }
}