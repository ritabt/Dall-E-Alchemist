from os import listdir
from os.path import isfile, join
from collections import defaultdict
import os


mypath = "C:\\Users\\ritat\\OneDrive\\Desktop\\DallE Images"
savepath = "C:\\Users\\ritat\\OneDrive\\Desktop\\Organized DallE"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

count = defaultdict(int)

for f in onlyfiles:
	idx = f.index(',')
	names = f[:idx].split()
	names.sort()
	folder_name = ' '.join(names)
	file_name = folder_name+" "+str(count[folder_name])+".png"
	count[folder_name] += 1
	save_folder = join(savepath, folder_name)
	if not os.path.exists(save_folder):
		os.makedirs(save_folder)
	file_path = join(save_folder, file_name)
	os.rename(join(mypath,f), file_path)

# ["star wrench, wrench in the shape of star", "star coconut, coconut in the shape of star", "fish crab, crab in the shape of fish", "fish seashell, seashell in the shape of fish", "fish dollar, dollar in the shape of fish", "fish star, star in the shape of fish", "fish fish, fish in the shape of fish", "fish sand, sand in the shape of fish", "fish screwdriver, screwdriver in the shape of fish", "fish hammer, hammer in the shape of fish", "fish wrench, wrench in the shape of fish", "fish coconut, coconut in the shape of fish", "sand crab, crab in the shape of sand", "sand seashell, seashell in the shape of sand", "sand dollar, dollar in the shape of sand", "sand star, star in the shape of sand", "sand fish, fish in the shape of sand", "sand sand, sand in the shape of sand", "sand screwdriver, screwdriver in the shape of sand", "sand hammer, hammer in the shape of sand", "sand wrench, wrench in the shape of sand", "sand coconut, coconut in the shape of sand", "screwdriver crab, crab in the shape of screwdriver", "screwdriver seashell, seashell in the shape of screwdriver", "screwdriver dollar, dollar in the shape of screwdriver", "screwdriver star, star in the shape of screwdriver", "screwdriver fish, fish in the shape of screwdriver", "screwdriver sand, sand in the shape of screwdriver", "screwdriver screwdriver, screwdriver in the shape of screwdriver", "screwdriver hammer, hammer in the shape of screwdriver", "screwdriver wrench, wrench in the shape of screwdriver", "screwdriver coconut, coconut in the shape of screwdriver", "hammer crab, crab in the shape of hammer", "hammer seashell, seashell in the shape of hammer", "hammer dollar, dollar in the shape of hammer", "hammer star, star in the shape of hammer", "hammer fish, fish in the shape of hammer", "hammer sand, sand in the shape of hammer", "hammer screwdriver, screwdriver in the shape of hammer", "hammer hammer, hammer in the shape of hammer", "hammer wrench, wrench in the shape of hammer", "hammer coconut, coconut in the shape of hammer", "wrench crab, crab in the shape of wrench", "wrench seashell, seashell in the shape of wrench", "wrench dollar, dollar in the shape of wrench", "wrench star, star in the shape of wrench", "wrench fish, fish in the shape of wrench", "wrench sand, sand in the shape of wrench", "wrench screwdriver, screwdriver in the shape of wrench", "wrench hammer, hammer in the shape of wrench", "wrench wrench, wrench in the shape of wrench", "wrench coconut, coconut in the shape of wrench", "coconut crab, crab in the shape of coconut", "coconut seashell, seashell in the shape of coconut", "coconut dollar, dollar in the shape of coconut", "coconut star, star in the shape of coconut", "coconut fish, fish in the shape of coconut", "coconut sand, sand in the shape of coconut", "coconut screwdriver, screwdriver in the shape of coconut", "coconut hammer, hammer in the shape of coconut", "coconut wrench, wrench in the shape of coconut", "coconut coconut, coconut in the shape of coconut"]


