# MAGANG AL-FATIH

## PERTEMUAN 3

### KONVERSI QUATERNION KE ROLL, PITCH, DAN YAW (RPY)

Project ini menggunakan ROS 2 untuk mengirim data Quaternion dari node publisher dan mengonversinya menjadi sudut Roll, Pitch, dan Yaw pada node subscriber.

### Package

- `arm_control` — node publisher dan subscriber untuk konversi Quaternion ke RPY.
- `arm_model` — model lengan robot dalam format URDF dan tampilan RViz.
- `arm_bringup` — konfigurasi dan launch untuk menjalankan sistem robot.
- `py_pubsub` — contoh komunikasi publisher dan subscriber.

## PERTEMUAN 4

### MODEL LENGAN ROBOT

Model robot dibuat menggunakan URDF dan divisualisasikan melalui RViz. Robot memiliki tiga joint revolute yang dapat diatur melalui Joint State Publisher GUI.

## CARA MENJALANKAN PROGRAM

### Build package

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### Menjalankan publisher

```bash
ros2 run arm_control arm_publisher
```

### Menjalankan subscriber

Buka terminal baru, lalu jalankan:

```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run arm_control arm_subscriber
```

### Menampilkan model robot

```bash
ros2 launch arm_model display.launch.py
```

## KEBUTUHAN

- Ubuntu
- ROS 2 Jazzy
- RViz
- Python 3

