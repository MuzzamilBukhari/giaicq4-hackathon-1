import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci # Using Fibonacci for demonstration, imagine it's a 'MoveRobot' action
import time

class TextCommandAgent(Node):

    def __init__(self):
        super().__init__('text_command_agent')
        self._action_client = ActionClient(self, Fibonacci, 'robot_command_action') # Renamed action topic

    def send_goal(self, command_value):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = command_value # Interpreting command_value as 'order' for Fibonacci

        self._action_client.wait_for_server()

        self.get_logger().info(f'Sending goal: {command_value}')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Action completed. Result: {result.sequence}')
        # rclpy.shutdown() # Don't shutdown if agent is continuous

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')

def main(args=None):
    rclpy.init(args=args)

    agent = TextCommandAgent()

    # Simulate agent sending commands based on some logic or user input
    while rclpy.ok():
        user_input = input("Enter command value (e.g., 5, 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        try:
            command_value = int(user_input)
            agent.send_goal(command_value)
            time.sleep(1) # Give time for action to start
        except ValueError:
            agent.get_logger().warn('Invalid input. Please enter an integer.')

    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()