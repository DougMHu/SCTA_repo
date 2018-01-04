SNMP Drivers
************

Simple Network Management Protocol (SNMP) is an Internet-standard protocol for collecting and organizing information about managed devices on IP networks and for modifying that information to change device behavior. SNMP exposes management data in the form of variables called management information base (MIB) objects which describe the system status and configuration. These variables can then be remotely queried and manipulated.

Some RF equipment, like the DM240XR, VTM, and VTR strictly use SNMP for remote interaction.

Instead of using proper Python libraries for interacting over SNMP, we use Windows batch files that implement the SNMP ``set`` and ``get`` commands. Unfortunately, this restricts our automation libraries to Windows only if you want to interact with equipment over SNMP. The batch files ``SnmpSet`` and ``SnmpGet`` can be found under ``SCTA_repo\install\``.
Copy the batch files to the ``C:`` drive on your Windows machine.