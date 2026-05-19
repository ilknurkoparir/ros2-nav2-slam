# ROS2 Autonomous Navigation and SLAM
Bu projede, Nav2 paketi kullanılarak robotun gezinme, engellerden kaçınma ve yol planlama (Path planning) işlemleri gerçekleştirilmiştir. Robotun konumlandırma işlemleri yapılmış ve slam_toolbox kullanılarak ortamın haritalanması sağlanmıştır. Son aşamada oluşturulan harita kaydedilmiş ve ilerleyen çalışmalarda yeniden kullanılabilir hâle getirilmiştir.

⚠️ **Uyarı:** Robot modelini ve gerekli tüm bileşenleri oluşturmaya başlamadan önce, bazı paketlerin kurulu olduğundan emin olun. Aşağıdaki komutları çalıştırın.

### Gerekli Paketlerin Kurulumu

```bash
$ sudo apt install ros-humble-robot-localization
$ sudo apt install ros-humble-navigation2
$ sudo apt install ros-humble-nav2-bringup
$ sudo apt install ros-humble-slam-toolbox
```
## Paket Oluşturma ve URDF Robot Modeli

Bu bölümde, bir ROS 2 paketi oluşturulacak ve URDF tabanlı bir robot modeli hazırlanacaktır.

### ROS Paketi Oluşturma
İlk olarak yeni bir ROS 2 paketi oluşturulacaktır.
```bash
$ cd ~/ros2_ws_1/src
$ ros2 pkg create robot_description_1 --build-type ament-python
```

### Klasör Yapısının Oluşturulması
Paket içerisinde daha düzenli ve okunabilir bir yapı oluşturmak amacıyla gerekli klasörler oluşturulacaktır.
```bash
$ cd ~/ros2_ws/src/robot_description_1
$ mkdir launch urdf maps worlds config
```

İki tekerlekli robot modeli için, robotun modellenme sürecini daha modüler ve yönetilebilir hâle getirmek amacıyla xacro yapısının sunduğu çeşitli özelliklerden yararlanılmıştır. `urdf` klasörü içerisinde, robotun tüm bileşenlerini bir araya getirerek nihai hâlini temsil eden `main.xacro` dosyası oluşturulmuştur. Robotun temel yapısını ve iskeletini tanımlayan ana dosya olarak `my_robot.xacro` kullanılmıştır.

Bununla birlikte, her bir bağlantının (link) renk ve görsel özelliklerinin tanımlandığı `properties.xacro` dosyası oluşturulmuş, Gazebo simülatörü üzerinde robotun diferansiyel sürüş mekanizmasının çalışabilmesi için gerekli ayarların yapıldığı `properties_gazebo.xacro` dosyası eklenmiştir. Ayrıca robotun çevresini algılayabilmesi amacıyla lidar sensörüne ait tanımlamaların yapıldığı `lidar.xacro` ve kamera sensörünün özelliklerinin belirlendiği `camera.xacro` dosyaları oluşturulmuştur. Bu modüler yapı sayesinde robot modeli hem simülasyon hem de geliştirme süreçlerinde daha esnek ve sürdürülebilir bir şekilde yönetilebilmektedir.

<img width="1412" height="919" alt="image" src="https://github.com/user-attachments/assets/5b9e757a-fa29-42d1-a4d2-567d60d2f7cd" />

<img width="1074" height="518" alt="Screenshot from 2025-12-05 17-58-20" src="https://github.com/user-attachments/assets/9ece0e98-1cac-457f-b4e6-53261ba6a1ad" />

Bu aşamada robot, RViz ve Gazebo ortamlarında başarıyla görselleştirilmiştir. `robot_gazebo.launch.py` adlı yeni bir launch dosyası oluşturulmuş, ardından paket derlenmiş ve ilgili launch dosyası çalıştırılmıştır.


## Robot Haritalama

