

# words = ["sapphire", "sword", "blueberry", "redberry", "apple", "water", "cinnamon"]
words = ["crab", "seashell", "dollar", "star", "fish", "sand", "screwdriver", "hammer", "wrench", "coconut"]
combinations = [
				"1 2, 2 in the shape of 1",
				]

# num_per_combination = [3]

# num_imgs = []
prompts = []
folders = []
subfolders = []

final_print = "["

# Make word combinations
for i in range(len(words)):
	for j in range(len(words)):
		# print("______________________________________________________")

		# Add extras
		for k, s in enumerate(combinations):
			while(s.find("1")!=-1):
				idx = s.find("1")
				s =  s[:idx] + words[i] + s[idx+1:]
			while(s.find("2")!=-1):
				idx = s.find("2")
				s =  s[:idx] + words[j] + s[idx+1:]
			# print("i = ", i, " j = ", j, " k = ", k, " Prompt = ", s)
			folders.append(words[i])
			subfolders.append(words[j])
			prompts.append(s)
			final_print += "\""+s+"\", "
			# num_imgs.append(num_per_combination[k])
final_print += "]"
print(final_print)
print("______________________________________________________")
print("Total number of prompts = ", len(prompts))