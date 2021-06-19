# Cost Optimization in AWS Spot Instances

## Dataset Source

Data | Source
------------ | -------------
AWS Spot Price History | [AWS archive](https://aws.amazon.com)
AWS On Demand Pricing | [AWS On Demand Pricing Page](https://aws.amazon.com/ec2/pricing/on-demand/)
Demand Data | [Google Cluster Usage Trace](https://research.google/tools/datasets/google-cluster-workload-traces-2019/)
Machine Configuration Data | [Google Cloud Machine Types](https://cloud.google.com/compute/docs/machine-types)

## Dataset format

The above dataset is aggregated into a python dictionary which is of the format

KEY: VM Type

VALUE: LIST -> 
  1. MIPS
  2. RAM
  3. Bandwidth
  4. On Demand Price
  5. LIST -> Spot Prices
  6. LIST -> Spot Scores
  7. Category of the VM

## Program Flow

Outlined below is a basic overview of the structure of the program.

### [Main.py](https://github.com/Shahryar-sss/Cloud-Cost-Optimization/blob/master/Main.py)

Execution starts from this file. A datacenter is first created with appropriate characteristics. Then a datacenter broker is created, using the required VM allocation policy and cloudlet allocation policy. A list of hosts is then created and assigned to the datacenter. Finally a list of cloudlets is created and submitted to the broker for execution.

### [DatacenterBroker.py](https://github.com/Shahryar-sss/Cloud-Cost-Optimization/blob/master/DatacenterBroker.py)

On receiving a list of cloudlets from the Main.py file, the broker chooses a VM from the configuration data available and provisions it in accordance with the cloudlet allocation policy and places the VM into a host according to the VM allocation policy.

### [VmThread](https://github.com/Shahryar-sss/Cloud-Cost-Optimization/blob/master/VmThread.py)

This thread constantly monitors the VMs running, and is responsible for the following:

1. Deprovisioning VM when corrsponding cloudlet has finished execution.
2. In case of cloudlet migration, deletes the VM freed up and invokes broker to assign a new VM to the migrating cloudlet.

### [ClockThread.py](https://github.com/Shahryar-sss/Cloud-Cost-Optimization/blob/master/ClockThread.py)

This thread constantly monitors the running cloudlet, and on **every clock tick**, does the following:

1. Checks if cloudlet needs to migrate based on RAM utilisation or increase in spot price above the on demand price
    1. Migrates the cloudlet if required
        1. Inserts the end time for the cloudlet-vm combination into a list property of the cloudlet object
        2. Sets the previous allocated VM type of the cloudlet to the current VM type, to avoid possible infinite loops during migration
        3. Sets the migration event to RAM or SPOT_SCORE, depending on the event.
        4. Removes the cloudlet from its assigned VM
    2. This is detected by VmThread.py, which then assigns a new VM according to above description.
2. If migration is not required, then decrements the length of the cloudlet according to the MIPS of the assigned VM.

<hr/>

The output of the program is printed to the console window and to the appropriate log files inside the log folder.
