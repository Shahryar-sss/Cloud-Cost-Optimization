migration = open("./Logs/Migration.txt", "w", 1)
vmAllocation = open("./Logs/VmAllocation.txt", "w", 1)
finishedExecution = open("./Logs/FinishedExecution.txt", "w", 1)
outputTables = open("./Logs/OutputTables.txt", "w", 1)

def printMessage(type, message):
    if type == "CloudletAllocationAndMigration":
        migration.write(message)
        migration.write("\n")
        print(message)

    elif type == "VmAllocation":
        vmAllocation.write(message)
        vmAllocation.write("\n")
        print(message)

    elif type == "FinishedExecution":
        finishedExecution.write(message)
        finishedExecution.write("\n")
        print(message)

    elif type == "OutputTables":
        outputTables.write(message)
        if message != "\n":
            outputTables.write("\n")
        print(message)

    else:
        print(message)