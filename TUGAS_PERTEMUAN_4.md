# Tugas Pertemuan 4

## 1. Fungsi Tag `<ros2_control>` pada URDF

Tag `<ros2_control>` digunakan untuk menghubungkan model robot pada URDF dengan sistem kontrol ROS 2. Tag ini menentukan hardware interface serta interface perintah dan status pada setiap joint. Pada robot ini digunakan hardware plugin `mock_components/GenericSystem`.

## 2. Controller dan Node yang Digunakan

Controller yang digunakan adalah `position_controllers/JointGroupPositionController` dengan nama `arm_controller`. Controller ini mengatur posisi `joint_1`, `joint_2`, dan `joint_3`.

Node yang dijalankan melalui `arm.bringup.launch.py` adalah:
- `robot_state_publisher`
- `ros2_control_node`
- `controller_spawner`, untuk menjalankan `joint_state_broadcaster` dan `arm_controller`
- `rviz2`


## 3. Forward Kinematics

Dengan nilai sudut `joint_1 = 0.00 rad` dan `joint_2 = 0.00 rad`, posisi origin `joint_3` terhadap `base_link` dihitung menggunakan:

\[
x=0.20\sin(q_2)\cos(q_1+0.6)
\]
\[
y=0.20\sin(q_2)\sin(q_1+0.6)
\]
\[
z=0.10+0.20\cos(q_2)
\]

Hasil perhitungan:

- `x = 0.00 m`
- `y = 0.00 m`
- `z = 0.30 m`

Jadi, posisi `joint_3` adalah **(0.00, 0.00, 0.30) meter** relatif terhadap `base_link`.