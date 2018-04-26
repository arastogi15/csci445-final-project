result = np.empty((0,5))
        end_time = self.time.time() + 10
        while self.time.time() < end_time:
            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                goal_theta = math.atan2(goal_y - self.odometry.y, goal_x - self.odometry.x)
                theta = math.atan2(math.sin(self.odometry.theta), math.cos(self.odometry.theta))
                print("[{},{},{}]".format(self.odometry.x, self.odometry.y, math.degrees(self.odometry.theta)))
                new_row = [self.time.time(), math.degrees(self.odometry.theta), math.degrees(goal_theta), self.odometry.x, self.odometry.y]
                result = np.vstack([result, new_row])

                output_theta = self.pidTheta.update(self.odometry.theta, goal_theta, self.time.time())

                # improved version 2: fuse with velocity controller
                distance = math.sqrt(math.pow(goal_x - self.odometry.x, 2) + math.pow(goal_y - self.odometry.y, 2))
                output_distance = self.pidDistance.update(0, distance, self.time.time())
                self.create.drive_direct(int(output_theta + output_distance), int(-output_theta + output_distance))
