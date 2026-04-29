# 🤖 dofbot_ros2

ROS 2 packages for the **Yahboom DOFBOT** — a 6-DOF AI Vision Robotic Arm.  
This repository provides robot configuration and MoveIt 2 motion-planning support for controlling DOFBOT under ROS 2.

---

## 📦 Packages

| Package | Description |
|---|---|
| `dofbot_config` | URDF/SRDF robot description, joint configuration, and launch files |
| `dofbot_moveit` | MoveIt 2 motion planning integration, trajectory execution, and demo launch |

---

## 🛠️ Prerequisites

| Requirement | Version |
|---|---|
| OS | Ubuntu 22.04 (Jammy) |
| ROS 2 | Humble Hawksbill |
| MoveIt 2 | `ros-humble-moveit` |
| Python | 3.10+ |
| Build tool | `colcon` |

Install ROS 2 dependencies:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-moveit \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-joint-state-publisher-gui \
  ros-humble-robot-state-publisher \
  python3-colcon-common-extensions
```

---

## 🚀 Installation

```bash
# 1. Create a workspace
mkdir -p ~/dofbot_ws/src
cd ~/dofbot_ws/src

# 2. Clone this repository
git clone https://github.com/pan-k15/dofbot_ros2.git

# 3. Install ROS dependencies
cd ~/dofbot_ws
rosdep install --from-paths src --ignore-src -r -y

# 4. Build
colcon build --symlink-install

# 5. Source the workspace
source install/setup.bash
```

---

## ▶️ Usage

### Visualize the Robot (RViz)

```bash
ros2 launch dofbot_config display.launch.py
```

### MoveIt 2 Demo (Simulated)

```bash
ros2 launch dofbot_moveit demo.launch.py
```

This opens RViz with the MoveIt Motion Planning plugin. You can drag the interactive marker to set a goal pose and click **Plan & Execute**.

---

## 📂 Repository Structure

```
dofbot_ros2/
├── dofbot_config/          # Robot description package
│   ├── urdf/               # URDF/XACRO robot model
│   ├── config/             # Joint limits, controllers
│   └── launch/             # Display and bringup launch files
├── dofbot_moveit/          # MoveIt 2 configuration package
│   ├── config/             # SRDF, kinematics, planning pipeline
│   └── launch/             # MoveIt demo launch files
└── README.md
```

---

## 🦾 About DOFBOT

DOFBOT is a 6-DOF serial bus servo robotic arm developed by **Yahboom**, designed for AI and robotics education. It supports:

- Forward/inverse kinematics
- MoveIt motion planning and simulation
- Cartesian path planning
- Collision detection
- AI vision tasks (color recognition, gesture control, etc.)

---

## 📄 License

This project is open source. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Yahboom Technology](https://www.yahboom.net) — DOFBOT hardware and reference software
- [MoveIt 2](https://moveit.picknik.ai) — Motion planning framework
- [ROS 2 Humble](https://docs.ros.org/en/humble/) — Robot Operating System