Haritalama, robotik sistemler için kritik bir öneme sahiptir. Robotun çalışma ortamına ait bir haritaya sahip olması, ortam hakkında bilgi edinilmesini sağlamakta ve bu sayede farklı görevlerin daha verimli bir şekilde gerçekleştirilmesine olanak tanımaktadır. Haritalama işlemi, derinlik kameraları ve lidar gibi mesafe ölçümü yapan sensörlerden elde edilen veriler kullanılarak gerçekleştirilmektedir.

### slam_toolbox Kullanımı

Bu projede robotun bulunduğu ortamın eş zamanlı olarak haritalanabilmesi için `slam_toolbox` paketi kullanılmıştır. `slam_toolbox`, lidar ve diğer mesafe sensörlerinden elde edilen veriler yardımıyla robotun konumunu belirlerken aynı anda ortamın haritasını oluşturmaya olanak tanımaktadır. Bu sayede robot, bilinmeyen bir ortamda gezinirken çevresini algılayarak kendi haritasını oluşturabilmiştir.

```bash
$ cp /opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml /home/projenizin_yolu
$ ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/home/ilknur/ros2_ws_1/src/robot_description_1/config/mapper_params_online_async.yaml use_sim_time:=true
```
```bash
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: base_footprint
scan_topic: /scan          # Eğer lidar /scan dışında farklı bir topic yayınlıyorsa, bu alanı kullanılan lidar topic adına göre güncelleyin
use_map_saver: true
mode: localization         # Haritalama yapmak için 'mapping' olarak ayarlayın.
                            # Kaydedilmiş bir haritayı kullanarak konumlandırma yapmak için 'localization' modunu kullanın

```

Haritalama esnasında robotu klavyeden hareket ettirmek için aşağıdaki komutun kullanın.

```bash
$ ros2 run teleop_twist_keyboard teleop_twist_keyboard

```
## **Haritalama Yapılmadan Önce**
<img width="940" height="653" alt="Screenshot from 2025-12-30 20-53-02" src="https://github.com/user-attachments/assets/d89fb5d8-2862-4ab6-ab3f-0f01ba58dfd9" />

## **Haritalama Yapıldıktan Sonra**
<img width="940" height="653" alt="Screenshot from 2025-12-30 20-56-06" src="https://github.com/user-attachments/assets/3cfa0294-3fcb-4e87-9600-3d9fbe549599" />

### Harita Kaydetme

Haritalama işlemi tamamlandıktan sonra oluşturulan ortam haritası kaydedilmiştir. Kaydedilen harita, daha sonraki çalışmalarda yeniden kullanılmak üzere saklanmış ve böylece robotun aynı ortamda tekrar haritalama yapmadan konumlandırma ve gezinme işlemlerini gerçekleştirmesi mümkün hâle getirilmiştir.

```bash
$ ros2 run nav2_map_server map_saver_cli -f my_map

```
## Otonom Sürüş

Harita yüklendikten ve robotun başlangıç konumu tanımlandıktan sonra, robota hedef bir konum verilebilmektedir. Bunun için yeni bir terminal açarak aşağıdaki komut çalıştırılmıştır.

```bash
$ ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true


```

Bu işlemden sonra robot, belirlenen hedef konuma ulaşmak için uygun bir yol oluşturmuş ve hareket etmeye başlamıştır. Hedefe ilerlerken, daha önce bilinmeyen engeller de dâhil olmak üzere karşılaştığı tüm engellerden kaçınabilecek yeteneğe sahiptir.


<img width="940" height="653" alt="Screenshot from 2025-12-30 18-25-03" src="https://github.com/user-attachments/assets/f60a50a5-48de-418c-98e6-f558592b6f0b" />


## İletişim

Proje ile ilgili sorularınız, geri bildirimleriniz için aşağıdaki e-posta adresi üzerinden iletişime geçebilirsiniz:

📧 **E-posta:** ilknurkoparir262@gmail.com
