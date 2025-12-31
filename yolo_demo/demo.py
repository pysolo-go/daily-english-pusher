from ultralytics import YOLO
import os
import sys

# 确保在 yolo_demo 目录下运行
os.makedirs("yolo_demo", exist_ok=True)
if os.path.basename(os.getcwd()) != "yolo_demo" and os.path.exists("yolo_demo"):
    os.chdir("yolo_demo")

# 1. 获取图片路径
if len(sys.argv) > 1:
    image_source = sys.argv[1]
    print(f"正在处理用户提供的图片: {image_source}")
else:
    image_source = 'https://ultralytics.com/images/bus.jpg'
    print(f"未提供图片路径，使用默认示例图: {image_source}")

# 2. 加载模型
# yolov8n.pt 是最轻量级的版本，速度快
if not os.path.exists('yolov8n.pt'):
    print("正在下载模型 yolov8n.pt ...")
model = YOLO('yolov8n.pt')

# 3. 预测图片
print(f"开始检测...")
results = model(image_source)

# 4. 展示结果
for result in results:
    # 保存结果图
    save_path = 'result_custom.jpg'
    result.save(filename=save_path)
    print(f"检测完成！结果已保存为 {os.path.abspath(save_path)}")
    
    # 打印检测到的物体
    print("\n检测到的物体统计：")
    counts = {}
    if result.boxes:
        for box in result.boxes:
            class_id = int(box.cls)
            class_name = result.names[class_id]
            conf = float(box.conf)
            print(f"  Found {class_name} (conf: {conf:.2f})")
            counts[class_name] = counts.get(class_name, 0) + 1
            
        print("\n汇总:")
        for name, count in counts.items():
            print(f"- {name}: {count} 个")
    else:
        print("未检测到任何已知物体。")

print(f"\n请打开 {os.path.abspath(save_path)} 查看结果！")
