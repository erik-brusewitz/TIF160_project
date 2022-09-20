import robot as rob

sc.initialize_communication()
print("Initializing robot software")
hubert = robot()
print("AAAAAAAAAAAAAAAAAAA")
hubert.info('body')
print("BBBBBBBBBBBBBBBBBBBB")
hubert.move('body',1)

# hubert.move('head', 1)
# hubert.info('head')
# hubert.move('shoulder',2)
# hubert.info('shoulder')

# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value