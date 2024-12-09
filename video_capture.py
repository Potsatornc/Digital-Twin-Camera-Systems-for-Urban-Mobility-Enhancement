import os
import time
from datetime import datetime, timedelta

example_folder =  "/home/admin/Desktop/test_pic"

reboot_count_file = os.path.join(example_folder, "reboot_count.txt")

if not os.path.exists(example_folder):
	os.makedirs(example_folder)

def get_last_image_filename(folder):
	files = [f for f in os.listdir(folder) if f.endswith('.jpg')]
	if files:
		files.sort(key = lambda x: os.path.getmtime(os.path.join(folder, x)), reverse = True)
		return files[0]
	return None

def extract_timestamp_from_filename(filename):
	try:
		name_part = filename.replace("image_","").replace(".jpg","")
		timestamp_part = name_part_rsplit("-", 1)[0]
		return datetime.strptime(timestamp_part, "%d_%m_%Y-%H_%M_%S")
	except Exception as e:
		print(f"Error parsing timestamp: {e}")
		return None

def check_reboot_and_update_count():
	if os.path.exists(reboot_count_file):
		with open(reboot_count_file, 'r') as file:
			count = int(file.read().strip())

	else:
		count = 0
	count += 1
	with open(reboot_count_file, 'w') as file:
		file.write(str(count))
	return count

def capture_images():
	try:

		reboot_count = check_reboot_and_update_count()

		last_image   = get_last_image_filename(example_folder)


		if last_image:
			print(f"Resuming from the last image: {last_iamge}")
			last_timestamp = extract_timestamp_from_filename(last_image)

			if last_timestamp:
				next_timestamp = last_timestamp + timedelta(seconds = 60)
			else:
				next_timestamp = datetime.now()
		else:
			print("No previous images found. Starting frash.")
			next_timestamp = datetime.now()

		while True:

			timestamp_str = next_timestamp.strftime(f"%d_%m_%Y-%H_%M_%S-{reboot_count:02d}")
			file_path     = os.path.join(example_folder, f"image_{timestamp_str}.jpg")

			os.system(f"libcamara-still -o {file_path}")
			print(f"Captured image and saved to {file_path}")

			next_timestamp  += timedelta(seconds = 60)
			time.sleep(60)

	except KeyboardInterrupt:
		print("Process Interrupted.")

capture_images()
